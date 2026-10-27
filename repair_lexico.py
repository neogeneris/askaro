#!/usr/bin/env python3
"""Reparar lexico.db: los triggers trg_concepto_unique_insert y trg_emoji_unique_insert
quedaron truncados en sqlite_master (sqlite3 no puede parsear el schema).
Estrategia:
 1. Parsear crudo de sqlite_master para extraer todo el DDL con SQL completo.
 2. Reconstruir la BD desde cero con ese DDL + datos, redefiniendo los triggers rotos
    sin concatenación || dentro de RAISE() (incompatibilidad que causó el truncado).
Uso: python3 repair_lexico.py [src.db] [dst.db]
"""
import struct, sys, os

def read_varint(buf, p):
    n = 0; shift = 0
    while True:
        b = buf[p]; p += 1
        n |= (b & 0x7f) << shift
        if not (b & 0x80): break
        shift += 7
    return n, p

def ser_kind(t):
    if t == 0: return ('null', 0)
    if 1 <= t <= 4: return ('int', t)
    if t == 5: return ('int', 6)
    if t == 6: return ('float', 8)
    if t == 7: return ('blob', 0)
    if t >= 12 and t % 2 == 0: return ('blob', (t - 12) // 2)
    if t >= 13: return ('text', (t - 13) // 2)
    return ('?', 0)

def parse_record(rec):
    hl, p = read_varint(rec, 0)
    hdr = rec[:hl]
    hp = 1
    types = []
    while hp < hl:
        t, hp = read_varint(hdr, hp)
        types.append(t)
    vals = []
    pos = hl
    for t in types:
        kind, size = ser_kind(t)
        if kind == 'null':
            vals.append(None)
        elif kind == 'int':
            vals.append(int.from_bytes(rec[pos:pos+size], 'big', signed=True)); pos += size
        elif kind == 'float':
            import struct as st
            vals.append(st.unpack('>d', rec[pos:pos+8])[0]); pos += 8
        elif kind in ('blob', 'text'):
            raw = bytes(rec[pos:pos+size]); pos += size
            vals.append(raw.decode('utf-8', errors='replace') if kind == 'text' else raw)
        else:
            return None
    return vals

class BTreeReader:
    def __init__(self, data, pagesize, reserved):
        self.data = data
        self.U = pagesize
        self.reserved = reserved
        self.M = pagesize - reserved

    def page(self, pgno):
        off = (pgno - 1) * self.U
        return self.data[off:off + self.U]

    def header_offsets(self, pgno):
        return (100, 108) if pgno == 1 else (0, 8)

    def walk(self, pgno):
        """Yield ('interior', left) o ('leaf', rowid, vals)."""
        hoff, ptrs_off = self.header_offsets(pgno)
        page = self.page(pgno)
        typ = page[hoff]
        ncells = struct.unpack('>H', page[hoff+3:hoff+5])[0]
        ptrs = [struct.unpack('>H', page[ptrs_off + 2*i:ptrs_off + 2*i + 2])[0]
                for i in range(ncells)]
        maxlocal = self.M - 35
        for cp in ptrs:
            if typ == 5:  # interior table node: left ptr varint + record key (NO payload-size first)
                left, p = read_varint(page, cp)
                # la clave es un record; el rowid máximo se obtiene del último entero del record.
                # Para nuestro recorrido solo necesitamos `left`.
                yield ('interior', left)
                continue
            if typ == 2:  # interior index node: left + key record
                left, p = read_varint(page, cp)
                yield ('interior', left)
                continue
            if typ not in (10, 13):
                return
            is_idx_leaf = (typ == 10)
            P, p = read_varint(page, cp)
            if not is_idx_leaf:
                rowid, p = read_varint(page, p)
            else:
                rowid = None
            # overflow si el primer varint es impar: codifica (U + X - 4), donde
            # U = bytes locales de payload y X = bytes en la página overflow.
            if P & 1:
                t = P >> 1                      # U + X - 4
                V, p = read_varint(page, p)     # V = tamaño total del payload
                rem = t - V + 4                 # = U (bytes locales)
                ovf_ptr = struct.unpack('>I', bytes(page[p+rem:p+rem+4]))[0]
                local = rem
                total = V
            else:
                total = P
                if P > self.M - 35:
                    Xl = (self.M - 35) + ((P - ((self.M - 35) + 4)) % (self.M - 4))
                    local = min(Xl, self.M - 3)
                    ovf_ptr = struct.unpack('>I', bytes(page[p+local:p+local+4]))[0]
                else:
                    local = P
                    ovf_ptr = 0
            rec = bytearray(page[p:p + local])
            need = total - local
            cur = ovf_ptr
            while need > 0 and cur:
                opage = self.page(cur)
                chunk = self.M - 4
                take = min(chunk, need)
                rec += opage[4:4 + take]
                nxt = struct.unpack('>I', opage[0:4])[0]
                need -= take
                cur = nxt
            vals = parse_record(rec)
            yield ('leaf', rowid, vals)

def walk_all(reader):
    """Recorren el B-tree de sqlite_master (raíz=página 1) y devuelven filas."""
    results = []
    stack = [1]
    while stack:
        pgno = stack.pop()
        for item in reader.walk(pgno):
            if item[0] == 'interior':
                if 1 < item[1] <= len(reader.data) // reader.U:
                    stack.append(item[1])
            else:
                results.append(item)
    results.sort(key=lambda r: r[0])
    return [(rowid, vals) for _, rowid, vals in results]

def main():
    import sqlite3
    src = sys.argv[1] if len(sys.argv) > 1 else 'lexico.db'
    dst = sys.argv[2] if len(sys.argv) > 2 else 'lexico_fixed.db'
    data = open(src, 'rb').read()
    pagesize = struct.unpack('>H', data[16:18])[0]
    if pagesize == 1:
        pagesize = 65536
    reserved = data[20]
    reader = BTreeReader(data, pagesize, reserved)
    schema = walk_all(reader)
    print(f'# {src}: {len(schema)} objetos de schema, pagesize={pagesize}')

    # --- arreglar SQL de triggers rotos (RAISE con || truncado) ---
    def fix_sql(sql):
        if sql and 'RAISE(ABORT,' in sql and "|| NEW." in sql:
            # sustituir SELECT RAISE(ABORT, 'msg' || NEW.col); por mensaje literal
            import re
            sql = re.sub(r"SELECT RAISE\(ABORT,\s*'([^']*?)'\s*\|\|[^;]*?\);",
                         lambda m: f"SELECT RAISE(ABORT, '{m.group(1).strip()}');", sql)
        return sql

    ddl = []
    tables = []
    for rowid, vals in schema:
        typ, name, tbl, rootpage, sql = vals[:5]
        sql = fix_sql(sql)
        ddl.append((typ, name, tbl, rootpage, sql))
        if typ == 'table':
            tables.append((name, rootpage, sql))
        print(f'{typ:9} {str(name):34} root={rootpage}')

    # --- extraer datos crudos por tabla ---
    tabdata = {}
    for name, root, tsql in tables:
        if name.startswith('sqlite_'):
            continue
        try:
            cols = [c[1] for c in __import__('re').finditer(__import__('re').compile(r''), '')]
        except Exception:
            pass
        rows = walk_all_cells(reader, root)
        tabdata[name] = rows
        print(f'#   {name}: {len(rows)} filas')

    # --- reconstruir BD ---
    if os.path.exists(dst):
        os.remove(dst)
    con = sqlite3.connect(dst)
    cur = con.cursor()
    # crear primero las tablas (sin índices/triggers), luego datos, luego índices/triggers
    for typ, name, tbl, root, sql in ddl:
        if typ == 'table' and sql:
            cur.execute(sql)
    for typ, name, tbl, root, sql in ddl:
        if typ == 'index' and sql:
            try:
                cur.execute(sql)
            except Exception as e:
                print('# WARN index', name, e)
    # insertar datos respetando rowid original
    for name, rows in tabdata.items():
        if not rows:
            continue
        ncols = max(len(v) for _, v in rows)
        collist = column_names(cur, name)
        if len(collist) != ncols:
            print(f'# WARN {name}: schema {len(collist)} cols vs {ncols} en registro; omite inserción por posición')
        ph = ','.join(['?'] * ncols)
        for rowid, vals in rows:
            vv = list(vals) + [None] * (ncols - len(vals))
            vv = vv[:ncols]
            try:
                cur.execute(f'INSERT INTO "{name}" (rowid) VALUES (?)' if False else
                            f'INSERT INTO "{name}" VALUES ({ph})', [x for x in vv])
            except Exception as e:
                print(f'# ERR {name} rowid={rowid}: {e}')
    # triggers al final
    for typ, name, tbl, root, sql in ddl:
        if typ == 'trigger' and sql:
            try:
                cur.execute(sql)
            except Exception as e:
                print('# WARN trigger', name, e)
    con.commit()
    print(cur.execute("PRAGMA integrity_check").fetchone())
    print('# escrito', dst)
    con.close()

def walk_all_cells(reader, rootpg):
    out = []
    stack = [rootpg]
    while stack:
        pgno = stack.pop()
        if pgno is None or pgno <= 0 or pgno > len(reader.data)//reader.U:
            continue
        for item in reader.walk(pgno):
            if item[0] == 'interior':
                stack.append(item[1])
            else:
                out.append((item[1], item[2]))
    out.sort(key=lambda r: r[0])
    return out

def column_names(cur, table):
    return [r[1] for r in cur.execute(f'PRAGMA table_info("{table}")')]

if __name__ == '__main__':
    main()
