#!/usr/bin/env python3
"""Sincronización bidireccional entre askaro_lexico_v11.csv y askaro_lexico.db

Uso:
  python3 scripts/lexico_db.py csv2db    # Regenera la BD desde el CSV (fuente de verdad inicial)
  python3 scripts/lexico_db.py db2csv    # Exporta la BD al CSV (tras trabajar en SQLite)
  python3 scripts/lexico_db.py status    # Comparar conteos e identificar desfases
"""
import csv, sqlite3, sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE, 'askaro_lexico_v11.csv')
DB_PATH = os.path.join(BASE, 'askaro_lexico.db')


def read_csv():
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [r for r in reader if any(c.strip() for c in r)]
    return header, rows


def csv2db():
    header, rows = read_csv()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS lexico')
    cols_def = ', '.join(f'"{c}" TEXT' for c in header)
    cur.execute(f'CREATE TABLE lexico ({cols_def}, PRIMARY KEY ("id"))')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_termino ON lexico("termino_askaro")')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_espanol ON lexico("espanol")')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_categoria ON lexico("categoria")')
    ph = ','.join('?' * len(header))
    cur.executemany(f'INSERT INTO lexico VALUES ({ph})', rows)
    conn.commit()
    n = cur.execute('SELECT COUNT(*) FROM lexico').fetchone()[0]
    conn.close()
    print(f'csv2db OK: {n} términos -> {DB_PATH}')


def db2csv():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('PRAGMA table_info(lexico)')
    header = [r[1] for r in cur.fetchall()]
    # conservar el orden original del archivo si existe
    if os.path.exists(CSV_PATH):
        orig_header, _ = read_csv()
        if set(orig_header) == set(header):
            header = orig_header
    cols = ', '.join(f'"{c}"' for c in header)
    rows = cur.execute(f'SELECT {cols} FROM lexico ORDER BY id').fetchall()
    conn.close()
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f'db2csv OK: {len(rows)} términos -> {CSV_PATH}')


def status():
    header, rows = read_csv()
    conn = sqlite3.connect(DB_PATH)
    n_db = conn.execute('SELECT COUNT(*) FROM lexico').fetchone()[0]
    ids_db = {r[0] for r in conn.execute('SELECT id FROM lexico')}
    conn.close()
    ids_csv = {r[0] for r in rows}
    print(f'CSV: {len(rows)} filas | BD: {n_db} filas')
    print(f'Solo en BD (nuevos acuñados): {sorted(ids_db - ids_csv)[:20]}')
    print(f'Solo en CSV (eliminados sin exportar): {sorted(ids_csv - ids_db)[:20]}')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    {'csv2db': csv2db, 'db2csv': db2csv, 'status': status}[cmd]()
