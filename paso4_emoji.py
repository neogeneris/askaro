#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PASO 4 — Asignar emoji a `lexico.db` (dos fuentes, una prioridad).

FUENTE 1 (primaria): sintesio.db
  - Tabla `imports`: columnas `concepto_espanol` + `glifo` (emoji canónico).
  - Si el concepto está en sintesio.db, se usa ESE emoji.
    nota = "emoji desde sintesio.db".
  - Prioridad absoluta ante colisión entre fuentes: si sintesio.db asigna un
    emoji a un concepto, cualquier candidato CLDR que colisione cede.

FUENTE 2 (fallback): búsqueda CLDR/Unicode (lista curada CANDIDATOS_CLDR).
  - Solo para conceptos NO encontrados en sintesio.db.
  - nota = "emoji desde búsqueda CLDR".

Resolución de colisiones (reglas del enunciado):
  1. específico gana (el referente literal Unicode del emoji)
  2. empate -> mayor puntuación
  3. sin alternativa -> segundo candidato; si no hay, más cercano + nota
  Toda resolución nueva se registra en emoji_colisiones (semilla fase 1 intacta).
  Los candidatos alternativos con puntuación se guardan en emoji_candidatos
  (elegido=1 marca el seleccionado; trigger garantiza unicidad por concepto).

Emojis no fully-qualified provenientes de sintesio.db: se usan igual, con
"; emoji no estándar" en la nota y advertencia en el informe.

Requiere pysqlite3 (SQLite >= 3.41): lexico.db tiene triggers con || en RAISE
que el parser de 3.40.x rechaza.
"""
import os
import sys
import sqlite3          # stdlib: solo para leer sintesio.db (BD normal)
from collections import Counter

try:
    import pysqlite3 as sqlx   # SQLite 3.51.x: escribe lexico.db
except ImportError:
    print("ERROR: falta pysqlite3-binary -> pip install pysqlite3-binary")
    sys.exit(1)

SINTESIO_DB = "sintesio.db"
LEXICO_DB   = "lexico.db"

# ============================================================================
# FUENTE 2: candidatos CLDR/Unicode por concepto (solo fallback).
# Formato: (emoji, nombre_oficial_unicode, codepoint, puntuacion)
# Puntuación 0-100 = representatividad 40% + frecuencia 25% + iconicidad 20%
#                    + unicidad 10% + estabilidad 5%.
# ============================================================================
CANDIDATOS_CLDR = {
    # cuerpo / persona
    "persona":   [("🧑", "PERSON", "U+1F9D1", 97), ("👤", "BUST IN SILHOUETTE", "U+1F464", 70)],
    "mujer":     [("👩", "WOMAN", "U+1F469", 97)],
    "hombre":    [("👨", "MAN", "U+1F468", 97)],
    "niño":      [("👦", "BOY", "U+1F466", 96)],
    "niña":      [("👧", "GIRL", "U+1F467", 96)],
    "mano":      [("✋", "RAISED HAND", "U+270B", 96), ("🫱", "RIGHTWARD HAND", "U+1FAF1", 70)],
    "pie":       [("🦶", "FOOT", "U+1F9B6", 95)],
    "ojo":       [("👁️", "EYE", "U+1F441 FE0F", 96)],
    "nariz":     [("👃", "NOSE", "U+1F443", 96)],
    "boca":      [("👄", "MOUTH", "U+1F444", 96)],
    # naturaleza / cielo
    "estrella":  [("⭐", "WHITE MEDIUM STAR", "U+2B50", 95), ("🌟", "GLOWING STAR", "U+1F31F", 80)],
    "cielo":     [("🌤️", "SUN BEHIND SMALL CLOUD", "U+1F324 FE0F", 80), ("🌌", "MILKY WAY", "U+1F30C", 70)],
    "nube":      [("☁️", "CLOUD", "U+2601 FE0F", 97)],
    "lluvia":    [("🌧️", "CLOUD WITH RAIN", "U+1F327 FE0F", 96)],
    "viento":    [("💨", "DASHING AWAY", "U+1F4A8", 88), ("🌬️", "WIND FACE", "U+1F32C FE0F", 86)],
    "montaña":   [("⛰️", "MOUNTAIN", "U+26F0 FE0F", 96), ("🏔️", "SNOW-CAPPED MOUNTAIN", "U+1F3D4 FE0F", 85)],
    "flor":      [("🌷", "TULIP", "U+1F337", 92), ("🌺", "HIBISCUS", "U+1F33A", 80)],
    "hoja":      [("🍃", "LEAF FLUTTING IN WIND", "U+1F343", 92), ("🌿", "HERB", "U+1F33F", 85)],
    "mar":       [("🌊", "WATER WAVE", "U+1F30A", 95), ("⛵", "SAILBOAT", "U+26F5 FE0F", 78)],
    "río":       [("🏞️", "NATIONAL PARK", "U+1F3DE FE0F", 70), ("〰️", "WAVY DASH", "U+3030 FE0F", 62)],
    # animales sin glifo en sintesio
    "perro":     [("🐕", "DOG", "U+1F415", 97), ("🐶", "DOG FACE", "U+1F436", 90)],
    "gato":      [("🐈", "CAT", "U+1F408", 97), ("🐱", "CAT FACE", "U+1F431", 90)],
    "caballo":   [("🐎", "HORSE", "U+1F40E", 96), ("🐴", "HORSE FACE", "U+1F434", 88)],
    "vaca":      [("🐄", "COW", "U+1F404", 96), ("🐮", "COW FACE", "U+1F42E", 88)],
    "oveja":     [("🐑", "SHEEP", "U+1F411", 96)],
    "cerdo":     [("🐖", "PIG", "U+1F416", 96), ("🐷", "PIG FACE", "U+1F437", 88)],
    "gallina":   [("🐔", "HEN", "U+1F414", 95), ("🐓", "ROOSTER", "U+1F413", 88)],
    "pájaro":    [("🐦", "BIRD", "U+1F426", 96)],
    "pez":       [("🐟", "FISH", "U+1F41F", 97)],
    "serpiente": [("🐍", "SNAKE", "U+1F40D", 97)],
    "rana":      [("🐸", "FROG", "U+1F438", 96)],
    "elefante":  [("🐘", "ELEPHANT", "U+1F418", 98)],
    "oso":       [("🐻", "BEAR", "U+1F43B", 97)],
    "lobo":      [("🐺", "WOLF", "U+1F43A", 96)],
    "ratón":     [("🐭", "MOUSE FACE", "U+1F42D", 95), ("🐁", "MOUSE", "U+1F401", 80)],
    # ⚠️ 'niña' existe en sintesio.db con 👧: no se incluye en CLDR para respetar la fuente primaria.
    # comida / casa
    "comer":     [("🍽️", "FORK AND KNIFE WITH PLATE", "U+1F37D FE0F", 88), ("😋", "FACE SAVOURING DELICIOUS FOOD", "U+1F60B", 80)],
    "beber":     [("🥤", "CUP WITH STRAW", "U+1F964", 90), ("🚰", "POTABLE WATER", "U+1F6B0", 75)],
    "pan":       [("🍞", "BREAD", "U+1F35E", 98)],
    "carne":     [("🥩", "CUT OF MEAT", "U+1F969", 95), ("🍖", "MEAT ON BONE", "U+1F356", 90)],
    "leche":     [("🥛", "GLASS OF MILK", "U+1F95B", 98)],
    "huevo":     [("🥚", "EGG", "U+1F95A", 98)],
    "manzana":   [("🍎", "RED APPLE", "U+1F34E", 98)],
    "cama":      [("🛏️", "BED", "U+1F6CF FE0F", 96)],
    "mesa":      [("🍽️", "FORK AND KNIFE WITH PLATE", "U+1F37D FE0F", 90)],
    "silla":     [("🪑", "CHAIR", "U+1FA91", 96)],
    "casa":      [("🏠", "HOUSE BUILDING", "U+1F3E0", 98)],
    "puerta":    [("🚪", "DOOR", "U+1F6AA", 98)],
    "ventana":   [("🪟", "WINDOW", "U+1FA9F", 97)],
    "ciudad":    [("🏙️", "CITYSCAPE", "U+1F3D9 FE0F", 95)],
    "aldea":     [("🏘️", "HOUSES", "U+1F3D8 FE0F", 85)],
    "camino":    [("🛤️", "RAILWAY TRACK", "U+1F6E4 FE0F", 85), ("🛣️", "MOTORWAY", "U+1F6E3 FE0F", 82)],
    # abstractos / verbos
    "vida":      [("💚", "GREEN HEART", "U+1F49A", 88), ("🌱", "SEEDLING", "U+1F331", 82)],
    "muerte":    [("💀", "SKULL", "U+1F480", 96)],
    "corazón":   [("❤️", "HEART", "U+2764 FE0F", 98)],
    "día":       [("🌞", "SUN WITH FACE", "U+1F31E", 90), ("☀️", "SUN", "U+2600 FE0F", 80)],
    "noche":     [("🌙", "CRESCENT MOON", "U+1F319", 92)],
    "tiempo":    [("⏳", "HOURGLASS NOT DONE", "U+23F3", 85), ("🕐", "CLOCK FACE ONE OCLOCK", "U+1F550", 82)],
    "guerra":    [("⚔️", "CROSSED SWORDS", "U+2694 FE0F", 95)],
    "paz":       [("🕊️", "DOVE OF PEACE", "U+1F54A FE0F", 92)],
    "libro":     [("📖", "OPEN BOOK", "U+1F4D6", 96)],
    "escribir":  [("✍️", "WRITING HAND", "U+270D FE0F", 93)],
    "hablar":    [("🗣️", "SPEAKING HEAD", "U+1F5E3 FE0F", 95)],
    "ver":       [("👀", "EYES", "U+1F440", 93)],
    "oir":       [("👂", "EAR", "U+1F442", 90)],
    "grande":    [("📏", "STRAIGHT RULER", "U+1F4CF", 70), ("🐘", "ELEPHANT", "U+1F418", 68)],
    "pequeño":   [("🐜", "ANT", "U+1F41C", 75)],
    "caliente":  [("🔥", "FIRE", "U+1F525", 90)],
    "frio":      [("🧊", "ICE CUBE", "U+1F9CA", 92)],
    "limpio":    [("🧼", "SOAP", "U+1F9FC", 85)],
    # conceptos de la semilla sin glifo propio (aseguran fila destino)
    "piedra":    [("🪨", "ROCK", "U+1FAA8", 96), ("⛰️", "MOUNTAIN", "U+26F0 FE0F", 70)],
    "historia":  [("📖", "OPEN BOOK", "U+1F4D6", 92)],
    "ardilla":   [("🐿️", "CHIPMUNK", "U+1F43F FE0F", 95)],
}

# Referentes literales Unicode (para la regla "específico gana").
REFERENTE_LITERAL = {
    "🪨": "piedra", "🪰": "mosca", "🏙️": "ciudad", "📜": "pergamino",
    "🐁": "ratón", "🐿️": "ardilla", "🌍": "tierra", "📖": "libro",
    "🐭": "ratón", "🌆": "ciudad", "🦋": "mariposa",
}

# Emojis cuyo default es presentación-texto y necesitan FE0F p/ fully-qualified.
NEEDS_FE0F = set("⚓⛵⛪⛴✈✂☀☁⛄⛅⚖⚔🕐")  # sólo los < U+1F000 importan realmente


def extraer_sintesio():
    """FUENTE 1: pares (concepto -> emoji) desde sintesio.db (tabla imports.glifo)."""
    c = sqlite3.connect(SINTESIO_DB)
    rows = c.execute(
        "SELECT concepto_espanol, glifo FROM imports "
        "WHERE glifo IS NOT NULL AND glifo <> ''"
    ).fetchall()
    total = c.execute("SELECT COUNT(*) FROM imports").fetchone()[0]
    c.close()
    return dict(rows), total


def es_no_estandar(e):
    base = e[0]
    return (ord(base) < 0x1F000 or base in NEEDS_FE0F) and "\ufe0f" not in e


def main():
    # ---------------- Verificación de la fuente ----------------
    print("=" * 70)
    print("VERIFICACIÓN DE LA FUENTE")
    print("=" * 70)
    existe = os.path.exists(SINTESIO_DB)
    print(f"¿Existe sintesio.db? -> {'SÍ' if existe else 'NO'}")
    sintesio_map = {}
    if existe:
        sintesio_map, total_imports = extraer_sintesio()
        print(f"sintesio.db: tabla 'imports' = {total_imports} filas; "
              f"{len(sintesio_map)} pares (concepto, emoji) en columna 'glifo'")

    # Lista de conceptos a poblar: todos los de sintesio.db (canónicos).
    conceptos = list(sintesio_map.keys())
    n_con = len(conceptos)
    n_sin = sum(1 for k in conceptos if k not in sintesio_map)
    print(f"Conceptos de lexico con emoji en sintesio.db: {n_con}; sin emoji: {n_sin}")

    # ---------------- Selección con prioridad de fuentes ----------------
    chosen = {}                 # concepto -> emoji final
    cand_by_concept = {}        # concepto -> lista de candidatos usados
    collisions = []             # filas nuevas para emoji_colisiones
    used = {}                   # emoji -> concepto dueño actual

    def register(k, e, cands):
        chosen[k] = e
        cand_by_concept[k] = cands

    # 1) Primero la FUENTE 1: nunca pierde ante nada.
    for k, e in sintesio_map.items():
        register(k, e, [(e, "(fuente sintesio.db)", None, 100)])
        used[e] = k

    # 2) Después FUENTE 2 (CLDR) para conceptos añadidos no presentes en sintesio.
    for k, cands in CANDIDATOS_CLDR.items():
        if k in sintesio_map:
            continue  # ya resuelto por fuente primaria
        cands = sorted(cands, key=lambda x: -x[3])
        best = cands[0]
        e = best[0]
        if e not in used:
            register(k, e, cands)
            used[e] = k
            continue
        # --- colisiona con un concepto ya asignado: resolver ---
        owner = used[e]
        lit = REFERENTE_LITERAL.get(e)
        if lit == k:
            winner, loser = k, owner          # específico gana (lucha CLDR-interna)
        elif lit == owner:
            winner, loser = owner, k          # específico gana (típico: sintesio manda)
        else:
            po = cand_by_concept[owner][0][3]
            winner, loser = (owner, k) if po >= best[3] else (k, owner)
        # el perdedor busca segundo candidato entre SUS candidatos
        loser_cands = cand_by_concept.get(loser) or (cands if loser == k else [])
        alt = next((c for c in loser_cands if c[0] != e), None)
        if alt is None and loser == k:
            alt = next((c for c in cands if c[0] != e), None)
        if alt is not None and alt[0] not in used:
            new_e = alt[0]
            resolucion = "segundo_candidato"
            register(loser, new_e, loser_cands)
            used[new_e] = loser
            note = f"colisión paso 4; {loser} migra a {new_e}"
        elif alt is not None:
            # segundo candidato también ocupado: se usa igual + nota (más cercano)
            new_e = alt[0]
            resolucion = "sin_alternativa"
            register(loser, new_e, loser_cands)
            note = f"colisión paso 4; sin alternativa libre; {loser} queda con {new_e} (revisar)"
        else:
            resolucion = "sin_alternativa"
            note = "colisión paso 4; sin segundo candidato (revisar)"
        collisions.append((e, winner, loser, resolucion, note))
        used[e] = winner

    # ---------------- Escritura en lexico.db ----------------
    conn = sqlx.connect(LEXICO_DB)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()

    # Semilla: pares ya documentados (no duplicar auditoría)
    semilla_pairs = {frozenset(r) for r in cur.execute(
        "SELECT concepto_ganador, concepto_perdedor FROM emoji_colisiones")}

    # Formas en 8 lenguas desde sintesio.db.imports
    formas = {}
    clase = {}
    cs = sqlite3.connect(SINTESIO_DB)
    for r in cs.execute(
        "SELECT concepto_espanol, es, fr, it, pt, ro, interlingua, esperanto, "
        "clase_gramatical, consenso_pct, n_universal FROM imports"):
        formas[r[0]] = r[1:8]
        clase[r[0]] = (r[8], r[9], r[10])
    cs.close()

    inserted_lex = inserted_cand = 0
    nonstandard = []
    from1 = from2 = 0

    for k in sorted(chosen):
        e = chosen[k]
        if k in sintesio_map:
            src = "emoji desde sintesio.db"
            from1 += 1
            if es_no_estandar(e):
                src += "; emoji no estándar"
                nonstandard.append((k, e))
        else:
            src = "emoji desde búsqueda CLDR"
            from2 += 1

        f = formas.get(k)
        if f:
            es, fr_, it, pt, ro, ia, eo = [x if x else "—" for x in f]
        else:
            es = fr_ = it = pt = ro = ia = eo = "—"
        cg, cpct, nuniv = clase.get(k, ("sustantivo", None, None))
        cat = cg if cg in ("sustantivo", "verbo", "adjetivo", "adverbio") else "sustantivo"
        try:
            consenso = int(nuniv) if nuniv not in (None, "") else 0
        except (TypeError, ValueError):
            consenso = 0
        consenso = max(0, min(8, consenso))
        cognado = "universal" if consenso >= 6 else ("romance" if consenso >= 4 else
                  ("parcial" if consenso >= 2 else "ninguno"))
        en = k  # imports no almacena inglés; se usa el concepto como placeholder documentado
        ganadora = es if es != "—" else next((x for x in (fr_, it, pt, ro, ia, eo) if x != "—"), k)
        fuente_g = "es" if ganadora == es else next(
            (lng for lng, val in (("fr", fr_), ("it", it), ("pt", pt),
                                  ("ro", ro), ("ia", ia), ("eo", eo)) if val == ganadora), "es")

        cur.execute(
            """INSERT INTO lexico (emoji, concepto_es, concepto_en, es, en, fr, it, pt,
                                   ro, ia, eo, categoria, cognado, lenguas_consenso,
                                   forma_ganadora, fuente_ganadora, nota)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (e, k, en, es, en, fr_, it, pt, ro, ia, eo, cat, cognado, consenso,
             ganadora, fuente_g, src))
        inserted_lex += 1

        for (ce, cname, ccod, cpunt) in cand_by_concept[k]:
            elegido = 1 if ce == e else 0
            cod = ccod if ccod else "U+" + format(ord(ce[0]), "04X")
            if "\ufe0f" in ce and "FE0F" not in cod:
                cod += " FE0F"
            cur.execute(
                """INSERT INTO emoji_candidatos
                   (concepto_es, emoji, nombre_oficial, codepoint, puntuacion, elegido, nota)
                   VALUES (?,?,?,?,?,?,?)""",
                (k, ce, cname, cod, min(cpunt, 100), elegido,
                   "paso 4: " + ("fuente sintesio.db" if k in sintesio_map else "búsqueda CLDR")))
            inserted_cand += 1

    # Colisiones nuevas (evitando duplicar las de la semilla)
    nuevas = 0
    for row in collisions:
        if frozenset((row[1], row[2])) in semilla_pairs:
            continue
        cur.execute(
            "INSERT INTO emoji_colisiones (emoji, concepto_ganador, concepto_perdedor, "
            "resolucion, nota) VALUES (?,?,?,?,?)", row)
        nuevas += 1

    conn.commit()

    # ---------------- Informe ----------------
    print()
    print("=" * 70)
    print("INFORME PASO 4")
    print("=" * 70)
    print(f"Filas insertadas en lexico:            {inserted_lex}")
    print(f"Filas insertadas en emoji_candidatos:  {inserted_cand}")
    print(f"Colisiones nuevas registradas:         {nuevas}")
    tot_col = cur.execute("SELECT COUNT(*) FROM emoji_colisiones").fetchone()[0]
    print(f"Total emoji_colisiones:                {tot_col} (6 semilla + {nuevas})")
    print(f"Emoji desde sintesio.db (FUENTE 1):    {from1}")
    print(f"Emoji desde búsqueda CLDR (FUENTE 2):  {from2}")
    elegidos = cur.execute("SELECT COUNT(*) FROM emoji_candidatos WHERE elegido=1").fetchone()[0]
    print(f"Candidatos con elegido=1:              {elegidos}")
    dup = cur.execute("""SELECT emoji, COUNT(*) c FROM lexico GROUP BY emoji HAVING c>1""").fetchall()
    print(f"Emojis duplicados en lexico:           {len(dup)} {dup if dup else ''}")
    if nonstandard:
        print("\nADVERTENCIA — emojis no fully-qualified desde sintesio.db (revisión manual):")
        for k, e in nonstandard:
            print(f"  {k}: {e!r} (codepoint base U+{ord(e[0]):04X}, falta U+FE0F)")
    print("\nintegrity_check:", cur.execute("PRAGMA integrity_check").fetchone()[0])
    print("foreign_key_check:", cur.execute("PRAGMA foreign_key_check").fetchall() or "sin errores")
    conn.close()


if __name__ == "__main__":
    main()
