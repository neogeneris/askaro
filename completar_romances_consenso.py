#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
completar_romances_consenso.py — cierra los huecos de fr/it/pt/ro en `sustantivos`
y añade la columna de grado de consenso por término español importado a Askáro.

Fuentes (sin inventar): trad/batch1..8.py (traducciones manuales verificadas),
tablas lexico/DIRECTAS de askaro_romances.py como respaldo.

Consenso (escala 0–8, comparable con lexico.lenguas_consenso):
  votos = nº de lenguas {fr,it,pt,ro,ia,eo} cuya raíz normalizada agrupa >=2;
  es cuenta +1 si coincide con el bloque mayoritario (>=MIN_VOTOS);
  latin_vulgar (+1) y origen_etimologia latino (+1) respaldan el bloque.
  Se exige bloque >= MIN_VOTOS (3) para contar votos; si no hay bloque,
  grado = 1 (solo español).

Uso: python3 completar_romances_consenso.py          # dry-run + CSV
     python3 completar_romances_consenso.py --apply   # escribe en lexico.db
"""
import sqlite3, unicodedata, re, glob, sys, csv, shutil, os
from collections import defaultdict

DB = 'lexico.db'
MIN_VOTOS = 3
APPLY = '--apply' in sys.argv

def norm(s):
    if not s: return ''
    s = unicodedata.normalize('NFD', str(s).strip().lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'\([^)]*\)', '', s)
    s = re.sub(r'[^a-z ]', ' ', s)
    return ' '.join(s.split())

RO_MAP = {'ă':'a','â':'a','î':'i','ș':'s','ţ':'t','ş':'s','ț':'t','ć':'c','đ':'d'}
def strip_acc(s):
    s = unicodedata.normalize('NFC', (s or '').strip().lower())
    s = ''.join(RO_MAP.get(c, c) for c in s)
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.replace('ĉ','c').replace('ĝ','g').replace('ŭ','u').replace('ĥ','h')

def root(w):
    """raíz comparable para agrupar votos (igual criterio que consenso_ganadora.py:
    sin acentos, sin desinencia final; plural eo -oj/-ojn antes que -n/-o)."""
    r = strip_acc(w).replace(' ', '')
    # plurales/acusativo eo primero, luego desinencias romances plurales
    for suf in ('ojn','oj','jn','os','as','es'):
        if len(r) > len(suf)+3 and r.endswith(suf):
            r = r[:-len(suf)]
            break
    else:
        # singular: UNA sola vocal final (no recortar 'demokratio' -> 'demokrat')
        if len(r) > 4 and r[-1] in 'aeiou':
            r = r[:-1]
    return r

def same_root(a, b):
    """mismo bloque si raíces idénticas o una es prefijo de la otra con
    diferencia <=2 grafemas (tolera ortografías divergentes fr/ro/eo)."""
    ra, rb = root(a), root(b)
    if not ra or not rb: return False
    if ra == rb: return True
    x, y = sorted((ra, rb), key=len)
    return y.startswith(x) and (len(y)-len(x)) <= 2

def lev_sim(a, b):
    if not a or not b: return 0.0
    x, y = sorted((a, b), key=len)
    prev = list(range(len(y)+1))
    for i, cx in enumerate(x, 1):
        cur = [i]
        for j, cy in enumerate(y):
            cur.append(min(prev[j+1]+1, cur[j]+1, prev[j] + (cx != cy)))
        prev = cur
    return 1 - prev[len(y)]/max(len(x), len(y))

def extraer_etimo(txt):
    """étimo latino desde origen_etimologia (reutiliza lógica de askaro_romances)."""
    if not txt: return None
    m = re.search(r'([^>;]+?)\s*\((?:[^)]*(?:lat|gr)[^)]*)\)', txt, re.I)
    if m:
        cand = m.group(1).strip().split(',')[0].strip()
        cand = re.sub(r'^(?:lat\.?\s*(?:vulg\.?)?\s*)', '', cand, flags=re.I).strip()
        cand = re.sub(r'\(m\)$', '', cand, flags=re.I)
        parts = [p for p in cand.split() if p.lower() not in ('ecce','ad','de','in','ex','cum','a','ab')]
        cand = ' '.join(parts) if parts else cand
        if len(cand) >= 3 and re.fullmatch(r"[A-Za-zÀ-ž .'-]+", cand):
            if len(cand.split()) > 1:
                cand = max(cand.split(), key=len)
            return cand
    m = re.search(r'\b([A-ZĀĒĪŌŪ][A-ZĀĒĪŌŪ]{2,}[A-ZĀĒĪŌŪ])(?:\(M\))?\b', txt)
    return m.group(1) if m else None

# ---------------- diccionarios de traducción ----------------
TRAD = {}
for f in sorted(glob.glob('trad/batch*.py')):
    g = {'__name__': 'x'}
    exec(open(f, encoding='utf-8').read(), g)
    for k, v in g['D'].items():
        kk = norm(k)
        if kk and kk not in TRAD:
            TRAD[kk] = tuple(str(x) for x in v[:4])
# claves con paréntesis eliminados por norm() se indexan además por su forma cruda
EXTRA = {'plata metal ag': ('argent','argento','prata','argint')}
for k, v in EXTRA.items():
    TRAD.setdefault(norm(k), v)

def main():
    con = sqlite3.connect(DB); cur = con.cursor()
    rows = cur.execute("""SELECT id,codigo,forma,es,en,fr,it,pt,ro,ia,eo,latin_vulgar,
                          origen_etimologia FROM sustantivos ORDER BY id""").fetchall()
    def empty(v): return v is None or str(v).strip() in ('','-','—')

    out = []
    n_backfill = 0
    for rid, cod, forma, es, en, fr, it, pt, ro, ia, eo, lv, etim in rows:
        fills = {}
        if any(empty(x) for x in (fr, it, pt, ro)):
            k = norm(es)
            if k in TRAD:
                nf, ni, np_, nr = TRAD[k]
                for col, old, new in (('fr',fr,nf),('it',it,ni),('pt',pt,np_),('ro',ro,nr)):
                    if empty(old) and not empty(new):
                        fills[col] = new
                n_backfill += 1
        vals = {'es': es,
                'fr': fills.get('fr', fr), 'it': fills.get('it', it),
                'pt': fills.get('pt', pt), 'ro': fills.get('ro', ro),
                'ia': ia, 'eo': eo}
        # --- votación por bloques de raíz con tolerancia ortográfica ---
        langs = [lg for lg in ('fr','it','pt','ro','ia','eo') if not empty(vals.get(lg))]
        parent = {lg: lg for lg in langs}
        def find(x):
            while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
            return x
        def union(a, b):
            ra_, rb_ = find(a), find(b)
            if ra_ != rb_: parent[rb_] = ra_
        for i in range(len(langs)):
            for j in range(i+1, len(langs)):
                if same_root(vals[langs[i]], vals[langs[j]]):
                    union(langs[i], langs[j])
        comp = defaultdict(list)
        for lg in langs: comp[find(lg)].append(lg)
        bloques = sorted(comp.values(), key=lambda m: (-len(m), m[0]))
        best_members = bloques[0] if bloques else []
        best_root = root(vals[best_members[0]]) if best_members else None
        consenso = 0; gana = ''; bloque_ok = len(best_members) >= MIN_VOTOS
        if bloque_ok:
            consenso = len(best_members)
            if not empty(vals['es']) and any(same_root(vals['es'], vals[l]) for l in best_members):
                consenso += 1; gana = 'es'
            gana = gana or next((l for l in ('ia','eo','it','pt','ro','fr') if l in best_members), '')
        elif not empty(vals['es']):
            n_es = sum(1 for lg in langs if same_root(vals['es'], vals[lg]))
            if n_es >= 2:
                consenso = n_es + 1; gana = 'es-parcial'
            else:
                consenso = 1; gana = 'es-sin-bloque'
        # --- respaldos etimológicos ---
        etimo = extraer_etimo(etim)
        resp_lv = bool(lv and not empty(lv) and bloque_ok and
                       any(same_root(lv, vals[l]) for l in best_members))
        resp_lat = bool(etimo and bloque_ok and
                        lev_sim(root(etimo), best_root) >= 0.55)
        if resp_lv: consenso += 1
        if resp_lat: consenso += 1
        consenso = min(consenso, 8)
        out.append(dict(id=rid, codigo=cod, forma_askaro=forma, es=es, en=en,
                        fr=vals['fr'] or '', it=vals['it'] or '', pt=vals['pt'] or '',
                        ro=vals['ro'] or '', ia=vals['ia'] or '', eo=vals['eo'] or '',
                        backfill=('SI' if fills else 'NO'),
                        bloque=best_root or '', votos_bloque=len(best_members),
                        gana=gana, resp_lv=int(resp_lv), resp_lat=int(resp_lat),
                        grado_consenso_es=consenso))

    with open('consenso_sustantivos.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)

    dist = defaultdict(int)
    for o in out: dist[o['grado_consenso_es']] += 1
    print(f"filas: {len(out)} | backfill romances: {n_backfill}")
    print("distribución grado_consenso_es:", dict(sorted(dist.items())))

    if APPLY:
        shutil.copy(DB, DB + '.bak_pre_consenso_20261104')
        cols = {r[1] for r in cur.execute("PRAGMA table_info(sustantivos)")}
        for c in ('grado_consenso_es', 'fuente_consenso'):
            if c not in cols:
                cur.execute(f"ALTER TABLE sustantivos ADD COLUMN {c} INTEGER") if c=='grado_consenso_es' \
                    else cur.execute(f"ALTER TABLE sustantivos ADD COLUMN {c} TEXT")
        for o in out:
            cur.execute("UPDATE sustantivos SET fr=?,it=?,pt=?,ro=?,grado_consenso_es=?,fuente_consenso=? WHERE id=?",
                        (o['fr'] or None, o['it'] or None, o['pt'] or None, o['ro'] or None,
                         o['grado_consenso_es'], o['gana'] or None, o['id']))
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_sust_consenso ON sustantivos(grado_consenso_es)")
        except sqlite3.OperationalError:
            pass
        con.commit()
        print("APLICADO a lexico.db (backup: lexico.db.bak_pre_consenso_20261104)")
    else:
        print("(dry-run)")
    con.close()

if __name__ == '__main__':
    main()
