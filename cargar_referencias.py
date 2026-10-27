#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cargar_referencias.py — Carga la tabla referencial `lenguas_referenciales`
(sánscrito, hindi, tibetano) en lexico.db.

PROPÓSITO EXCLUSIVAMENTE REFERENCIAL / CURIOSIDAD:
  * Estas lenguas NO participan en el consenso de `consenso_ganadora.py`
    (el voto ponderado sigue usando solo es/fr/it/pt/ro/ia/eo + latin como
    desempate). Se mantienen en tabla aparte precisamente para eso.
  * Sirven para comparar parecidos tipológicos/PIE con las formas romances.

FORMATO DE DATOS (dict DATA):
  concepto_es : {
    'sa': (forma_transliterada_IAST, escritura_devanagari, etimo_PIE_o_None),
    'hi': (forma_transliterada,        escritura_devanagari, None),
    'bo': (transliteracion_Wylie,      escritura_tibetana,   None),
  }

Criterio de inclusión: solo términos con equivalencia semántica clara y
atestación segura; nada especulativo. Los huecos se dejan vacíos a propósito.
"""
import sqlite3, sys

DB = sys.argv[1] if len(sys.argv) > 1 else "lexico.db"

LENGUA = {'sa': 'sanscrito', 'hi': 'hindi', 'bo': 'tibetano'}

# (forma_transliterada, escritura_original, etimo_PIE_o_None)
SA = lambda f, s, p=None: ('sa', (f, s, p))
HI = lambda f, s:        ('hi', (f, s, None))
BO = lambda f, s:        ('bo', (f, s, None))

DATA = {
  # --- núcleo indoeuropeo: cognados célebres sánscrito ↔ latín/romances ---
  'agua':     [SA('ap-', 'अप्', '*h₂ep- (parcial; lat. aqua < *akweh₂-)'),
               HI('pani', 'पानी'), BO('chu', 'ཆུ')],
  'fuego':    [SA('agni', 'अग्नि', '*h₁n̥gʷnis'),
               HI('ag', 'आग'), BO('me', 'མེ')],
  'noche':    [SA('nakt', 'नक्ति', '*nókʷts (cf. lat. nox, noctis)'),
               HI('rat', 'रात'), BO('mi gam', 'མི་གམ')],
  'sol':      [SA('surya', 'सूर्य'),
               HI('suraj', 'सूरज'), BO('nyi ma', 'ཉི་མ')],
  'luna':     [SA('mas', 'मास्', '*mḗh₁n̥s (cf. lat. mens; romances usan LUNA)'),
               HI('chand', 'चाँद'), BO('zla ba', 'ཟླ་བ')],
  'cielo':    [SA('div/dyaus', 'दिव्', '*dyéws (cf. lat. divus, Iuppiter)'),
               HI('akash', 'आकाश'), BO('nam mkha', 'ནམ་མཁའ')],
  'tierra':   [SA('ksham', 'क्षम्', '*dʰéǵʰōm (parcial; cf. lat. humus)'),
               HI('dharti', 'धरती'), BO('sa', 'ས')],
  'pie':      [SA('pad', 'पाद', '*ped- (cf. lat. pes, pedis — casi idéntico)'),
               HI('pair', 'पैर'), BO('rkang pa', 'རྐང་པ')],
  'corazón':  [SA('hridaya', 'हृदय', '(cf. lat. cor, cordis)'),
               HI('dil', 'दिल'), BO('snying', 'སྙིང')],
  'comer':    [SA('ad/edati', 'एदति', '*h₁ed- (cf. lat. edere)'),
               HI('khana', 'खाना'), BO('za', 'ཟ')],
  'beber':    [SA('pa/pibati', 'पिबति', '*peh₃- (cf. lat. potare/bibere, parcial)'),
               HI('pina', 'पीना'), BO('thung ba', 'ཐུང་བ')],
  'estrella': [SA('star/tArA', 'तारा', '*h₂stḗr (cf. lat. stella < *ster-la)'),
               HI('sitara', 'सितारा'), BO('skar ma', 'སྐར་མ')],
  'día':      [SA('diva', 'दिवस्', '(cf. lat. dies; etimología debatida)'),
               HI('din', 'दिन'), BO('nyi zhag', 'ཉི་ཞག')],
  'leche':    [SA('payas/dugdha', 'दुग्ध', '(cf. lat. lac, lactis — raíces distintas)'),
               HI('dudh', 'दूध'), BO('oma', 'ཨོ་མ')],
  'montaña':  [SA('giri/parvata', 'पर्वत'),
               HI('pahar', 'पहाड़'), BO('ri', 'རི')],
  'rey':      [SA('rajan', 'राजन्', '*h₃rḗǵs (cf. lat. rex, regis — casi idéntico)'),
               HI('raja', 'राजा'), BO('rgyal po', 'རྒྱལ་པོ')],
  'puerta':   [SA('dvára', 'द्वार', '*dʰwer- (cf. lat. foris/fores)'),
               HI('darwaza', 'दरवाज़ा'), BO('sgo', 'སྒོ')],
  'viento':   [SA('váta', 'वात', '*weh₂t- (cf. lat. ventus — casi idéntico)'),
               HI('hawa', 'हवा'), BO('rlung', 'རླུང')],
  'nuevo':    [SA('nava', 'नव', '*néwos (cf. lat. novus — casi idéntico)'),
               HI('naya', 'नया'), BO('gsar pa', 'གསར་པ')],
  'nube':     [SA('megha', 'मेघ'),
               HI('baadal', 'बादल'), BO('sprin', 'སྤྲིན')],
  'nombre':   [SA('naman', 'नामन्', '*h₃nómn̥ (cf. lat. nomen — casi idéntico)'),
               HI('nam', 'नाम'), BO('ming', 'མིང')],
}
# PENDIENTES de incluir cuando existan como concepto en lexico:
#   dos/três/cuatro/cien, dar, ser, sal, nombrar (formas preparadas en el historial).
# NOTA: 'lluvia'/'llover' excluido a propósito: sánscrito varṣa- no es cognado
# de lat. pluviam (*deuk̷- 'humedecer'); darlo como paralelo sería engañoso.


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
      CREATE TABLE IF NOT EXISTS lenguas_referenciales (
        lexico_id   INTEGER REFERENCES lexico(id),
        lengua      TEXT NOT NULL CHECK(lengua IN ('sanscrito','hindi','tibetano')),
        forma       TEXT NOT NULL,
        script_orig TEXT,
        etimo_ie    TEXT,
        nota        TEXT,
        PRIMARY KEY (lexico_id, lengua)
      )""")
    ids = {r[0]: r[1] for r in cur.execute("SELECT id, concepto_es FROM lexico")}
    por_concepto = {v: k for k, v in ids.items()}
    insertadas, omitidas = 0, []
    for concepto, langs in sorted(DATA.items()):
        lid = por_concepto.get(concepto)
        if lid is None:
            omitidas.append(concepto)
            continue
        for code, (forma, script, pie) in langs:
            cur.execute(
                "INSERT OR REPLACE INTO lenguas_referenciales "
                "(lexico_id, lengua, forma, script_orig, etimo_ie, nota) "
                "VALUES (?,?,?,?,?,?)",
                (lid, LENGUA[code], forma, script, pie,
                 'referencial: no participa en el consenso'))
            insertadas += 1
    con.commit()
    print(f"Filas insertadas: {insertadas}")
    print(f"Conceptos del dataset sin fila en lexico: {omitidas or 'ninguno'}")
    # resumen por lengua
    for l, n in cur.execute("SELECT lengua, COUNT(*) FROM lenguas_referenciales GROUP BY lengua"):
        print(f"  {l}: {n}")

    # Informe comparativo: parecido del sánscrito con las formas romances
    import unicodedata as _u
    def norm(s):
        if not s: return ''
        s = _u.normalize('NFD', s.lower())
        return ''.join(c for c in s if _u.category(c) != 'Mn')
    def lev(a, b):
        m, n = len(a), len(b)
        d = list(range(n + 1))
        for i in range(1, m + 1):
            prev, d[0] = d[0], i
            for j in range(1, n + 1):
                cur2 = d[j]
                d[j] = min(d[j] + 1, d[j-1] + 1, prev + (a[i-1] != b[j-1]))
                prev = cur2
        return d[n]
    print("\n=== Parecido sánscrito vs romance (distancia Levenshtein / longitud) ===")
    q = """SELECT l.concepto_es, l.es, l.it, l.fr, l.pt, l.ro, l.latin, r.forma, r.etimo_ie
           FROM lenguas_referenciales r JOIN lexico l ON l.id = r.lexico_id
           WHERE r.lengua='sanscrito' ORDER BY l.concepto_es"""
    for row in cur.execute(q):
        concepto, es, it, fr, pt, ro, latin, sa_forma, pie = row
        base = sa_forma.split('/')[0].replace('-', '')
        sims = []
        for nombre, val in (('es', es), ('it', it), ('fr', fr), ('pt', pt),
                           ('ro', ro), ('lat', latin)):
            if val and val != '—':
                v = norm(val)
                dist = lev(norm(base), v)
                sim = max(0.0, 1 - dist / max(len(v), len(base), 1))
                sims.append((sim, nombre))
        sims.sort(reverse=True)
        top = ', '.join(f"{n}={s:.2f}" for s, n in sims[:3])
        flag = ' <== PARALELO' if sims and sims[0][0] >= 0.6 else ''
        print(f"{concepto:12s} sa={sa_forma:18s} {top}{flag}")
    con.close()


if __name__ == "__main__":
    main()
