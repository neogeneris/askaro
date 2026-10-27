#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
askaro_romances.py — Fase 1 (dry-run) para askaro_lexicon (1.404 términos).

Objetivo del usuario: replicar en askaro_lexicon lo hecho con lexico:
  columnas romances (fr, it, pt, ro), interlingua (ia), esperanto (eo),
  y luego un sistema de consenso que produzca "termino_propuesto".

Este script NO escribe en la BD todavía. Hace:
  1. ALTER TABLE (simulado) -> añade columnas fr/it/pt/ro/ia/eo/latin_vulgar/
     termino_propuesto/consenso_lenguas a askaro_lexicon.
  2. Rellena las columnas desde 3 fuentes (sin inventar):
       A. join exacto con lexico.concepto_es (fuente='lexico')
       B. traducciones directas conocidas para el núcleo NSM/funcional (fuente='directa')
       C. derivación por reglas desde el étimo latino de origen_etimologia
          hacia ia/eo (fuente='derivada', marcado como propuesta)
  3. Aplica votación ponderada estilo consenso_ganadora.py (bloques de raíz
     normalizada, MIN_VOTOS=3, español gana solo sin bloque) y calcula
     termino_propuesto + n_lenguas_consenso.
  4. Emite informe CSV (askaro_consenso_dryrun.csv) y estadísticas de cobertura.

Uso:  python askaro_romances.py            # dry-run
      python askaro_romances.py --apply    # aplica ALTER+UPDATE a lexico.db
"""
import sqlite3, re, unicodedata, sys, csv
from collections import defaultdict

DB = 'lexico.db'
MIN_VOTOS = 3

NUEVAS_COLS = ['fr', 'it', 'pt', 'ro', 'ia', 'eo', 'latin_vulgar',
               'fuente_columnas', 'termino_propuesto', 'n_consenso']

# ---------------------------------------------------------------- helpers
def norm(s):
    if not s: return ''
    s = unicodedata.normalize('NFD', s.strip().lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'\([^)]*\)', '', s)          # quitar glosas "(genérico)"
    s = re.sub(r'[^a-z ]', ' ', s)
    return s.strip()

def root(form):
    """raíz comparable: quita desinencias flexivas típicas."""
    r = norm(form).replace(' ', '')
    for suf in ('as','os','es','ae','am','um','us','i','o','a','e'):
        if len(r) > 4 and r.endswith(suf):
            return r[:-len(suf)]
    return r

def similar(a, b):
    ra, rb = root(a), root(b)
    if not ra or not rb: return 0.0
    if ra == rb: return 1.0
    # distancia de Levenshtein simple
    x, y = sorted((ra, rb), key=len)
    prev = list(range(len(y)+1))
    for i, cx in enumerate(x, 1):
        cur = [i]
        for j, cy in enumerate(y):
            cur.append(min(prev[j+1]+1, cur[j]+1, prev[j] + (cx != cy)))
        prev = cur
    return 1 - prev[len(y)] / max(len(x), len(y))

# ---------------------------------------------------------------- fuentes
def load_lex_map(cur):
    m = {}
    for row in cur.execute("SELECT concepto_es, es, fr, it, pt, ro, ia, eo, latin, latin_vulgar FROM lexico"):
        k = norm(row[0])
        if k and k not in m:
            m[k] = {'fr': row[2], 'it': row[3], 'pt': row[4], 'ro': row[5],
                    'ia': row[6], 'eo': row[7], 'latin': row[8], 'lv': row[9]}
    return m

# Traducciones directas verificadas para el núcleo funcional/NSM que falta
# en lexico. Forma base: fr / it / pt / ro / ia / eo  (solo donde hay palabra
# estándar inequívoca; vacío si no).
DIRECTAS = {
 'yo':      dict(fr='moi',   it='me',    pt='eu',    ro='mă',    ia='me',    eo='mi'),
 'tu':      dict(fr='toi',   it='te',    pt='tu',    ro='tu',    ia='te',    eo='vi'),
 'el':      dict(fr='lui',   it='lui',   pt='ele',   ro='el',    ia='ille',  eo='li'),
 'ella':    dict(fr='elle',  it='lei',   pt='ela',   ro='ea',    ia='illa',  eo='ŝi'),
 'nosotros':dict(fr='nous',  it='noi',   pt='nós',   ro='noi',   ia='nos',   eo='ni'),
 'ustedes': dict(fr='vous',  it='voi',   pt='vocês', ro='voi',   ia='vos',   eo='ili'),
 'ellos':   dict(fr='eux',   it='loro',  pt='eles',  ro='ei',    ia='illes', eo='ili'),
 'nombre':  dict(fr='nom',   it='nome',  pt='nome',  ro='nume',  ia='nomine',eo='nomo'),
 'aire':    dict(fr='air',   it='aria',  pt='ar',    ro='aer',   ia='aere',  eo='aero'),
 'ser':     dict(fr='être',  it='essere',pt='ser',   ro='a fi',  ia='esser', eo='esti'),
 'tener':   dict(fr='avoir', it='avere', pt='ter',   ro='a avea',ia='haber', eo='havi'),
 'hacer':   dict(fr='faire', it='fare',  pt='fazer', ro='a face',ia='facere',eo='fari'),
 'ir':      dict(fr='aller', it='andare',pt='ir',    ro='a merge',ia='ir',   eo='iri'),
 'venir':   dict(fr='venir', it='venire',pt='vir',   ro='a veni',ia='venir', eo='veni'),
 'decir':   dict(fr='dire',  it='dire',  pt='dizer', ro='a spune',ia='dicere',eo='diri'),
 'dar':     dict(fr='donner',it='dare',  pt='dar',   ro='a da',  ia='dar',   eo='doni'),
 'saber':   dict(fr='savoir',it='sapere',pt='saber', ro='a ști', ia='sapere',eo='scii'),
 'querer':  dict(fr='vouloir',it='volere',pt='querer',ro='a vrea',ia='voler', eo='voli'),
 'poder':   dict(fr='pouvoir',it='potere',pt='poder',ro='a putea',ia='poter',eo='posi'),
 'bueno':   dict(fr='bon',   it='buono', pt='bom',   ro='bun',   ia='bon',   eo='bona'),
 'pequeno': dict(fr='petit', it='piccolo',pt='pequeno',ro='mic', ia='parve', eo='malgranda'),
 'nuevo':   dict(fr='nouveau',it='nuovo',pt='novo',  ro='nou',   ia='nove',  eo='nova'),
 'grande':  dict(fr='grand', it='grande',pt='grande',ro='mare',  ia='grande',eo='granda'),
 'caliente':dict(fr='chaud', it='caldo', pt='quente',ro='cald',  ia='calide',eo='varma'),
 'frio':    dict(fr='froid', it='freddo',pt='frio',  ro='rece',  ia='frigid',eo='malvarma'),
 'noche':   dict(fr='nuit',  it='notte', pt='noite', ro='noapte',ia='nocte', eo='nokto'),
 'dia':     dict(fr='jour',  it='giorno',pt='dia',   ro='zi',    ia='die',   eo='tago'),
 'agua':    dict(fr='eau',   it='acqua', pt='água',  ro='apă',   ia='aqua',  eo='akvo'),
 'madre':   dict(fr='mère',  it='madre', pt='mãe',   ro='mamă',  ia='matre', eo='patrino'),
 'padre':   dict(fr='père',  it='padre', pt='pai',   ro='tată',  ia='patre', eo='patrino'),
 'hermano': dict(fr='frère', it='fratello',pt='irmão',ro='frate',ia='fratre',eo='frato'),
 'hermana': dict(fr='sœur',  it='sorella',pt='irmã', ro='soră',  ia='soror', eo='fratin'),
 'mujer':   dict(fr='femme', it='donna', pt='mulher',ro='femeie',ia='femina',eo='femina'),
 'hombre':  dict(fr='homme', it='uomo',  pt='homem', ro='bărbat',ia='homine',eo='viro'),
 'uno':     dict(fr='un',    it='uno',   pt='um',    ro='unu',   ia='un',    eo='unu'),
 'dos':     dict(fr='deux',  it='due',   pt='dois',  ro='doi',   ia='duo',   eo='du'),
 'tres':    dict(fr='trois', it='tre',   pt='três',  ro='trei',  ia='tres',  eo='tri'),
 'cuatro':  dict(fr='quatre',it='quattro',pt='quatro',ro='patru',ia='quattuor',eo='kvar'),
 'cien':    dict(fr='cent',  it='cento', pt='cem',   ro='sută',  ia='cente', eo='cent'),
}
# corregir entradas escritas con trampa sintáctica arriba
DIRECTAS['ser']   = dict(fr='être', it='essere', pt='ser', ro='a fi', ia='esser', eo='esti')
DIRECTAS['padre'] = dict(fr='père', it='padre', pt='pai', ro='tată', ia='patre', eo='patrino')

# ------------------------------------------------- derivación latín -> ia/eo
MACRON = str.maketrans({'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u'})

def extraer_etimo(txt):
    """Extrae el étimo latino de origen_etimologia. Formas típicas:
       'ego (lat.)', 'persōna (lat.)', 'mors, mortis (lat.)',
       'lat. vulg. CAUSA(M) > ...', 'focus (lat. vulg.)', 'āēr (gr./lat.)'."""
    if not txt: return None
    # griego politonico -> latinizar por NFD+stripping (vía tablas estándar es compleja;
    # se transcribe el alfabeto y se quitan macrón/espíritu/aspiración)
    GR_MAP = {'α':'a','β':'b','γ':'g','δ':'d','ε':'e','ζ':'z','η':'e','θ':'th','ι':'i','κ':'k','λ':'l','μ':'m','ν':'n','ξ':'x','ο':'o','π':'p','ρ':'r','σ':'s','ς':'s','τ':'t','υ':'y','φ':'f','χ':'ch','ψ':'ps','ω':'o'}
    def latiniza_g(s):
        t = unicodedata.normalize('NFD', s.lower())
        t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
        t = t.replace('᾿','').replace(chr(0x1fbd),'').replace('·','')
        return ''.join(GR_MAP.get(c, c if ord(c) < 0x345 else '') for c in t)
    # token(es) inmediatamente antes de una glosa (lat.)/(lat vulg)
    m = re.search(r'([^>;]+?)\s*\((?:[^)]*(?:lat|gr)[^)]*)\)', txt, re.I)
    if m:
        cand = m.group(1).strip().split(',')[0].strip()   # 'mors, mortis' -> 'mors'
        cand = re.sub(r'^(?:lat\.?\s*(?:vulg\.?)?\s*)', '', cand, flags=re.I).strip()
        if re.search(r'[\u0370-\u03ff]', cand): cand = latiniza_g(cand)
        cand = cand.split('>')[-1].strip() if '<' in cand and '>' in cand else cand
        parts = [p for p in cand.split() if p.lower() not in ('ecce','ad','de','in','ex','cum','a','ab')]
        cand = ' '.join(parts) if parts else cand
        if len(cand) >= 3 and re.fullmatch(r'[A-Za-z\u00c0-\u024F\u1e00-\u1eff][A-Za-z\u00c0-\u024F\u1e00-\u1eff .\u0300-\u036f+-]*', cand):
            if len(cand.split()) > 1:
                cand = max(cand.split(), key=len)   # 'ecce hoc'->'hoc', 'ambulare via'->'ambulare'
            return cand
    # MAYÚSCULAS etimológicas estilo lexico: 'CAUSA(M)'
    m = re.search(r'\b([AĀĒĪŌŪ][A-ZĀĒĪŌŪ]{2,}[A-ZĀĒĪŌŪ])(?:\(M\))?\b', txt)
    if m: return m.group(1)
    return None

VOWELMAC = {'a','e','i','o','u','y'}
def stem_latino(w):
    """raíz latina: normaliza macrones (NFD) y quita desinencias comunes."""
    w = unicodedata.normalize('NFD', w.lower().strip('. ()'))
    w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    w = re.sub(r'\(m\)$', '', w)
    for suf in ('us','um','am','ar','eri','or','ore','is','es','em','ae','io','ion','tatis','tas'):
        if len(w) > len(suf)+2 and w.endswith(suf):
            return w[:-len(suf)]
    return re.sub(r'i$', '', w)

def lat_a_ia(l):
    w = stem_latino(l)
    w = w.replace('ph','f').replace('ae','e').replace('oe','e')
    w = re.sub(r'ct$', 't', w)          # nocte -> nocte (ia mantiene ct en culto; simple)
    return w + ('e' if not w.endswith(('a','e','i','o','u')) else '')

def lat_a_eo(l):
    w = stem_latino(l)
    w = w.replace('ph','f').replace('qu','k').replace('c','k').replace('g','g')
    w = re.sub(r'sk','s', w)
    if not w.endswith(('a','e','i','o','u')): w += 'o'
    return w

# ---------------------------------------------------------------- consenso
LENGUAS_BLOQUE = ['fr', 'it', 'pt', 'ro', 'ia', 'eo', 'es']
PREF = ['ia', 'eo', 'it', 'pt', 'ro', 'fr', 'es']

def elegir_ganadora(vals):
    """vals: dict lengua->forma (no vacías). Devuelve (forma, n_votos, lengua)."""
    grupos = defaultdict(list)
    for lg, f in vals.items():
        if f: grupos[root(f)].append((lg, f))
    bloques = sorted(grupos.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    best_form = best_n = best_lang = None
    for r, members in bloques:
        n = len(members)
        if n >= MIN_VOTOS:
            forms = {lg: f for lg, f in members}
            lang = next(l for l in PREF if l in forms)
            cand = forms[lang]
            if best_n is None or n > best_n:
                best_form, best_n, best_lang = cand, n, lang
    if best_form:
        return best_form, best_n, best_lang
    # sin bloque: fallback español (documentado, no sesgo silencioso)
    if vals.get('es'):
        return vals['es'], 1, 'es-sin-bloque'
    return None, 0, None

# ---------------------------------------------------------------- main
def main(apply=False):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    lexmap = load_lex_map(cur)

    rows = list(cur.execute("""SELECT id, codigo, español, ingles, origen_etimologia
                               FROM askaro_lexicon ORDER BY id"""))
    stats = defaultdict(int)
    out = []
    for rid, cod, esp, eng, etim in rows:
        vals = {'es': esp}
        deriv = {}
        fuente = None
        k = norm(esp)
        if k in lexmap:
            vals.update({l: lexmap[k][l] for l in ('fr','it','pt','ro','ia','eo')})
            if lexmap[k].get('lv'): vals['latin_vulgar'] = lexmap[k]['lv']
            fuente = 'lexico'; stats['via_lexico'] += 1
        elif k in DIRECTAS:
            vals.update(DIRECTAS[k]); fuente = 'directa'; stats['via_directa'] += 1
        else:
            e = extraer_etimo(etim)
            if e:
                # NO votan: son formas mecánicas del propio étimo (circularidad)
                deriv = {'ia': lat_a_ia(e), 'eo': lat_a_eo(e)}
                fuente = f'derivada<{e}'; stats['via_derivacion'] += 1
            else:
                fuente = 'sin-fuente'; stats['sin_fuente'] += 1
        gan, n, lang = elegir_ganadora(vals)   # solo con datos attestados
        filled = sum(1 for l in LENGUAS_BLOQUE if vals.get(l))
        for k2, v2 in list(deriv.items()):
            vals.setdefault(k2, v2)
        out.append(dict(id=rid, codigo=cod, español=esp, fuente=fuente,
                        fr=vals.get('fr',''), it=vals.get('it',''), pt=vals.get('pt',''),
                        ro=vals.get('ro',''), ia=vals.get('ia',''), eo=vals.get('eo',''),
                        latin_vulgar=vals.get('latin_vulgar',''),
                        n_llenas=filled, termino_propuesto=gan or '',
                        n_consenso=n, gana=lang or ''))
        stats[f'llenas_{filled}' if filled<=6 else 'llenas_7'] += 1

    with open('askaro_consenso_dryrun.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)

    print(f"filas procesadas: {len(out)}")
    for k in sorted(stats): print(f"  {k}: {stats[k]}")
    cons = sum(1 for o in out if o['n_consenso'] >= MIN_VOTOS)
    print(f"con bloque>= {MIN_VOTOS}: {cons}")
    if apply:
        existing = {r[1] for r in cur.execute("PRAGMA table_info(askaro_lexicon)")}
        for c in NUEVAS_COLS:
            if c not in existing:
                cur.execute(f"ALTER TABLE askaro_lexicon ADD COLUMN {c} TEXT")
        for o in out:
            cur.execute("""UPDATE askaro_lexicon SET fr=?,it=?,pt=?,ro=?,ia=?,eo=?,
                           latin_vulgar=?,fuente_columnas=?,termino_propuesto=?,n_consenso=? WHERE id=?""",
                        (o['fr'],o['it'],o['pt'],o['ro'],o['ia'],o['eo'],
                         o['latin_vulgar'],o['fuente'],o['termino_propuesto'],o['n_consenso'],o['id']))
        con.commit()
        print("APLICADO.")
    else:
        print("(dry-run: no se escribió en la BD)")
    con.close()

if __name__ == '__main__':
    main(apply='--apply' in sys.argv)
