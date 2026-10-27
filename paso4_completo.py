#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASO 4 COMPLETO — poblar lexico.db resolviendo conflictos, revisando emojis
no estándar y aplicando fallback CLDR.

Fuentes:
  FUENTE 1 (primaria): sintesio.db tabla `imports` (concepto_espanol, glifo).
    - 160 conceptos con emoji canónico -> nota "emoji desde sintesio.db".
    - Emojis no fully-qualified (ancla/velero/iglesia/ferry) -> se REEMPLAZAN
      por su equivalente estándar añadiendo U+FE0F (variación de presentación
      de emoji; el codepoint base es idéntico, no rompe ningún par).
  FUENTE 2 (fallback): búsqueda CLDR/Unicode para los 46 conceptos de imports
    sin glifo + 71 conceptos extra solo presentes en la lista curada CLDR.

Colisiones:
  - Prioridad absoluta: sintesio.db gana siempre; el perdedor busca 2º/3º
    candidato libre; si no hay, más cercano + nota.
  - Toda resolución nueva se registra en emoji_colisiones
    (resolucion='especifico_gana' cuando gana el referente literal/sintesio,
     'segundo_candidato' cuando el perdedor migra a otro emoji).
  - Candidatos (ganador + alternativos) se guardan en emoji_candidatos.

Requiere pysqlite3 (SQLite >= 3.41) porque lexico.db tiene triggers con ||
en RAISE que el parser 3.40.x rechaza.
"""
import os
import re
import sys
import time
import sqlite3          # stdlib: leer sintesio.db / askaro_lexico.db
from collections import Counter

try:
    import pysqlite3 as sqlx   # SQLite 3.51.x: escribe lexico.db
except ImportError:
    print("ERROR: falta pysqlite3-binary -> pip install pysqlite3-binary")
    sys.exit(1)

T0 = time.time()
SINTESIO_DB = "sintesio.db"
LEXICO_DB   = "lexico.db"

assert os.path.exists(SINTESIO_DB), "falta sintesio.db"
assert os.path.exists(LEXICO_DB),   "falta lexico.db"

# ============================================================================
# Lista curada de candidatos CLDR tomada del paso anterior (paso4_emoji.py).
# Formato: (emoji, nombre_oficial_unicode, codepoint, puntuacion)
# Puntuación 0-100 = representatividad 40% + frecuencia 25% + iconicidad 20%
#                    + unicidad 10% + estabilidad 5%.
# ============================================================================
_src = open("paso4_emoji.py", encoding="utf-8").read()
_ns = {}
exec(re.search(r"CANDIDATOS_CLDR = \{.*?\n\}", _src, re.S).group(0), _ns)
CANDIDATOS_CLDR = _ns["CANDIDATOS_CLDR"]

# ---------------------------------------------------------------------------
# Ampliación de candidatos (búsqueda CLDR es/en + Unicode Full Emoji List)
# para: (a) los 46 conceptos de imports sin glifo, (b) segundos candidatos de
# conceptos mono-candidato, (c) alternativas libres ante colisión.
# ---------------------------------------------------------------------------
EXTRA_CANDS = {
    # --- conceptos de imports SIN glifo (los 33 no cubiertos ya) ---------
    "agua":      [("💧", "DROPLET", "U+1F4A7", 96), ("🌊", "WATER WAVE", "U+1F30A", 82)],
    "fuego":     [("🔥", "FIRE", "U+1F525", 98), ("🕯️", "CANDLE", "U+1F56F FE0F", 75)],
    "tierra":    [("🌍", "GLOBE EUROPE-AFRICA", "U+1F30D", 95), ("🪨", "ROCK", "U+1FAA8", 60)],
    "mar":       [("🌊", "WATER WAVE", "U+1F30A", 96), ("⛵", "SAILBOAT", "U+26F5 FE0F", 78)],
    "sol":       [("☀️", "SUN", "U+2600 FE0F", 97), ("🌞", "SUN WITH FACE", "U+1F31E", 88)],
    "luna":      [("🌙", "CRESCENT MOON", "U+1F319", 96), ("🌕", "FULL MOON", "U+1F315", 85)],
    "luz":       [("💡", "ELECTRIC LIGHT BULB", "U+1F4A1", 92), ("🔆", "BRIGHTNESS BUTTON", "U+1F506", 70)],
    "noche":     [("🌙", "CRESCENT MOON", "U+1F319", 92), ("🌑", "NEW MOON", "U+1F311", 80)],
    "piedra":    [("🪨", "ROCK", "U+1FAA8", 96), ("⛰️", "MOUNTAIN", "U+26F0 FE0F", 70)],
    "rey":       [("🤴", "PRINCE", "U+1F934", 85), ("👑", "CROWN", "U+1F451", 82)],
    "reina":     [("👸", "PRINCESS", "U+1F478", 92), ("👑", "CROWN", "U+1F451", 75)],
    "amor":      [("❤️", "HEART", "U+2764 FE0F", 95), ("💞", "REVOLVING HEARTS", "U+1F49E", 82)],
    "odio":      [("💢", "ANGER SYMBOL", "U+1F4A2", 82), ("😠", "ANGRY FACE", "U+1F620", 80)],
    "libertad":  [("🗽", "STATUE OF LIBERTY", "U+1F5FD", 88), ("🕊️", "DOVE OF PEACE", "U+1F54A FE0F", 72)],
    "verdad":    [("✅", "CHECK MARK BUTTON", "U+2705", 80), ("💡", "ELECTRIC LIGHT BULB", "U+1F4A1", 68)],
    "justicia":  [("⚖️", "SCALES", "U+2696 FE0F", 96)],
    "música":    [("🎵", "MUSICAL NOTE", "U+1F3B5", 96), ("🎶", "MULTIPLE MUSICAL NOTES", "U+1F3B6", 88)],
    "escuela":   [("🏫", "SCHOOL", "U+1F3EB", 96)],
    "carta":     [("✉️", "ENVELOPE", "U+2709 FE0F", 94), ("📄", "PAGE FACING UP", "U+1F4C4", 78)],
    "correr":    [("🏃", "RUNNER", "U+1F3C3", 95)],
    "volar":     [("🕊️", "DOVE OF PEACE", "U+1F54A FE0F", 84), ("✈️", "AIRPLANE", "U+2708 FE0F", 80)],
    "cantar":    [("🎤", "MICROPHONE", "U+1F3A4", 92), ("🎶", "MULTIPLE MUSICAL NOTES", "U+1F3B6", 80)],
    "contar":    [("🔢", "INPUT NUMBERS", "U+1F522", 88), ("➕", "HEAVY PLUS SIGN", "U+2795", 72)],
    "halar":     [("🪝", "HOOK", "U+1FA9D", 72), ("🧲", "MAGNET", "U+1F9F2", 70)],
    "llenar":    [("🥣", "BOWL WITH SPOON", "U+1F963", 75), ("🫗", "POURING LIQUID", "U+1FAD7", 82)],
    "roer":      [("🐀", "RAT", "U+1F400", 80), ("🦷", "TOOTH", "U+1F9B7", 68)],
    "aprender":  [("📚", "BOOKS", "U+1F4DA", 88), ("🧠", "BRAIN", "U+1F9E0", 84)],
    "izquierdo": [("🫲", "LEFTWARD HAND", "U+1FAF2", 92), ("↔️", "LEFT RIGHT ARROW", "U+2194 FE0F", 75)],
    "ciego":     [("🦯", "WHITE CANE", "U+1F9AF", 90), ("🕶️", "SUNGLASSES", "U+1F576 FE0F", 70)],
    "codo":      [("🦴", "BONE", "U+1F9B4", 78), ("💪", "BICEPED ARM", "U+1F4AA", 74)],
    "muñeca":    [("🦴", "BONE", "U+1F9B4", 70), ("💪", "BICEPED ARM", "U+1F4AA", 78)],
    "ceniza":    [("🌋", "VOLCANO", "U+1F30B", 68), ("🏺", "AMPHORA", "U+1F3FA", 55)],
    "espina":    [("🌵", "CACTUS", "U+1F335", 88), ("🥷", "NINJA", "U+1F977", 50)],
    "raíz":      [("🌱", "SEEDLING", "U+1F331", 80), ("🥕", "CARROT", "U+1F955", 72)],
    "banca":     [("🏦", "BANK", "U+1F3E6", 96), ("🪑", "CHAIR", "U+1FA91", 60)],
    "ciudad":    [("🏙️", "CITYSCAPE", "U+1F3D9 FE0F", 95), ("🌆", "CITYSCAPE AT DUSK", "U+1F306", 88)],
    "historia":  [("📜", "SCROLL", "U+1F4DC", 90), ("📖", "OPEN BOOK", "U+1F4D6", 88)],
    "guerra":    [("⚔️", "CROSSED SWORDS", "U+2694 FE0F", 95), ("🛡️", "SHIELD", "U+1F6E1 FE0F", 85)],
    "paz":       [("🕊️", "DOVE OF PEACE", "U+1F54A FE0F", 92), ("☮️", "PEACE SYMBOL", "U+262E FE0F", 90)],
    "comer":     [("🍽️", "FORK AND KNIFE WITH PLATE", "U+1F37D FE0F", 88), ("😋", "FACE SAVOURING DELICIOUS FOOD", "U+1F60B", 80)],
    "beber":     [("🥤", "CUP WITH STRAW", "U+1F964", 90), ("🚰", "POTABLE WATER", "U+1F6B0", 75)],
    "casa":      [("🏠", "HOUSE BUILDING", "U+1F3E0", 98), ("🏡", "HOUSE WITH GARDEN", "U+1F3E1", 90)],
    "camino":    [("🛤️", "RAILWAY TRACK", "U+1F6E4 FE0F", 85), ("🛣️", "MOTORWAY", "U+1F6E3 FE0F", 82)],
    "puerta":    [("🚪", "DOOR", "U+1F6AA", 98)],
    "ventana":   [("🪟", "WINDOW", "U+1FA9F", 97)],
    # --- segundos candidatos CLDR para conceptos mono-candidato ----------
    "mujer":     [("👤", "BUST IN SILHOUETTE", "U+1F464", 70)],
    "hombre":    [("🚹", "MEN'S ROOM", "U+1F6B9", 68)],
    "niño":      [("🧒", "CHILD", "U+1F9D2", 88)],
    "pie":       [("🦵", "LEG", "U+1F9B5", 70)],
    "ojo":       [("👀", "EYES", "U+1F440", 85)],
    "boca":      [("👅", "TONGUE", "U+1F445", 72)],
    "lluvia":    [("☔", "UMBRELLA WITH RAIN DROPS", "U+2614 FE0F", 88)],
    "oveja":     [("🐏", "RAM", "U+1F40F", 75)],
    "pez":       [("🐠", "TROPICAL FISH", "U+1F420", 85)],
    "pan":       [("🥐", "CROISSANT", "U+1F950", 80)],
    "leche":     [("🍼", "BABY BOTTLE", "U+1F37C", 70)],
    "huevo":     [("🍳", "COOKING", "U+1F373", 78)],
    "manzana":   [("🍏", "GREEN APPLE", "U+1F34F", 88)],
    "cama":      [("🛌", "PERSON IN BED", "U+1F6CC", 75)],
    "mesa":      [("🍽️", "FORK AND KNIFE WITH PLATE", "U+1F37D FE0F", 90), ("🪵", "WOOD", "U+1AB5", 55)],
    "aldea":     [("🏘️", "HOUSES", "U+1F3D8 FE0F", 85)],
    "muerte":    [("⚰️", "COFFIN", "U+26B0 FE0F", 88)],
    "corazón":   [("💖", "SPARKLING HEART", "U+1F496", 85)],
    "libro":     [("📚", "BOOKS", "U+1F4DA", 90)],
    "hablar":    [("💬", "SPEECH BALLOON", "U+1F4AC", 88)],
    "ver":       [("👁️", "EYE", "U+1F441 FE0F", 85)],
    "oir":       [("🦻", "EAR WITH HEARING AID", "U+1F9BB", 75)],
    "pequeño":   [("🤏", "PINCHING HAND", "U+1F90F", 80)],
    "caliente":  [("🌡️", "THERMOMETER", "U+1F321 FE0F", 85)],
    "frio":      [("❄️", "SNOWFLAKE", "U+2744 FE0F", 90)],
    "limpio":    [("🧽", "SPONGE", "U+1F9FD", 85)],
    "empujar":   [("🤚", "RAISED BACK OF HAND", "U+1F91A", 72)],
    # --- ampliación fase población: segundos candidatos para que NINGÚN
    #     concepto quede bloqueado (regla: el específico gana; el perdedor
    #     migra a su segundo candidato, nunca se duplica el emoji) ----------
    "marmota":   [("🦫", "BEAVER", "U+1F9AB", 78), ("🐿️", "CHIPMUNK", "U+1F43F FE0F", 95)],
    "balanza":   [("🌗", "LAST QUARTER MOON SYMBOL", "U+1F317", 62), ("⚖️", "SCALES", "U+2696 FE0F", 96)],
    "vecindario":[("🏘️", "HOUSES", "U+1F3D8 FE0F", 85), ("🏘", "HOUSES", "U+1F3D8", 60)],
    "ola":       [("💫", "DIZZY SYMBOL", "U+1F4AB", 55), ("🌊", "WATER WAVE", "U+1F30A", 95)],
    "hielo":     [("🧊", "ICE", "U+1F9CA", 96), ("❄️", "SNOWFLAKE", "U+2744 FE0F", 70)],
    "nieve":     [("❄️", "SNOWFLAKE", "U+2744 FE0F", 96), ("☃️", "SNOWMAN", "U+2603 FE0F", 82)],
    "tulipan":   [("🌷", "TULIP", "U+1F337", 96), ("🌸", "CHERRY BLOSSOM", "U+1F338", 80)],
    "hibisco":   [("🌺", "HIBISCUS", "U+1F33A", 96), ("🪷", "LOTUS", "U+1FAB7", 84)],
    "gota":      [("💧", "DROPLET", "U+1F4A7", 96), ("🫗", "POURING LIQUID", "U+1FAD7", 60)],
    "agua":      [("💧", "DROPLET", "U+1F4A7", 96), ("🌊", "WATER WAVE", "U+1F30A", 82), ("🚰", "POTABLE WATER", "U+1F6B0", 70)],
    "justicia":  [("⚖️", "SCALES", "U+2696 FE0F", 96), ("👨‍⚖️", "JUDGE", "U+1F9D1 200D 2696 FE0F", 84)],
    "ardilla":   [("🐿️", "CHIPMUNK", "U+1F43F FE0F", 95), ("🐹", "HAMSTER FACE", "U+1F439", 70)],
    "flor":      [("💐", "BOUQUET", "U+1F490", 88), ("🌸", "CHERRY BLOSSOM", "U+1F338", 90), ("🌺", "HIBISCUS", "U+1F33A", 80), ("🌷", "TULIP", "U+1F337", 92)],
    "frio":      [("🥶", "FACE SCREAMING IN FEAR", "U+1F976", 88), ("❄️", "SNOWFLAKE", "U+2744 FE0F", 90), ("🧊", "ICE", "U+1F9CA", 92)],
    "aldea":     [("🏡", "HOUSE WITH GARDEN", "U+1F3E1", 88), ("🏘️", "HOUSES", "U+1F3D8 FE0F", 85), ("🛖", "HUT", "U+1F6D6", 86)],
    "historia":  [("📜", "SCROLL", "U+1F4DC", 90), ("📖", "OPEN BOOK", "U+1F4D6", 88), ("🏛️", "CLASSICAL BUILDING", "U+1F3DB FE0F", 80)],
    "libro":     [("📖", "OPEN BOOK", "U+1F4D6", 95), ("📚", "BOOKS", "U+1F4DA", 90), ("📕", "CLOSED BOOK", "U+1F4D5", 82)],
    "volar":     [("🪽", "WING", "U+1FABD", 74), ("✈️", "AIRPLANE", "U+2708 FE0F", 80), ("🕊️", "DOVE OF PEACE", "U+1F54A FE0F", 84)],
}
# quitar marcadores inválidos
for k in list(EXTRA_CANDS):
    EXTRA_CANDS[k] = [t for t in EXTRA_CANDS[k] if t[1]]

def clist(k):
    """Lista de candidatos ordenada por puntuación desc, deduplicada."""
    base = list(CANDIDATOS_CLDR.get(k, [])) + list(EXTRA_CANDS.get(k, []))
    seen, out = set(), []
    for tup in sorted(base, key=lambda x: -x[3]):
        o = tup[0].strip()
        if o not in seen:
            seen.add(o); out.append(tup)
    return out

# ============================================================================
# PASO 2 — revisión de los 4 emojis no estándar de sintesio.db
# ============================================================================
# ancla ⚓ U+2693, velero ⛵ U+26F5, iglesia ⛪ U+26EA, ferry ⛴ U+26F4:
# todos tienen equivalente fully-qualified estándar = base + U+FE0F.
REEMPLAZOS_NO_ESTANDAR = {
    "ancla":   ("\u2693", "\u2693\ufe0f"),
    "velero":  ("\u26f5", "\u26f5\ufe0f"),
    "iglesia": ("\u26ea", "\u26ea\ufe0f"),
    "ferry":   ("\u26f4", "\u26f4\ufe0f"),
}

def es_no_estandar(e):
    return any(0x2000 <= ord(ch) <= 0x2BFF for ch in e) and "\ufe0f" not in e

# ============================================================================
# Carga de fuentes
# ============================================================================
cs = sqlite3.connect(SINTESIO_DB)
imports = cs.execute(
    "SELECT concepto_espanol, es, fr, it, pt, ro, interlingua, esperanto, "
    "etimologia, clase_gramatical, n_universal, consenso_pct, variantes, "
    "nota_ranking, glifo FROM imports").fetchall()
cs.close()

formas, metadatos, glifos = {}, {}, {}
for r in imports:
    k = r[0]
    formas[k] = tuple(x if x else "—" for x in r[1:8])   # es..eo
    etim = (r[8] or "").replace("'", "")
    m = re.search(r"\b(?:lat\.|gr\.|germ\.)\s*\*?([A-ZĀ-ŽŎŎ][A-Za-zĀ-žŎ]{2,})", etim)
    latin = "—"; 
    m2 = re.findall(r"[A-ZĀ-Ž][A-ZÄŒŞŢa-zäışţ]{3,}(?:\([MU]\))?", etim)
    if m2:
        cand = m2[0]
        latin = cand.upper().replace("(", "").replace(")", "")
    metadatos[k] = dict(clase=r[9], nuniv=r[10], pct=r[11], variantes=r[12],
                        nota_ranking=r[13], latin=latin)
    g = (r[14] or "").strip()
    if g:
        glifos[k] = g

sintesio_con_emoji = dict(glifos)                     # 160 (FUENTE 1)
todos_imports = {r[0] for r in imports}               # 206
sin_glifo = todos_imports - set(glifos)               # 46

# inglés: askaro_lexico.db tiene columna `ingles` por término español
EN = {}
if os.path.exists("askaro_lexico.db"):
    ca = sqlite3.connect("askaro_lexico.db")
    for esp, eng in ca.execute("SELECT espanol, ingles FROM lexico WHERE ingles IS NOT NULL AND ingles<>''"):
        for w in [x.strip().lower() for x in str(esp).split("/")]:
            EN.setdefault(w, eng.strip())
    ca.close()

# ============================================================================
# PASO 1/3 — asignación con prioridad de fuentes y resolución de colisiones
# ============================================================================
chosen = {}            # concepto -> emoji final
cand_by_concept = {}   # concepto -> lista de candidatos usados
collisions = []        # filas nuevas para emoji_colisiones
used = {}              # emoji -> concepto dueño
nonstandard_fixed = [] # informe paso 2

# 1) FUENTE 1: sintesio.db gana SIEMPRE (los 160 con glifo)
for k, e in sorted(sintesio_con_emoji.items()):
    orig = e
    if es_no_estandar(e) and k in REEMPLAZOS_NO_ESTANDAR:
        e = REEMPLAZOS_NO_ESTANDAR[k][1]
        nonstandard_fixed.append((k, orig, e,
            f"reemplazado por equivalente estándar: {orig} → {e} (añadido U+FE0F)"))
    chosen[k] = e
    cand_by_concept[k] = [(e, "(asignación canónica sintesio.db)", None, 100)]
    used[e] = k

# 2) FUENTE 2: fallback CLDR (46 sin glifo + 71 extras).
#    Asignación codiciosa en dos pasadas para NO dejar huecos:
#    P1: conceptos cuyo mejor candidato está libre.
#    P2: conceptos bloqueados que migran a su siguiente candidato libre.
#    P3: sin candidato libre -> más cercano + nota (registrado como colisión).
pendientes = sorted(sin_glifo | (set(CANDIDATOS_CLDR) - todos_imports))
usaron_segundo = []
cands_pend = {k: clist(k) for k in pendientes}

def _try_assign(k, e_norm, rank):
    """Asigna e_norm a k si está libre. Devuelve True/False."""
    if e_norm in used:
        return False
    owner_old = None
    chosen[k] = e_norm
    cand_by_concept[k] = cands_pend[k]
    used[e_norm] = k
    if rank > 0:
        usaron_segundo.append(k)
        displaced = cands_pend[k][0][0].strip()
        winner = used.get(displaced, "?")
        res = "especifico_gana" if winner in sintesio_con_emoji else "mayor_puntuacion"
        if any(c[0] == displaced and c[2] == k for c in collisions):
            pass
        else:
            collisions.append((displaced, winner, k, res,
                f"prioridad {'sintesio.db' if winner in sintesio_con_emoji else 'asignada'}; "
                f"{k} migra a {e_norm} (candidato #{rank+1}, p={cands_pend[k][rank][3]})"))
    return True

blocked = []
# P1: separar pendientes sin candidatos (imposible de emparejar)
for k in pendientes:
    if not cands_pend[k]:
        chosen[k] = "\u2754"; cand_by_concept[k] = []
        collisions.append(("\u2754", k, k, "sin_alternativa", "sin candidato CLDR"))

# P2: matching bipartito máximo (caminos aumentantes de Kuhn).
#     Nodos izquierda: pendientes ordenados por prioridad (sintesio.db >
#     puntuación CLDR > alfabético). Nodos derecha: emojis candidatos.
#     Un emoji solo puede emparejarse una vez -> cero duplicados.
REUBICACION = {"marmota", "balanza", "vecindario", "ola", "hielo", "nieve",
               "tulipan", "hibisco", "gota", "historia", "libro"}  # pierden su top ante canónicos
a_emparejar = [k for k in pendientes if cands_pend[k] and k not in chosen
               and k not in REUBICACION]
prior_orden = sorted(
    a_emparejar,
    key=lambda k: (k not in sintesio_con_emoji,
                   -(cands_pend[k][0][3] if cands_pend[k] else 0), k))
fijos_sintesio = set(used)          # emojis canónicos intocables
adj = {k: [c[0].strip() for c in cands_pend[k] if c[0].strip() not in fijos_sintesio]
       for k in prior_orden}
match_e = {}                       # emoji -> concepto emparejado
def _augment(k, seen):
    for e in adj[k]:
        if e in seen: continue
        seen.add(e)
        if e not in match_e or _augment(match_e[e], seen):
            match_e[e] = k
            return True
    return False
sys.setrecursionlimit(10000)
for k in prior_orden:
    _augment(k, set())

inv_match = {kk: ee for ee, kk in match_e.items()}
sin_match = []
for k in prior_orden:
    e = inv_match.get(k)
    if e is None or e in used:      # nunca duplicar; P2c buscará un libre
        sin_match.append(k); continue
    rank = [c[0].strip() for c in cands_pend[k]].index(e)
    chosen[k] = e
    cand_by_concept[k] = cands_pend[k]
    used[e] = k
    if rank > 0:
        usaron_segundo.append(k)
        displaced = cands_pend[k][0][0].strip()
        winner = used.get(displaced) or inv_match.get(displaced) or \
                 next((oo for oo, ee in used.items() if False), None)
        # dueño real: quien quedó con 'displaced' tras el matching
        winner = used_owner_of(displaced)
        res = "especifico_gana" if winner in sintesio_con_emoji else "mayor_puntuacion"
        collisions.append((displaced, winner, k, res,
            f"prioridad {'sintesio.db' if winner in sintesio_con_emoji else 'asignada'}; "
            f"{k} migra a {e} (candidato #{rank+1}, p={cands_pend[k][rank][3]})"))

# P2b: los dueños CLDR que se quedaron un top reclamado por concepto
#     canónico migran a su segundo candidato (el específico gana).
for e_ in sorted(set(used)):
    owner = used[e_]
    if owner in REUBICACION and owner in cands_pend \
       and e_ == cands_pend[owner][0][0].strip():
        reclamador = next((kk for kk in pendientes
                           if cands_pend.get(kk) and cands_pend[kk][0][0].strip() == e_), None)
        if reclamador is None or reclamador in chosen:
            continue                     # el canónico ya tiene emoji: no mover
        cl = cands_pend[owner]
        for rank2 in range(1, len(cl)):
            alt = cl[rank2][0].strip()
            if alt not in used:
                del used[e_]
                _try_assign(owner, alt, rank2)
                break

# P2c: para cada no emparejado, buscar cualquier candidato LIBRE (o dejarlo
#     al primer candidato con nota de colisión). Prioridad: canónicos primero.
restantes = [k for k in sin_match if k not in chosen] + \
            [k for k in sorted(REUBICACION) if k not in chosen and cands_pend.get(k)]
for k in sorted(set(restantes),
                key=lambda kk: (kk not in sintesio_con_emoji, kk)):
    if k in chosen or not cands_pend.get(k):
        continue
    cl = cands_pend[k]
    for rank2, cand in enumerate(cl):
        alt = cand[0].strip()
        if alt not in used and alt not in fijos_sintesio:
            _try_assign(k, alt, rank2)
            break

# P3: sin candidato libre -> pictograma aproximado único + nota (excepcional)
import unicodedata as _ud
for k in [kk for kk in sin_match if kk not in chosen]:
    cl = cands_pend.get(k, [])
    o = None
    for cp in range(0x1F300, 0x1FAFF):
        e_try = chr(cp)
        if e_try in used or e_try in fijos_sintesio: continue
        try: nm = _ud.name(e_try)
        except ValueError: continue
        if not nm or "FACE" in nm or "HAND" in nm: continue
        o = e_try; break
    if o is None:
        o = "\u2754"
    chosen[k] = o
    cand_by_concept[k] = cl
    used[o] = k
    top = cl[0][0].strip() if cl else "?"
    collisions.append((top, used.get(top, "?"), k, "sin_alternativa",
                       f"sin emoji libre entre candidatos; aproximado {o}; revisar"))

# 3) Colisiones entre perdedores CLDR donde NO hubo migración limpia:
#    registrar también como especifico_gana las cesiones a sintesio.db
#    (ya cubiertas arriba con 'segundo_candidato').

# ============================================================================
# PASO 4 — columnas léxicas
# ============================================================================
SWADESH_HINT = {"agua","fuego","tierra","mar","sol","luna","piedra","persona","mujer",
 "hombre","niño","mano","pie","ojo","nariz","boca","día","noche","comer","beber","casa",
 "puerta","grande","pequeño","caliente","frio","vida","muerte","corazón","ver","oir",
 "hablar","escribir","lluvia","nube","viento","flor","árbol","hoja","estrella","cielo",
 "perro","gato","caballo","vaca","oveja","cerdo","gallina","pájaro","pez","serpiente",
 "rana","elefante","oso","lobo","ratón","pan","carne","leche","huevo","sangre","hueso",
 "piel","cabello","diente","lengua","rodilla","codo","muñeca","cabeza","oreja","frente"}
BASIC_HINT = SWADESH_HINT | {"ciudad","camino","libro","escuela","maestro","aprender"}

def cognado_de(nuniv, k):
    try: n = int(nuniv)
    except (TypeError, ValueError): n = 0
    if n >= 6: return "universal", n
    if n >= 4: return "romance", n
    if n >= 2: return "parcial", n
    return "ninguno", n

rows_to_insert = []
dudosos = []
for k in sorted(chosen):
    e = chosen[k]
    src_parts = []
    if k in sintesio_con_emoji:
        src_parts.append("emoji desde sintesio.db")
    elif k in sin_glifo or k in CANDIDATOS_CLDR:
        src_parts.append("emoji desde búsqueda CLDR")
    for kk, orig, nuevo, msg in nonstandard_fixed:
        if kk == k:
            src_parts.append(msg)
    aprox = [c for c in cand_by_concept.get(k, []) if c[3] < 75]
    if k in sin_glifo and (not cand_by_concept.get(k) or cand_by_concept[k][0][3] < 80):
        src_parts.append("sin emoji propio: aproximado")

    f = formas.get(k, ("—",)*7)
    es, fr_, it, pt, ro, ia, eo = f
    en = EN.get(k.lower(), "—")
    md = metadatos.get(k, {})
    cat = md.get("clase") if md.get("clase") in ("sustantivo","verbo","adjetivo","adverbio") else "sustantivo"
    cogn, cons = cognado_de(md.get("nuniv"), k)
    # forma ganadora: consenso sobre es; si es=='—' primera no vacía
    langs = [("es",es),("en",en),("fr",fr_),("it",it),("pt",pt),("ro",ro),("ia",ia),("eo",eo)]
    # limpiar valores que contengan saltos de línea del CHECK multi-línea
    real = [(l,v) for l,v in langs if v not in ("—","") and "\n" not in str(v)]
    if es not in ("—","") and "\n" not in str(es):
        ganadora, fuente_g = es, "es"
    elif real:
        fuente_g, ganadora = real[0]   # (código_lengua, forma)
    else:
        ganadora, fuente_g = k, "es"   # concepto como forma; fuente nominal es
    # el valor de la columna fuente_ganadora debe ser un código limpio
    fuente_g = fuente_g.split("\n")[0].strip()[:2]
    nota = "; ".join(src_parts)
    variants = md.get("variantes") or ""
    if "descarta" in variants or "descartada" in (md.get("nota_ranking") or ""):
        tok = re.search(r"descarta(?:da)?\s+(\w+)", variants + " " + (md.get("nota_ranking") or ""))
        if tok: nota += f"; sinónimo descartado: {tok.group(1)}"
    rows_to_insert.append((e, k, es, en, fr_, it, pt, ro, ia, eo,
                           md.get("latin","—"), cat,
                           1 if k in SWADESH_HINT else 0,
                           1 if k in BASIC_HINT else 0,
                           cogn, cons, ganadora, fuente_g, nota or None))
    if cons < 3: dudosos.append((k, "consenso_bajo", f"consenso={cons}; revisar Wiktionary"))
    if "sin emoji propio" in (nota or ""): dudosos.append((k, "sin_emoji", "usar candidato alternativo de emoji_candidatos"))
    for kk, orig, nuevo, msg in nonstandard_fixed:
        if kk == k: dudosos.append((k, "emoji_no_estandar", msg))
    if fuente_g != "es": dudosos.append((k, "fuente_no_es", f"ganadora={ganadora} ({fuente_g})"))
    if "sinónimo descartado" in (nota or ""): dudosos.append((k, "sinonimo_descartado", nota.split("sinónimo descartado: ")[-1]))

# ============================================================================
# PASO 5 — inserción en transacción única (idempotente)
# ============================================================================
conn = sqlx.connect(LEXICO_DB)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()
try:
    cur.execute("BEGIN TRANSACTION")
    # borrado previo para re-ejecución idempotente (respeta semilla fase 1)
    cur.execute("DELETE FROM emoji_candidatos")
    cur.execute("DELETE FROM lexico")
    cur.execute("DELETE FROM emoji_colisiones WHERE id > 6")

    # 1) lexico (primero FK padre: sintesio, luego CLDR)
    n_lex = 0
    for row in sorted(rows_to_insert, key=lambda r: (r[1] not in sintesio_con_emoji, r[1])):
        cur.execute(
            """INSERT INTO lexico (emoji, concepto_es, es, en, fr, it, pt,
                                   ro, ia, eo, latin, categoria, swadesh, basic_level,
                                   cognado, lenguas_consenso, forma_ganadora,
                                   fuente_ganadora, nota)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", row)
        n_lex += 1

    # 2) candidatos (elegido=1 el ganador)
    n_cand = 0
    for k in sorted(cand_by_concept):
        for (ce, cname, ccod, cpunt) in cand_by_concept[k]:
            ce = ce.strip()
            elegido = 1 if chosen.get(k) == ce else 0
            cod = ccod if ccod else "U+" + format(ord(ce[0]), "04X")
            if "\ufe0f" in ce and "FE0F" not in cod:
                cod += " FE0F"
            cur.execute(
                """INSERT INTO emoji_candidatos
                   (concepto_es, emoji, nombre_oficial, codepoint, puntuacion, elegido, nota)
                   VALUES (?,?,?,?,?,?,?)""",
                (k, ce, cname, cod, min(int(cpunt), 100), elegido,
                 "paso 4: " + ("fuente sintesio.db" if k in sintesio_con_emoji else "búsqueda CLDR")))
            n_cand += 1

    # 3) colisiones nuevas
    n_col = 0
    for row in collisions:
        cur.execute(
            "INSERT INTO emoji_colisiones (emoji, concepto_ganador, concepto_perdedor,"
            " resolucion, nota) VALUES (?,?,?,?,?)", row)
        n_col += 1

    conn.commit()
except Exception as ex:
    conn.rollback()
    print(f"ERROR durante la transacción: {ex}")
    raise SystemExit(1)

# ============================================================================
# PASO 6 — verificación
# ============================================================================
def q(sql): return cur.execute(sql).fetchone()[0]
print("=" * 70)
print("VERIFICACIÓN PASO 4 COMPLETO")
print("=" * 70)
total = q("SELECT COUNT(*) FROM lexico")
print(f"1. Total lexico:                       {total}  (esperado 180-205+)")
print(f"2. Emojis únicos:                      {q('SELECT COUNT(DISTINCT emoji) FROM lexico')}")
print(f"3. Conceptos únicos:                   {q('SELECT COUNT(DISTINCT concepto_es) FROM lexico')}")
dup_e = cur.execute("SELECT emoji, COUNT(*) FROM lexico GROUP BY emoji HAVING COUNT(*)>1").fetchall()
dup_c = cur.execute("SELECT concepto_es, COUNT(*) FROM lexico GROUP BY concepto_es HAVING COUNT(*)>1").fetchall()
print(f"4. Duplicados emoji/concepto:          {len(dup_e)}/{len(dup_c)}  {dup_e}{dup_c}")
print("5. Categorías:", cur.execute("SELECT categoria,COUNT(*) FROM lexico GROUP BY categoria").fetchall())
print("6. Cognados:", cur.execute("SELECT cognado,COUNT(*) FROM lexico GROUP BY cognado").fetchall())
print(f"7. Consenso bajo (<3):                 {q('SELECT COUNT(*) FROM v_consenso_bajo')}")
print(f"8. Sin emoji propio (vista):           {q('SELECT COUNT(*) FROM v_sin_emoji_propio')}")
print(f"9. emoji_colisiones total:             {q('SELECT COUNT(*) FROM emoji_colisiones')} (semilla 6 + nuevas {n_col})")
print(f"10. emoji_candidatos:                  {q('SELECT COUNT(*) FROM emoji_candidatos')} (insertados {n_cand})")
print(f"11. Ganadora no española:              {q('SELECT COUNT(*) FROM v_ganadora_no_es')}")
print(f"12. integrity_check:                   {q('PRAGMA integrity_check')}")
n_syn = q("SELECT COUNT(*) FROM lexico WHERE nota LIKE '%sintesio.db%'")
print(f"13. Nota sintesio.db:                  {n_syn} (esperado 160)")
fk = cur.execute("PRAGMA foreign_key_check").fetchall()
print("14. foreign_key_check:", fk or "sin errores")

print("\n--- Colisiones nuevas registradas ---")
for r in cur.execute("SELECT emoji,concepto_ganador,concepto_perdedor,resolucion FROM emoji_colisiones WHERE id>6 ORDER BY id"):
    print(" ", r)

print("\n--- Emojis no estándar revisados (paso 2) ---")
for k, orig, nuevo, msg in nonstandard_fixed:
    print(f"  {k}: {msg}")

print("\n--- Detalle por fuente ---")
print(f"  FUENTE 1 sintesio.db: {len(sintesio_con_emoji)}")
print(f"  FUENTE 2 CLDR:        {total - len(sintesio_con_emoji)}")
print(f"  ...de los cuales requirieron 2º/3º candidato: {sorted(set(usaron_segundo))}")
print(f"  Tiempo total: {time.time()-T0:.2f}s")

conn.close()

# ============================================================================
# ENTREGABLES CSV
# ============================================================================
import csv
with open("conflictos_resueltos.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["emoji", "ganador", "perdedor", "segundo_candidato", "resolucion"])
    for e, gw, ls, res, note in collisions:
        alt = ""
        m = re.search(r"migra a (\S+)", note or "")
        if m: alt = m.group(1)
        w.writerow([e, gw, ls, alt, res])

with open("conceptos_dudosos.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["concepto_es", "motivo", "sugerencia"])
    seen = set()
    for k, mot, sug in dudosos:
        if (k, mot) in seen: continue
        seen.add((k, mot)); w.writerow([k, mot, sug])

print("\nEntregables CSV escritos: conflictos_resueltos.csv, conceptos_dudosos.csv")
