import sqlite3, random
from collections import defaultdict

db = sqlite3.connect('sintesio.db')
db.row_factory = sqlite3.Row
cur = db.cursor()

rows = [dict(r) for r in cur.execute("""
  SELECT s.id, s.termino, s.espanol, s.grupo, m.confianza, m.animado, m.abstracto
  FROM matriz_rasgo m JOIN sustantivo s ON s.id = m.sustantivo_id
  ORDER BY s.id
""")]

def anim_class(r):
    if r['animado']=='si': return 'A'
    if r['abstracto']=='si': return 'B'
    return 'C'

QUOTAS = {
  'media': (40, {'A':0,'B':20,'C':20}),   # A: no hay animados en media (documentado)
  'baja':  (30, {'A':5,'B':12,'C':13}),   # A: proxy animales naturaleza/comida baja
  'alta':  (20, {'A':7,'B':3,'C':10}),
}

# Proxy de "animado" para estratos sin animados en matriz:
# animales típicos en grupo naturaleza/comida con confianza del estrato
PROXY_ANIM_BAJA = ['ASK-SUS-0121','ASK-SUS-0508','ASK-SUS-0510','ASK-SUS-1221','ASK-SUS-1226']

def select_stratum(cand, n, quota, max_per_group=15, forced_ids=None):
    bygc = defaultdict(lambda: defaultdict(list))
    picked, gcount, clscount, idx = [], defaultdict(int), defaultdict(int), defaultdict(int)
    cand_by_id = {r['id']: r for r in cand}
    # forzados primero (cuentan como clase A)
    for fid in (forced_ids or []):
        r = cand_by_id.get(fid)
        if r and gcount[r['grupo'] or '(sin grupo)'] < max_per_group:
            picked.append(r); gcount[r['grupo'] or '(sin grupo)']+=1; clscount['A']+=1
    for r in cand:
        if r['id'] in {p['id'] for p in picked}: continue
        bygc[r['grupo'] or '(sin grupo)'][anim_class(r)].append(r)
    groups = sorted(bygc.items(), key=lambda kv: (-sum(len(v) for v in kv[1].values()), kv[0]))
    def take(gname, c):
        lst = bygc[gname].get(c, [])
        k = idx[(gname,c)]
        if k < len(lst) and gcount[gname] < max_per_group:
            picked.append(lst[k]); idx[(gname,c)]=k+1; gcount[gname]+=1; clscount[c]+=1
            return True
        return False
    for c in ['A','B','C']:
        avail_c = sum(len(m.get(c,[])) for _,m in groups)
        need = min(quota[c], avail_c)
        while clscount[c] < need:
            progressed = False
            for gname,_ in groups:
                if clscount[c] >= need: break
                if take(gname, c): progressed = True
            if not progressed: break
    while len(picked) < n:
        deficit = {c: quota[c]-clscount[c] for c in 'ABC'}
        placed = False
        for c in sorted('ABC', key=lambda x: -deficit[x]):
            for gname,_ in sorted(groups, key=lambda kv: gcount[kv[0]]):
                if take(gname, c): placed=True; break
            if placed: break
        if not placed: break
    return picked[:n]

sel = {}
for estr,(n,quota) in QUOTAS.items():
    cand = [r for r in rows if r['confianza']==estr]
    forced = PROXY_ANIM_BAJA if estr=='baja' else None
    sel[estr] = select_stratum(cand, n, quota, forced_ids=forced)
    assert len(sel[estr])==n, (estr,len(sel[estr]))

used = {r['id'] for e in sel for r in sel[e]}
rest = [r for r in rows if r['id'] not in used]
random.seed(100)
sel['azar'] = random.sample(rest, 10)

all_sel = [(e,r) for e in ['media','baja','alta','azar'] for r in sel[e]]
assert len(all_sel)==100 and len({r['id'] for _,r in all_sel})==100

cur.executescript("""
DROP TABLE IF EXISTS gold_standard;
CREATE TABLE gold_standard (
    sustantivo_id TEXT PRIMARY KEY REFERENCES sustantivo(id) ON DELETE CASCADE,
    estrato       TEXT NOT NULL CHECK(estrato IN ('media','baja','alta','azar')),
    seleccion     INTEGER NOT NULL,
    clasificado_por TEXT DEFAULT 'pendiente',
    nota_curador  TEXT
);
""")
for i,(estr,r) in enumerate(all_sel, start=1):
    nota = 'proxy-animal (matriz dice animado=no)' if r['id'] in PROXY_ANIM_BAJA else None
    cur.execute("INSERT INTO gold_standard VALUES (?,?,?, 'pendiente', ?)", (r['id'], estr, i, nota))
db.commit()

print("Total:", cur.execute("SELECT COUNT(*) FROM gold_standard").fetchone()[0])
for e,n in cur.execute("SELECT estrato,COUNT(*) FROM gold_standard GROUP BY estrato"): print(f"  {e}: {n}")
print("\nMezcla por estrato:")
for e,a,ab,in_,tot in cur.execute("""SELECT g.estrato, SUM(m.animado='si'),
   SUM(m.animado='no' AND m.abstracto='si'), SUM(m.animado='no' AND m.abstracto='no'), COUNT(*)
   FROM gold_standard g JOIN matriz_rasgo m ON m.sustantivo_id=g.sustantivo_id GROUP BY 1"""):
    print(f"  {e}: animados(matriz)={a} abstractos={ab} inanimados={in_} total={tot}")
print("Animales-naturaleza/comida incluidos (proxy o reales):",
   cur.execute("""SELECT COUNT(*) FROM gold_standard g JOIN sustantivo s ON s.id=g.sustantivo_id
   WHERE s.grupo IN ('naturaleza','comida')""").fetchone()[0])
print("\nPor grupo:")
for gp,n in cur.execute("""SELECT COALESCE(NULLIF(s.grupo,''),'(sin grupo)'),COUNT(*)
  FROM gold_standard g JOIN sustantivo s ON s.id=g.sustantivo_id GROUP BY 1 ORDER BY 2 DESC"""):
    print(f"  {gp}: {n}")
