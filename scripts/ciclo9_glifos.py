#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ciclo 9: glifos UTF-8 -> sustantivos Askâro. Reglas maestro: h=/x/ (j esp), j=/Ê/, g siempre fuerte,
c suave/z/s -> s, c fuerte -> k, ll/ñ/rr se conservan; tilde explicito con >=2 vocales (penultima);
sustantivo -o neutral, -a solo femenino biologico; raiz desnuda + desinencia en imports_forma."""
import sqlite3, unicodedata, re

DB = "sintesio.db"

def norm_askaro(es, latin_root):
    """Ortografia askara desde la forma romance/latin verificada."""
    w = es.lower()
    w = w.replace("qu", "k").replace("ch", "c")          # ch -> c (africada)
    w = re.sub(r"[cz]", "s", w)                            # c suave, z, s -> s
    w = w.replace("c", "k")                                # c restante (fuerte) -> k
    w = w.replace("g", "g")                                # g siempre fuerte (get)
    w = w.replace("h", "j") if False else w                # h muda: se elimina abajo
    w = re.sub(r"^h", "", w)                               # h inicial muda -> elision
    w = w.replace("x", "ks")
    return w

def tilde_penult(w):
    """Tilde explicito sobre la penultima vocal si >=2 vocales y no lo lleva ya."""
    vowels = "aeiouáéíóúâêî"
    vs = [i for i, ch in enumerate(w) if ch in vowels]
    if len(vs) < 2:
        return w, None
    if any(ch in "áéíóúâêî" for ch in w):
        return w, "preexistente"
    idx = vs[-2]
    acc = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}
    w2 = w[:idx] + acc[w[idx]] + w[idx+1:]
    return w2, "penultima"

# (es, latin_root, emoji) — verificacion etimologica por fila
GLIFOS = [
    ("nieve",      "NIVEM",      "❄️"),
    ("hielo",      "GELUM",      "🧊"),
    ("arco",       "ARCUM",      "🏹"),
    ("flecha",     None,         "➡️"),   # germanico -> pendiente de criterio
    ("ancla",      "ANCORA",     "⚓"),
    ("timón",      "TEMON(em)",  "🧭"),
    ("brújula",    None,         "🧭"),   # duplicado de nucleo por simbolo
    ("mosca",      "MUSCA",      "🪰"),
    ("araña",      "ARANE(A)",   "🕷️"),
    ("telaraña",   "TELA+ARANEI","🕸️"),
    ("hormiga",    "FORMICA",    "🐜"),
    ("abeja",      "APIS/BACULUM","🐝"),
    ("libélula",   "LIBELLULA",  "🪰"),
    ("caracol",    "COCHLEA",    "🐌"),
    ("luciérnaga", LUM+"ICARIA", "✨"),
    ("erizo",      "ERI(C)IUS",  "🦔"),
    ("topo",       "TALPA",      "🐁"),
    ("castor",     "CASTOR",     "🦫"),
    ("nutria",     "LUTRA",      "🦦"),
    ("conejo",     CUNICULUS,    "🐇"),
    ("marmota",    MARMOTA,      "🐿️"),
    ("bisonte",    "BISONTE(m)", "🦬"),
    ("yak",        None,         "🐃"),   # tibetano -> no romance
    ("dromedario", "DROMEDARIUS","🐪"),
    ("llama",      "LGAMA(peruano)","🦙"), # quechua -> consenso?
]

con = sqlite3.connect(DB)
cur = con.cursor()
existing_es = {r[0] for r in cur.execute("SELECT concepto_espanol FROM imports")}
existing_roots = {r[0] for r in cur.execute("SELECT forma FROM imports_forma")}
lex_roots = set()
for t, in cur.execute("SELECT termino_norm FROM sustantivo"):
    lex_roots.add(t)

added = []
skipped = []
for es, latin, emoji in GLIFOS:
    if es in existing_es:
        skipped.append((es, "ya en imports")); continue
    base = norm_askaro(es, latin)
    forma_tonica, modo = tilde_penult(base)
    raiz = forma_tonica.rstrip("áéíóúâêî")  # marca queda en forma_tonica
    if forma_tonica in lex_roots or base in lex_roots:
        skipped.append((es, f"colision raiz con corpus ({base})")); continue
    genero = "a" if es in ("nutria",) else "o"   # femenino biologico real
    des = "-a" if genero == "a" else "-o"
    clase = "sustantivo"
    if latin is None:
        skip_reason = "sin raiz latina clara"
        skipped.append((es, skip_reason)); continue
    crit = "cognado_universal" if es in ("nieve","mosca","araña","hormiga","caracol","erizo","topo","castor","conejo","bisonte","dromedario") else "reconstruccion_latina"
    maxid = cur.execute("SELECT MAX(id) FROM imports").fetchone()[0] or 0
    nid = maxid + 1
    cur.execute("""INSERT INTO imports (id, concepto_espanol, es, palabra_sugerida, tipo_sugerencia,
                 estado, clase_gramatical, askaro_forma_norm, criterio_seleccion, etimologia, variantes)
                 VALUES (?,?,?,?,?,?,?, ?,?,?,?,?)""",
        (nid, es, es, forma_tonica, "auto-glifo", "propuesta", clase, forma_tonica, crit,
         f"lat. {latin}; glifo {emoji}", f"ciclo9:{emoji}"))
    cur.execute("INSERT INTO imports_forma (import_id, forma, desinencia, genero, forma_tonica, silaba_tonica) VALUES (?,?,?,?,?,?)",
        (nid, base, des, genero, forma_tonica, modo))
    added.append((es, base, forma_tonica, crit, emoji))

con.commit()
print(f"AÑADIDOS: {len(added)}  OMITIDOS: {len(skipped)}")
for e, b, ft, c, em in added: print(f"  {e:12s} -> {b:12s} tonica={ft:12s} [{c}] {em}")
print("OMITIDOS:")
for e, r in skipped: print(f"  {e}: {r}")
tot = cur.execute("SELECT COUNT(*) FROM imports").fetchone()[0]
print(f"TOTAL imports: {tot}")
con.close()
