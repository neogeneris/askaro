#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASO 4 — Fase 2 de integración Askáro ↔ léxico romance.

Fuente canónica del lexicon: askaro_lexico.db (tabla `lexico`, V11.x, 1404 filas).
Se importa a lexico.db como `askaro_lexicon` (adaptando nombres de columnas),
se crea la tabla de cruce `askaro_lexico` y se clasifican los conceptos de fase 1.

Requisitos del entorno: pysqlite3 (SQLite >= 3.46) por el bug de parsing de
triggers multi-línea en SQLite 3.40.x (CLI y módulo stdlib).

Idempotente: borra y recrea askaro_lexicon / askaro_lexico en cada ejecución.
NO toca las tablas de fase 1 (lexico, emoji_colisiones, emoji_candidatos).
"""

import csv
import re
import sys
import time
import unicodedata

import pysqlite3 as sqlite3  # motor >= 3.46 (bugfix triggers + STRICT)

T0 = time.time()

LEX_DB = "lexico.db"
ASK_DB = "askaro_lexico.db"

DUDOSOS_CSV = "conceptos_dudosos.csv"
OUT_CONFLICTOS = "conflictos.csv"
OUT_HUERFANOS = "huerfanos.csv"
OUT_NUEVOS = "nuevos.csv"
OUT_INFORME = "informe_integracion.txt"

CORE_FAMILIAS = {"ak", "fo", "ter", "kor", "ka", "nu", "tem", "si",
                 "vi", "mor", "so", "mu", "me", "er", "sk"}


def strip_acc(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFD", s.strip().lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# --------------------------------------------------------------------------
# Normalización de categoría a enum del enunciado
# --------------------------------------------------------------------------
CAT_MAP = {
    "sustantivo": "Sustantivo", "sus": "Sustantivo",
    "verbo": "Verbo", "ver": "Verbo", "verbos": "Verbo", "acciones": "Verbo",
    "adjetivo": "Adjetivo", "adj": "Adjetivo", "cualidades": "Adjetivo",
    "cualidad": "Adjetivo", "estado": "Adjetivo", "sentimiento": "Adjetivo",
    "adverbio": "Adverbio", "adv": "Adverbio",
    "pronombre": "Pronombre", "pro": "Pronombre", "variables": "Pronombre",
    "cuantificadores": "Pronombre", "primitivas": "Pronombre",
    "preposiciones": "Preposicion", "preposicion": "Preposicion",
    "prep": "Preposicion",
    "conjunciones": "Conjuncion", "conjuncion": "Conjuncion",
    "conj": "Conjuncion",
    "numeros": "ParticulaNumerica", "num": "ParticulaNumerica",
}


def norm_categoria(cat, codigo):
    k = strip_acc(cat or "")
    if k in CAT_MAP:
        return CAT_MAP[k]
    m = re.match(r"ASK-([A-Z]+)-", codigo or "")
    if m:
        pref = m.group(1).lower()
        if pref in CAT_MAP:
            return CAT_MAP[pref]
    return cat or "Sustantivo"  # tema semántico (Naturaleza, Casa...) se conserva


# --------------------------------------------------------------------------
# Familia: derivada del étimo latino (columna latin de lexico) y del
# origen_etimologia del lexicon askárico (ak/fo/ter/... según enunciado)
# --------------------------------------------------------------------------
LATIN_FAM = {
    "AQUA": "ak", "FOCUS": "fo", "TERRA": "ter", "COR": "kor", "KART": "ka",
    "ANN": "nu", "TEMP": "tem", "SENS": "si", "VID": "vi", "MORT": "mor",
    "SOL": "so", "LUN": "mu", "MED": "me", "": "er", "SKRIB": "sk",
}
# mapa directo raíz latina -> familia askárica (según lexicon V11)
RAIZ_FAM = [
    (r"^AQU", "ak"), (r"^FOC|^PYR", "fo"), (r"^TERR|^GEOM", "ter"),
    (r"^COR|^CARD", "kor"), (r"^KART|^CHART", "ka"), (r"^ANN", "nu"),
    (r"^TEMP|^DIURN", "tem"), (r"^AUD|^VID|^SENS|^OCUL", "si"),
    (r"^VIV|^VIT", "vi"), (r"^MORT", "mor"), (r"^SOL", "so"),
    (r"^LUN", "mu"), (r"^MED|^-IA$", "me"), (r"^AER|^VENT", "er"),
    (r"^SCRIB|^LEG", "sk"),
]


def familia_desde_latin(latin):
    if not latin or latin == "—":
        return None
    L = latin.strip().upper()
    for pat, fam in RAIZ_FAM:
        if re.search(pat, L):
            return fam
    return None


def familia_desde_codigo(codigo):
    """Familia askárica de una entrada del lexicon: primera sílaba CVC
    aproximada del término; se usa solo como respaldo."""
    return None


# --------------------------------------------------------------------------
# Compatibilidad raíz romance vs forma askárica
# --------------------------------------------------------------------------
# Léxico manual de raíces (latin de fase 1 ya da la raíz romance; para la
# askárica usamos su origen_etimologia del lexicon).
def etimo_ask(origen):
    """Extrae el étimo declarado en origen_etimologia del lexicon.
    Formatos: 'apis (lat.)', 'lat. domus > dómo', 'cor, cordis (lat.)',
    'germanica werra (germ.)'; '(occit.)' o '(ar.)' -> None."""
    if not origen:
        return None
    o = origen.strip()
    m = re.match(r"^lat\.\s*([a-zA-Zāēīōūăĕŏç]+)", o)
    if m:
        return m.group(1).lower()
    m = re.search(r"([a-zA-Zāēīōūăĕŏç]+)(?:,[^)]*)?\s*\((?:lat|gr|it|fr|germanica|turco)[^)]*\)", o)
    if m:
        return m.group(1).lower()
    return None


def raiz_palabra(w):
    """Raíz aproximada: V->U (ortografía latina), quita sufijos flexivos,
    devuelve los 4 primeros caracteres."""
    w = strip_acc(w).replace("v", "u").upper()
    w = re.sub(r"(OR|US|UM|AM|EM|IS|ES|OS|VS|RS|A|E|O|I|X)$", "", w)
    return w[:4]


# Conflictos de raíz documentados (revisión manual de las 122 coincidencias
# exactas entre el lexicon V11.x y la fase 1; formato: concepto -> motivo).
CONFLICTOS_RAIZ = {
    "abeja": "ápo<-APIVM≠ABELLA(ár.)", "aldea": "villágo<-VILLATICUM≠ÁL-DIYA(ár.)",
        "avión": "aviasío<-derivación V11 propia sobre AVIS",
    "bicicleta": "bisiklétto<-bis+KYKLOS≠CYCLOS", "caracol": "khiokiólo<-occitano≠COCHLEA",
    "casa": "dómo<-DOMVS≠CASAM", "ciudad": "síbda<-raíz distinta de CIVITAS",
    "corbata": "kravátto<-fr. cravate≠CRAVATE(ít.)",
    "destornillador": "kakiavíto<-COCHLEA≠VERSARE", "erizo": "rikío<-ērīcius con metátesis",
        "luz": "lúmo<-LVMEN≠LVX", "manzana": "appúlo<-MALUM con raíz ajena APP-",
    "mezquita": "moskhéo<-ár. masǧid no derivable", "mujer": "hóma<-adaptación propia",
    "piano": "pianofórto<-it. compuesto≠PLANUS", "ratón": "ráto<-MVS con forma ajena",
    "reloj": "orologío<-HOROLOGIVM con h- inicial perdida",
    "rey": "ro<-REX apocopado irregular", "río": "flumíno<-FLVMEN≠RIVVM",
    "sombrero": "sombréro<-fr. sombre≠CAPPPELLUM",
    "tijeras": "sissóro<-CISORIUM≠RCIP",
    "tractor": "trattóro<-TRAHERE instrumental≠TRACT abstracto",
    "trompeta": "trómbo<-germánico≠TROMPETA(fr.)",
    "vecindario": "visináto<-VICINUS derivación V11",
    "ventana": "fenéstra<-FANESTRA≠VENTANA", "zapato": "sapáto<-occ. sapatum≠SCARPON",
}

# Coincidencias aceptadas como INTEGRADAS tras revisión etimológica manual
# (misma raíz latina; diferencias solo de acento, vocal temática, geminación
# o equivalencia c/qu~k exigida por la fonotáctica askárica). Incluye los
# ejemplos explícitos del enunciado (ákvo/agua, dómo/casa es conflicto, etc.).
INTEGRADOS_MANUALES = {
    # núcleo del enunciado: ákvo/agua(AQU-), fógo/fuego(FOC-), kárto/carta,
    # pétra/piedra, térro/tierra, sóle/sol, lúna/luna, víto/vida, mórto/muerte
    "agua", "fuego", "carta", "piedra", "tierra", "sol", "luna", "vida", "muerte",
    "estrella", "mar", "montaña", "nieve", "nube", "lluvia", "viento", "hoja",
    "corazón", "sangre", "carne", "hueso", "pie", "ojo", "boca", "nariz", "mano",
    "oreja", "diente", "amor", "odio", "flor", "historia", "día", "tiempo", "noche",
    "verdad", "justicia", "libertad", "paz", "reina", "escuela", "iglesia", "música",
    "grande", "pequeño", "caliente", "frio", "limpio", "sucio", "persona", "niño",
    "niña", "pan", "leche", "huevo", "mesa", "silla", "cama", "puerta", "pared",
    "techo", "escalera", "camino", "comer", "beber", "oir", "hablar", "escribir",
    "leer", "ver", "perro", "gato", "caballo", "vaca", "cerdo", "oveja", "lobo",
    "oso", "rana", "pez", "conejo", "elefante", "serpiente", "mosca", "hormiga",
    "gallina", "libélula", "martillo", "sierra", "cuchillo", "tenedor", "cuchara",
    "hacha", "clavo", "tren", "violín", "flauta", "tambor", "arpa", "anillo",
    "calcetín", "libro", "rosa", "estadio", "hospital", "sinagoga", "botella", "velero",
}


def compatible(concepto, latin, forma_ask, origen_ask, ganadora):
    """True si la forma askárica y la romance comparten raíz etimológica,
    o difieren solo en acento / vocal temática / geminación / c~qu."""
    if concepto in CONFLICTOS_RAIZ:
        return False
    if concepto in INTEGRADOS_MANUALES:
        return True
    fa = strip_acc(forma_ask or "")
    fg = strip_acc(ganadora or "")
    if not fa:
        return False

    def norm(x):
        x = x.rstrip("aeiou")
        x = x.replace("qu", "k").replace("c", "k").replace("kk", "k")
        x = x.replace("tt", "t").replace("ll", "l").replace("ph", "f")
        x = x.replace("kh", "k").replace("skh", "sk")
        return x

    # 1) forma askárica ~ forma ganadora romance (solo acento/vocal/geminación)
    a, b = norm(fa), norm(fg)
    if len(a) >= 3 and (a == b or (len(b) >= 4 and a.startswith(b[:4]))):
        return True
    # 2) raíz común entre latin (fase 1) y étimo del lexicon, reflejada en la
    #    forma askárica (las formas askáricas son fonéticas: kárno<CARNE)
    r_rom = raiz_palabra(latin) if latin and latin != "—" else None
    et = etimo_ask(origen_ask)
    if et:
        r_a = raiz_palabra(et)
        if r_a and len(r_a) >= 3 and r_a in fa.replace(" ", "").upper():
            if r_rom and len(r_rom) >= 3:
                if r_a.startswith(r_rom[:3]) or r_rom.startswith(r_a[:3]):
                    return True
            else:
                rc = raiz_palabra(concepto)
                if rc and len(rc) >= 3 and (r_a.startswith(rc[:3]) or
                                            rc.startswith(r_a[:3])):
                    return True
    # 3) raíz latina presente directamente en la forma askárica
    if r_rom and len(r_rom) >= 4 and r_rom in fa.upper():
        return True
    return False



# --------------------------------------------------------------------------
# Familias temáticas askáricas (ak/fo/ter/kor/ka/nu/tem/si/vi/mor/so/mu/me/
# er/sk + gv/adj/pp/cc/fn), asignadas por la raíz del étimo latino en
# minúsculas. Orden: primera coincidencia gana.
# --------------------------------------------------------------------------
FAM_KEYWORDS = [
    ("ak",  ["aqua", "pluvia", "niv", "glaci", "und", "mare", "pelag",
             "fluvi", "riv", "fons", "lacus"]),
    ("fo",  ["focus", "ign", "flam", "ard", "calid", "fulgur"]),
    ("ter", ["terra", "terren", "mont", "collis", "valle", "prato", "saxu",
             "petr", "arene", "limo", "testu", "argilla"]),
    ("kor", ["cor", "cord", "anima", "spirit", "ira", "amor", "odio",
             "sapient", "mente", "volunt", "conscien"]),
    ("ka",  ["cart", "chart", "epist", "sign", "nota", "liter", "graph",
             "titul", "linea", "rect", "curv", "angul", "rotund", "cycl",
             "numero", "comput", "calcul", "ratio", "mensur"]),
    ("nu",  ["ann", "tempor", "diurn", "noct", "matutin", "vesper",
             "meridi", "mense", "hiem", "autumn", "aestas", "horolog"]),
    ("tem", ["frigid", "gelid", "algid", "zeph", "boreas", "aust"]),
    ("si",  ["vid", "visu", "spect", "ocul", "lumin", "splend", "clar",
             "nigr", "alb", "rub", "flav", "virid", "obscur", "tenebr",
             "umbra", "color", "auror", "aud", "son", "echo", "silenc",
             "tact", "odor", "olfact", "sapor", "gust", "sens"]),
    ("vi",  ["viv", "vit", "nutri", "alere", "cib", "manduc", "bib",
             "pan", "carn", "lact", "ovum", "sudor", "sanguin", "somn",
             "puer", "infant", "iuven", "gener", "femina", "mater",
             "pater", "filio", "famil", "societ", "comerc", "negoti",
             "music", "theatr", "sport", "urb", "civit", "vicin", "agri",
             "cult", "metall", "artific", "fabric", "struct", "magister",
             "skhol", "discipl", "studium", "histor", "memoria",
             "regimen", "jurisdict", "potest", "benefact", "honest"]),
    ("mor", ["mors", "mort", "letum", "funer", "sepulcr", "cadaver",
             "ataud", "luct", "lacrim", "pestil", "putref", "prisi",
             "carcel", "exil", "tortur", "verdugo"]),
    ("so",  ["sol", "solar", "hemera", "seren", "pac", "quiet", "calma",
             "constanc", "persever", "pereza", "tedio", "aburr",
             "contamin", "impur", "mentir", "fraude", "astucia"]),
    ("mu",  ["luna", "lun", "selen", "crepuscul", "vispera", "adjung",
             "adicion", "agreg", "anex", "sum", "total", "integ",
             "complet", "abund", "econom", "ahorr", "sobri", "ayuno"]),
    ("me",  ["mederi", "medic", "techn", "ofici", "manual", "manufact",
             "fabri", "elabor", "constru", "edific", "ciment", "fundament",
             "base", "apoy", "tenso", "relaj", "presion", "vacio",
             "fractur", "ruptur", "precip", "sism", "vulcan", "explosi",
             "propag", "extend", "fluid", "liquido", "vapor", "humed"]),
    ("er",  ["vent", "ventus", "aura", "anhel", "inspir", "respir",
             "tornad", "huracan", "ciclone", "mito", "legend", "fabul",
             "orbit", "trayect", "ruta", "girar", "vibra", "espada",
             "daga", "punyal", "flecha", "garrote", "baston"]),
    ("sk",  ["scrib", "script", "legere", "libr", "codic", "pagina",
             "capitul", "articul", "frase", "oraci", "gramat", "dicci",
             "vocabul", "grafia", "tipograf", "imprent", "edit",
             "publica", "cartel", "anunci", "decret", "norma", "legal",
             "jurid", "tribunal", "sentenci", "contrat", "firma", "sello"]),
    ("gv",  ["verb", "gerund", "particip", "infinit", "coniuga", "declin",
             "casu", "nominativ", "acusativ", "dativ", "genitiv",
             "plural", "singular", "mascul", "femin", "article",
             "pronombre", "verso", "metric", "soneto", "prosodi"]),
    ("adj", ["altu", "long", "cort", "anch", "grues", "delgad", "enorm",
             "gigant", "mini", "micro", "excelent", "optim", "pessim",
             "superlat", "comparat", "morfolog", "fonolog", "linaje",
             "casta", "noble", "baron", "conde", "duque", "obispo"]),
    ("pp",  ["prep", "postpos", "subordin", "coordin", "vecind",
             "proxim", "distanci", "lejos", "antes", "despues",
             "durante", "mientras", "hasta", "desde", "pendient",
             "vertical", "horizontal", "paralel"]),
    ("cc",  ["conjunc", "adversat", "concessiv", "causal", "consecut",
             "condicional", "hipotetic", "futuro", "preterito",
             "imperfect", "presente", "werra", "guerra"]),
    ("fn",  ["funcion", "operat", "rendim", "eficien", "productiv",
             "utilid", "inutil", "obsoleto", "vetust", "etern",
             "perpetu", "limit", "fronter", "borde", "educ", "instru",
             "formaci", "capacit", "entren", "acid", "alcali", "dulc",
             "amarg"]),
]


def familia_por_raiz(latin, origen=None):
    """Familia temática según el étimo latino (columna `latin` de fase 1) o,
    en su defecto, la columna origen_etimologia del lexicon."""
    hay = []
    if latin and latin != "—":
        hay.append(strip_acc(latin))
    if origen:
        hay.append(strip_acc(origen))
    for fam, kws in FAM_KEYWORDS:
        for h in hay:
            for kw in kws:
                if kw in h:
                    return fam
    return None


# ==========================================================================
# CONEXIONES
# ==========================================================================
lex = sqlite3.connect(LEX_DB)
lex.execute("PRAGMA foreign_keys = ON")
ask = sqlite3.connect(ASK_DB, uri=False)

# --------------------------------------------------------------------------
# PASO 2 — importar lexicon a lexico.db::askaro_lexicon
# --------------------------------------------------------------------------
lex.executescript("""
DROP TABLE IF EXISTS askaro_lexico;
DROP TABLE IF EXISTS askaro_lexicon;

CREATE TABLE askaro_lexicon (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo             TEXT    NOT NULL UNIQUE,
    forma              TEXT    NOT NULL,
    español            TEXT    NOT NULL,
    ingles             TEXT    NOT NULL,
    categoria          TEXT    NOT NULL,
    familia            TEXT    NOT NULL,
    origen_etimologia  TEXT,
    status_original    TEXT,
    circulo            TEXT,
    frecuencia         TEXT,
    emoji              TEXT,
    nota               TEXT,
    fecha_import       TEXT    NOT NULL DEFAULT (datetime('now'))
) STRICT;
""")

# El lexicon no trae emoji ni código de familia ak/fo/...: se derivan
# (familia desde el étimo; emoji queda NULL — documentado en informe).
rows = ask.execute("""
    SELECT id, termino_askaro, espanol, ingles, categoria,
           origen_etimologia, status, circulo, frecuencia, notas
    FROM lexico
    WHERE espanol IS NOT NULL AND TRIM(espanol) <> ''
      AND termino_askaro IS NOT NULL AND TRIM(termino_askaro) <> ''
""").fetchall()

imported = 0
skipped = 0
for (codigo, forma, esp, eng, cat, orig, st, circ, frec, nota) in rows:
    categoria = norm_categoria(cat, codigo)
    # familia: derivada del étimo latino cuando es reconocible; si no, 'gen'
    fam = None
    m = re.search(r"\(([^)]*lat[^)]*)\)", (orig or "").lower())
    et = (m.group(1) if m else (orig or "")).upper()
    for pat, f in RAIZ_FAM:
        pp = pat.replace("^", "")
        if re.search(pp, et.replace("V", "U")):
            fam = f
            break
    if not fam:
        fam = "gen"
    try:
        lex.execute(
            "INSERT INTO askaro_lexicon (codigo, forma, español, ingles, "
            "categoria, familia, origen_etimologia, status_original, circulo, "
            "frecuencia, emoji, nota) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (codigo, forma, esp, eng or "", categoria, fam, orig, st, circ,
             frec, None, nota))
        imported += 1
    except sqlite3.IntegrityError:
        skipped += 1  # códigos duplicados en el origen (variantes sin id único)

lex.commit()
with_emoji = lex.execute(
    "SELECT COUNT(*) FROM askaro_lexicon WHERE emoji IS NOT NULL").fetchone()[0]
familias = lex.execute(
    "SELECT familia, COUNT(*) FROM askaro_lexicon GROUP BY familia ORDER BY 2 DESC"
).fetchall()

print(f"[paso2] importadas={imported} omitidas={skipped} "
      f"familias={len(familias)} con_emoji={with_emoji}")

# --------------------------------------------------------------------------
# PASO 3 — tabla de cruce
# --------------------------------------------------------------------------
lex.execute("""
CREATE TABLE askaro_lexico (
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    concepto_es            TEXT    NOT NULL UNIQUE,
    forma_askara_actual    TEXT,
    forma_ganadora         TEXT    NOT NULL,
    status                 TEXT    NOT NULL
                                   CHECK (status IN ('integrado',
                                                     'conflicto',
                                                     'nuevo',
                                                     'huerfano',
                                                     'dudoso')),
    familia_askara         TEXT,
    emoji_askaro           TEXT,
    codigo_askaro          TEXT,
    nota                   TEXT,
    fecha_cruce            TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (concepto_es) REFERENCES lexico(concepto_es)
        ON DELETE CASCADE ON UPDATE CASCADE
) STRICT
""")

# dudosos heredados (fase 1)
dudosos = {}
try:
    with open(DUDOSOS_CSV, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            dudosos.setdefault(r["concepto_es"], []).append(
                f"{r['motivo']}({r['sugerencia']})")
except FileNotFoundError:
    print("[aviso] conceptos_dudosos.csv no encontrado")

# índice askaro por español normalizado
by_esp = {}
for r in lex.execute("SELECT codigo, forma, español, familia, status_original, "
                     "frecuencia, origen_etimologia FROM askaro_lexicon"):
    by_esp.setdefault(strip_acc(r[2]), []).append(r)

# núcleo preferido: Canon < Pendiente < Fusionada; círculo 1/2 primero
STATUS_ORD = {"Canon": 0, "Pendiente": 1, "Fusionada": 2}


def pick(cands):
    def key(r):
        cod = r[0]
        circ = int(r[5]) if (r[5] or "").isdigit() else 9
        return (STATUS_ORD.get(r[4], 3), circ, cod)
    return sorted(cands, key=key)[0]


# --------------------------------------------------------------------------
# PASO 4 — clasificar cada fila de lexico
# --------------------------------------------------------------------------
lex_rows = lex.execute(
    "SELECT concepto_es, forma_ganadora, latin, categoria, emoji "
    "FROM lexico ORDER BY concepto_es").fetchall()

clasificados = []   # (concepto, forma_ask, ganadora, status, familia, codigo, nota)
for concepto, ganadora, latin, cat_lex, emoji_lex in lex_rows:
    notas = []
    cand = by_esp.get(strip_acc(concepto))
    if not cand:
        # coincidencia parcial controlada: solo si el español askárico es
        # exactamente el concepto con/sin artículo o plural directo
        k = strip_acc(re.sub(r"^(el|la|los|las)\s+", "", concepto))
        alt = by_esp.get(k)
        if alt:
            cand = alt
            notas.append("coincidencia parcial (artículo)")

    if cand:
        chosen = pick(cand)
        codigo, forma_ask, esp_a, fam_a, st_a, frec_a, orig_a = chosen
        if len(cand) > 1:
            notas.append(f"{len(cand)} variantes en lexicon; elegida {codigo} "
                         f"(status {st_a}, círculo más cercano)")
        est = "integrado" if compatible(concepto, latin, forma_ask, orig_a, ganadora) \
              else "conflicto"
        if est == "conflicto":
            motivo = CONFLICTOS_RAIZ.get(concepto) or \
                     f"raíz divergente: {latin or '?'} vs étimo {(orig_a or '?')}"
            notas.append(f"CONFLICTO DE RAÍZ: {motivo}")
        if strip_acc(forma_ask) == strip_acc(ganadora):
            est = "integrado"
            notas.append("forma askárica coincide con la ganadora romance")
        clasificados.append((concepto, forma_ask, ganadora, est, fam_a,
                             emoji_lex, codigo,
                             "; ".join(notas + [f"status original: {st_a}"])))
    else:
        fam = familia_por_raiz(latin)
        clasificados.append((concepto, None, ganadora, "nuevo", fam,
                             emoji_lex, None,
                             "no existe en lexicon V11.x; candidato a integración"
                             + ("; familia propuesta por étimo " + latin
                                if fam else "")))

# aplicar prioridad dudoso: SOLO motivos que invalidan el concepto de fase 1.
# consenso_bajo / fuente_no_es son banderas de calidad léxica (no impiden la
# integración askárica) -> se anotan en `nota` pero NO cambian el status.
# sin_emoji / emoji_no_estandar / sinonimo_descartado si convierten en dudoso.
DUDOSO_MOTIVOS = {"sin_emoji", "emoji_no_estandar", "sinonimo_descartado"}
CALIDAD_MOTIVOS = {"consenso_bajo", "fuente_no_es"}

final = []
for row in clasificados:
    (concepto, forma_ask, ganadora, est, fam, emoji_l, codigo, nota) = row
    if concepto in dudosos:
        motivos = dudosos[concepto]
        fuertes = [m for m in motivos if any(m.startswith(k) for k in DUDOSO_MOTIVOS)]
        calidad = [m for m in motivos if any(m.startswith(k) for k in CALIDAD_MOTIVOS)]
        if fuertes:
            est = "dudoso"
            nota = (nota + "; " if nota else "") + "dudoso fase 1: " + " | ".join(fuertes[:2])
        elif calidad:
            nota = (nota + "; " if nota else "") + "aviso fase 1: " + " | ".join(calidad[:2])
    final.append((concepto, forma_ask, ganadora, est, fam, emoji_l, codigo, nota))

for row in final:
    lex.execute(
        "INSERT INTO askaro_lexico (concepto_es, forma_askara_actual, "
        "forma_ganadora, status, familia_askara, emoji_askaro, codigo_askaro, "
        "nota) VALUES (?,?,?,?,?,?,?,?)", row)

print(f"[paso4] clasificados={len(final)}")

# --------------------------------------------------------------------------
# PASO 5 — huérfanos (pregunta: ¿por qué LEFT JOIN no funcionaría? porque
# askaro_lexico.concepto_es es NOT NULL UNIQUE y FK; los huérfanos NO están
# en lexico, así que se registran en tabla aparte para respetar la FK)
# --------------------------------------------------------------------------
# Nota de diseño: el enunciado pide insertar huérfanos en askaro_lexico con
# forma_ganadora=NULL, pero la columna es NOT NULL y la FK exige existencia
# en lexico. Para NO modificar el esquema de fase 1 ni violir restricciones,
# los huérfanos se registran en la tabla espejo askaro_huerfanos (mismas
# columnas, sin FK) y se reportan también en huerfanos.csv.
lex.execute("""
CREATE TABLE IF NOT EXISTS askaro_huerfanos (
    id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    concepto_es            TEXT    NOT NULL UNIQUE,
    forma_askara_actual    TEXT    NOT NULL,
    codigo_askaro          TEXT    NOT NULL,
    categoria              TEXT    NOT NULL,
    familia                TEXT    NOT NULL,
    nota                   TEXT,
    fecha_cruce            TEXT    NOT NULL DEFAULT (datetime('now'))
) STRICT
""")

covered = {strip_acc(r[0]) for r in
           lex.execute("SELECT DISTINCT español FROM askaro_lexicon")}
matched = {strip_acc(r[0]) for r in
           lex.execute("SELECT concepto_es FROM askaro_lexico")} | \
          {strip_acc(c) for (c, *_ ) in final}

huérfanos = []
seen_h = set()
for r in lex.execute("SELECT codigo, forma, español, categoria, familia, "
                     "status_original, frecuencia, origen_etimologia "
                     "FROM askaro_lexicon"):
    cod, forma, esp, cat, fam, st, frec, orig = r
    ke = strip_acc(esp)
    if ke in matched or ke in seen_h:
        continue
    # SIN filtro por categoria gramatical: en V11.x la columna `categoria`
    # guarda el tema semántico (Familia, Casa, Naturaleza...), no Sustantivo/
    # Verbo/Adjetivo; filtrar por eso dejaría 0 huérfanos. Se excluyen solo
    # las clases funcionales identificables por el prefijo ASK-* del código.
    mcat = re.match(r"ASK-([A-Z]+)-", cod or "")
    if mcat and mcat.group(1) in ("ADV", "ADJ", "NUM", "CC", "PP", "INT"):
        continue
    # SIN filtro de familia: las familias del enunciado (ak/fo/ter...) no
    # existen como columnas en el lexicon V11.x; filtrar por ellas dejaría
    # solo 6 huérfanos artificiales. Se reportan todos los sust./verb./adj.
    seen_h.add(ke)
    fam_ok = fam if fam != "gen" else (familia_por_raiz(None, orig) or "gen")
    nucleo = (frec or "") in ("1", "2", "núcleo")
    prio = "alta" if (st == "Canon" and nucleo) else \
           ("media" if st in ("Canon", "Pendiente") else "baja")
    huérfanos.append((esp, forma, cod, cat, fam_ok,
                      f"existe en Askáro V11.x pero no en fase 1; prioridad {prio}"))

lex.executemany(
    "INSERT OR IGNORE INTO askaro_huerfanos (concepto_es, forma_askara_actual,"
    " codigo_askaro, categoria, familia, nota) VALUES (?,?,?,?,?,?)",
    [(h[0], h[1], h[2], h[3], h[4], h[5]) for h in huérfanos])

print(f"[paso5] huerfanos={len(huérfanos)}")
lex.commit()

# --------------------------------------------------------------------------
# PASO 6 — verificación (10 checks)
# --------------------------------------------------------------------------
checks = {}
checks["total_askaro_lexico"] = lex.execute(
    "SELECT COUNT(*) FROM askaro_lexico").fetchone()[0]
checks["status_dist"] = lex.execute(
    "SELECT status, COUNT(*) FROM askaro_lexico GROUP BY status").fetchall()
checks["faltantes_de_lexico"] = lex.execute(
    "SELECT COUNT(*) FROM lexico l LEFT JOIN askaro_lexico a "
    "ON l.concepto_es=a.concepto_es WHERE a.concepto_es IS NULL").fetchone()[0]
checks["huerfanos_total"] = lex.execute(
    "SELECT COUNT(*) FROM askaro_huerfanos").fetchone()[0]
checks["dudosos_total"] = lex.execute(
    "SELECT COUNT(*) FROM askaro_lexico WHERE status='dudoso'").fetchone()[0]
checks["familias_nuevos"] = lex.execute(
    "SELECT familia_askara, COUNT(*) FROM askaro_lexico WHERE status='nuevo' "
    "GROUP BY 1 ORDER BY 2 DESC").fetchall()
checks["integrity"] = lex.execute("PRAGMA integrity_check").fetchone()[0]
checks["fk_violations"] = lex.execute("PRAGMA foreign_key_check").fetchall()

for k, v in checks.items():
    print(f"[check] {k}: {v}")

# --------------------------------------------------------------------------
# PASO 8 — CSVs
# --------------------------------------------------------------------------
conf = lex.execute("""SELECT a.concepto_es, a.forma_ganadora, a.forma_askara_actual,
    l.latin, a.codigo_askaro, a.familia_askara FROM askaro_lexico a
    JOIN lexico l ON l.concepto_es = a.concepto_es WHERE a.status='conflicto'
    ORDER BY a.concepto_es""").fetchall()
with open(OUT_CONFLICTOS, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["concepto_es", "forma_ganadora", "forma_askara_actual",
                "raiz_romance", "raiz_askara", "familia", "decision_sugerida"])
    for ce, fg, fa, latin, cod, fam in conf:
        w.writerow([ce, fg, fa, latin, cod, fam,
                    "mantener Askáro" if fam in CORE_FAMILIAS else "adoptar romance"])

with open(OUT_HUERFANOS, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["concepto_es", "forma_askara_actual", "familia", "categoria",
                "prioridad_sugerida"])
    for esp, forma, cod, cat, fam, nota in huérfanos:
        prio = re.search(r"prioridad (\w+)", nota).group(1)
        w.writerow([esp, forma, fam, cat, prio])

nuevos = lex.execute("""SELECT l.concepto_es, a.forma_ganadora, a.familia_askara,
    l.emoji FROM lexico l JOIN askaro_lexico a ON a.concepto_es=l.concepto_es
    WHERE a.status='nuevo' ORDER BY l.concepto_es""").fetchall()
with open(OUT_NUEVOS, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["concepto_es", "forma_ganadora", "familia_propuesta", "emoji"])
    for ce, fg, fam, em in nuevos:
        w.writerow([ce, fg, fam or "gen", em])

# --------------------------------------------------------------------------
# PASO 7 — informe
# --------------------------------------------------------------------------
elapsed = time.time() - T0
stats_fam = lex.execute("""
  SELECT a.familia_askara,
         SUM(a.status='integrado'), SUM(a.status='conflicto'),
         SUM(a.status='nuevo'), SUM(a.status='dudoso')
  FROM askaro_lexico a GROUP BY 1 ORDER BY 5 DESC""").fetchall()

con_emoji_lex = lex.execute(
    "SELECT COUNT(*) FROM lexico WHERE emoji IS NOT NULL").fetchone()[0]

lines = []
A = lines.append
A("INFORME DE INTEGRACIÓN ASKÁRO ↔ LÉXICO ROMANCE (FASE 2)")
A("=" * 60)
A("")
A("1. IMPORTACIÓN DEL LEXICON")
A(f"   Fuente: askaro_lexico.db tabla `lexico` (V11.x, 1404 filas).")
A(f"   Adaptación de columnas: id→codigo, termino_askaro→forma, espanol→español,")
A(f"   ingles→ingles, categoria→normalizada, origen_etimologia→familia derivada.")
A(f"   Filas importadas a askaro_lexicon: {imported} (omitidas por UNIQUE: {skipped}).")
A(f"   Familias cubiertas: {', '.join(f'{fam}:{n}' for fam, n in familias)}.")
A(f"   Entradas con emoji: {with_emoji} (el lexicon V11.x NO incluye emojis;")
A(f"   campo emoji = NULL en todas las filas — ver punto 9).")
A("")
A("2. TABLA DE CRUCE askaro_lexico")
A(f"   Filas: {checks['total_askaro_lexico']} (= todos los conceptos de fase 1).")
A(f"   Cubrimiento de lexico: faltantes = {checks['faltantes_de_lexico']} (esperado 0).")
A(f"   Huérfanos registrados en tabla espejo askaro_huerfanos: {checks['huerfanos_total']}")
A("   (DECISIÓN DOCUMENTADA: el enunciado pedía insertar huérfanos en")
A("    askaro_lexico con forma_ganadora=NULL, pero esa columna es NOT NULL y la")
A("    FK exige que concepto_es exista en lexico. Para no tocar el esquema ni")
A("    inventar formas romances, los huérfanos viven en askaro_huerfanos.)")
A("")
A("3. DISTRIBUCIÓN POR STATUS")
for st, n in checks["status_dist"]:
    A(f"   {st:10s}: {n}")
A("")
A("4. CONFLICTOS (raíz/etimología divergente)")
for ce, fg, fa, latin, cod, fam in conf:
    A(f"   - {ce}: romance '{fg}' ({latin}) vs askárico '{fa}' [{cod}, fam {fam}]")
A("")
A("5. NUEVOS (sin entrada en el lexicon)")
for ce, fg, fam, em in nuevos:
    A(f"   - {ce}: '{fg}', familia propuesta {fam or 'gen'} {em}")
A("")
A("6. HUÉRFANOS TOP 30 (ordenados por familia/prioridad)")
top = sorted(huérfanos, key=lambda h: (h[4], h[5]))[:30]
for esp, forma, cod, cat, fam, nota in top:
    A(f"   - {esp} → {forma} [{cod}] fam {fam} ({cat})")
A("")
A("7. DUDOSOS HEREDADOS DE FASE 1")
A(f"   Total marcados: {checks['dudosos_total']} "
  f"(de {len(dudosos)} conceptos en conceptos_dudosos.csv; los demás ya no")
A("   existen en lexico tras la ampliación de fase 1 a 264 filas).")
for ce in sorted(d for d, *_ in [x for x in final if x[3] == 'dudoso']):
    A(f"   - {ce}")
A("")
A("8. ESTADÍSTICAS POR FAMILIA (cruce fase 1)")
A("   familia | integrado | conflicto | nuevo | dudoso")
for fam, i, cf, nv, dd in stats_fam:
    A(f"   {str(fam):8s}| {i} | {cf} | {nv} | {dd}")
A("   Familias sobrerrepresentadas en huérfanos:")
from collections import Counter
cnt = Counter(h[4] for h in huérfanos)
for fam, n in cnt.most_common(8):
    A(f"     {fam}: {n}")
A("")
A("9. ALINEACIÓN DE EMOJIS")
A(f"   askaro_lexicon tiene 0 emojis; lexico.fase1 tiene {con_emoji_lex}.")
A("   Ningún emoji askárico contradice a lexico (no hay nada que comparar).")
A("   Acción sugerida: añadir columna emoji al lexicon V12 tomando lexico.db")
A("   como fuente canónica visual.")
A("")
A("10. TIEMPO DE EJECUCIÓN")
A(f"   {elapsed:.2f} s")
A("")
A("VERIFICACIÓN: integrity_check = %s | foreign_key_check = %s" %
  (checks["integrity"], "limpio" if not checks["fk_violations"] else checks["fk_violations"]))

with open(OUT_INFORME, "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")

print(f"[informe] escrito {OUT_INFORME} ({elapsed:.1f}s)")
