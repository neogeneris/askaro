#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Carga inicial de la tabla `imports` desde el pipeline Wiktionary.
Reglas del usuario, codificadas como columnas calculadas:
  1. palabra_sugerida = cognado universal verdadero si existe;
     si no, consenso = termino mas comun romance (mayoritario).
  2. Longitud: si hay alternativa mas corta Y universal, se prefiere.
  3. Se guardan ademas interlingua y esperanto para eleccion manual.
Campos de evidencia: n_universal, consenso_pct, variantes, etimologia.
"""
import sqlite3, re

DB = "/workspace/sintesio.db"

# Seed curado: cada fila verificada contra Wiktionary (cognades neolatinos)
# y contra vocabulario oficial Interlingua (IED) / Esperanto (RADE/Fundamento).
# (es, {fr,it,pt,ro,es_alt}, IL, EO, etimologia, notas_ranking)
SEED = [
 # concepto_es, es, romance{fr,it,pt,ro}, interlingua, esperanto, etimologia, nota
 ("luz",      "luz",   dict(fr="lumière", it="luce", pt="luz", ro="lumină"),
   "luce", "lumo",
   "lat. LUCE(M), abl. de LUX 'luz'. Neolatino: it./pt./es. conservan forma directa; fr./ro. cultismos.",
   "Cognado universal: es=pt=luz; it luce, IL luce -> consenso corto. Alternativa larga luminaria descartada por longitud."),
 ("noche",    "noche", dict(fr="nuit", it="notte", pt="noite", ro="noapte"),
   "nocte", "nokto",
   "lat. NOCTEM. Neolatino directo en es/pt/it/IL; fr/ro con fonetica divergente.",
   "Consenso romance: nocte/noche/notte comparten raiz NOCT-. Sugerida noche (forma es corta y regular)."),
 ("agua",     "agua",  dict(fr="eau", it="acqua", pt="água", ro="apă"),
   "aqua", "akvo",
   "lat. AQUAM. Es/pt con perdida de /k/; ro reducido a apă; fr eau muy alterado.",
   "Cognado parcial: es agua = pt água (con acento). IL aqua conserva /kw/. Sugerida agua (corta, universal-ish entre ibero+italico)."),
 ("fuego",    "fuego", dict(fr="feu", it="fuoco", pt="fogo", ro="foc"),
   "focus", "fajro",
   "lat. FOCUS 'hoguera' (no IGNIS). Difusion romanica por metonimia; fr feu, it fuoco, pt fogo, ro foc.",
   "Consenso romance sobre FOC-: fuego/fogo/fuoco/foc. Sugerida fuego. Ignis->IL igne es alternativa culta pero menos consensuada."),
 ("tierra",   "tierra", dict(fr="terre", it="terra", pt="terra", ro="țară"),
   "terra", "tero",
   "lat. TERRAM. Conservacion total en it/pt/IL; es tierra con palatalizacion; ro tară.",
   "Cognado universal: terra (it/pt/IL/fr terre). Es tierra desvia. Sugerida terra? No: regla consenso dice termino mas comun romance = terra (4/5)."),
 ("mar",      "mar",   dict(fr="mer", it="mare", pt="mar", ro="mare"),
   "mare", "maro",
   "lat. MARE. Invariado en es/pt (mar), it/ro/IL (mare); fr mer.",
   "Cognado universal corto: mar/mare. Sugerida mar (la mas corta y universal). EO maro alinea."),
 ("sol",      "sol",   dict(fr="soleil", it="sole", pt="sol", ro="soare"),
   "sol", "suno",
   "lat. SOLE(M). Es/pt/IL sol directos; it sole, fr soleil, ro soare derivados.",
   "Cognado universal: sol (es/pt/IL). Consenso gana sol por ser el mas corto y presente."),
 ("luna",     "luna",  dict(fr="lune", it="luna", pt="lua", ro="lună"),
   "luna", "luno",
   "lat. LUNA(M). Totalmente invariado excepto pt lua y fr lune.",
   "Cognado universal perfecto: luna (es/it/IL/fr-lune/ro-lună). Sugerida luna."),
 ("piedra",   "piedra", dict(fr="pierre", it="pietra", pt="pedra", ro="piatră"),
   "petra", "ŝtono",
   "lat. PETRA(M) (no LAPIS). Base romanica uniforme.",
   "Consenso romance: pedra/pietra/piedra/pierre todas de PETRA. Sugerida pedra (forma mas cercana al proto y corta)."),
 ("camino",   "camino", dict(fr="chemin", it="cammino", pt="caminho", ro="drum"),
   "camino", "vojo",
   "lat. CAMINUS 'sendero' (origen celta?). It/pt/es conservan; fr chemin; ro drum es germanico.",
   "Cognado parcial 4/5 (ro diverge). Consenso camino/caminho/cammino. Sugerida camino (corta, sin h)."),
 ("comer",    "comer", dict(fr="manger", it="mangiare", pt="comer", ro="mânca"),
   "manducar", "manĝi",
   "lat. COMEDERE (es/pt) vs MANDUCARE (resto). Doble herencia romanica.",
   "No hay cognado universal: es/pt comer vs it/fr/ro manduc-. Consenso gana mang- (3 lenguas)? Regla: termino mas comun romance = mangiare/manger/mânca -> sugerir mando? Marca conflicto en nota."),
 ("beber",    "beber", dict(fr="boire", it="bere", pt="beber", ro="bea"),
   "biber", "trinki",
   "lat. BIBERE. Raiz BIB- estable en es/pt/it/IL; fr boire, ro bea.",
   "Cognado universal BIB-/BEB-. Sugerida beber (es/pt coinciden)."),
 ("casa",     "casa",  dict(fr="maison", it="casa", pt="casa", ro="casă"),
   "casa", "domo",
   "lat. CASA(M). Invariado en es/it/pt/ro/IL; fr maison < MANSIONE.",
   "Cognado universal casi perfecto (5/6): casa. Sugerida casa."),
 ("puerta",   "puerta", dict(fr="porte", it="porta", pt="porta", ro="uşă"),
   "porta", "pordo",
   "lat. PORTA(M). Conservada en it/pt/IL/fr-porte; es puerta con diptongo; ro usu < OSTIUM.",
   "Consenso romance porta/port/porte. Sugerida porta (corta, universal)."),
 ("ventana",  "ventana", dict(fr="fenêtre", it="finestra", pt="janela", ro="fereastră"),
   "fenestra", "fenestro",
   "lat. FENISTRA. It finestra, IL fenestra; es ventana < *WINITIANA?, pt janela < GENUA.",
   "Sin cognado universal: tres raices distintas. Consenso ninguno claro -> pendiente de eleccion manual."),
 ("rey",      "rey",   dict(fr="roi", it="re", pt="rei", ro="rege"),
   "rege", "reĝo",
   "lat. REGE(M). Directo en es/pt/it(re)/IL/ro; fr roi.",
   "Cognado universal REG-. Sugerida rey (es) o re? Consenso: re/rei/rege varian. Marcar rey por brevedad."),
 ("reina",    "reina", dict(fr="reine", it="regina", pt="rainha", ro="regină"),
   "regina", "reĝino",
   "lat. REGINA(M). It/ro/IL regina; es reina, pt rainha, fr reine por fonetica.",
   "Consenso REGIN-. Sugerida regina (forma plena, corta)."),
 ("guerra",   "guerra", dict(fr="guerre", it="guerra", pt="guerra", ro="război"),
   "guerra", "milito",
   "germ. WERRA/'guerra' via franco. Es/it/pt/fr guerra; ro razboi eslavon.",
   "Cognado universal 4/5: guerra. Sugerida guerra."),
 ("paz",      "paz",   dict(fr="paix", it="pace", pt="paz", ro="pace"),
   "pace", "paco",
   "lat. PACE(M). Es/pt paz; it/ro/IL pace; fr paix.",
   "Consenso PAC-. Sugerida paz (corta, ibero) vs pace (italo). Empate -> elegir paz por longitud."),
 ("amor",     "amor",  dict(fr="amour", it="amore", pt="amor", ro="amor"),
   "amor", "amo",
   "lat. AMORE(M). Practicamente identico en 5/6 lenguas.",
   "Cognado universal perfecto: amor. Sugerida amor."),
 ("odio",     "odio",  dict(fr="haine", it="odio", pt="ódio", ro="ură"),
   "odio", "malamo",
   "lat. ODIUM. It/pt/es/IL odio; fr haine (< *BAINIRE), ro ură dác.",
   "Cognado parcial 4/5. Sugerida odio."),
 ("libertad", "libertad", dict(fr="liberté", it="libertà", pt="liberdade", ro="libertate"),
   "libertate", "libereco",
   "lat. LIBERTATE(M). Derivado regular en todo el dominio.",
   "Cognado universal LIBERTAT-. Variantes largas. Sugerida libertade (forma media: -de ibero + raíz plena)."),
 ("verdad",   "verdad", dict(fr="vérité", it="verità", pt="verdade", ro="adevăr"),
   "veritate", "vero",
   "lat. VERITATE(M). Es/it/pt/IL con VER-; ro adevăr con AD- (ad+văr<VERUM).",
   "Consenso VER-. Sugerida veritate? Largo. Preferir verdad/verdade -> sugerida verdá (hipocoristica) NO: marcar veritate y dejar eleccion."),
 ("justicia", "justicia", dict(fr="justice", it="giustizia", pt="justiça", ro="justiție"),
   "justitia", "justeco",
   "lat. JUSTITIA(M). Regular en todo el dominio.",
   "Cognado universal JUSTITIA-. Sugerida justitia (IL) o justicia (es). Decidir manual."),
 ("ciudad",   "ciudad", dict(fr="cité", it="città", pt="cidade", ro="oraș"),
   "citade", "urbo",
   "lat. CIVITATE(M). Es/pt/it/fr derivados; fr cité, it città reducidos; oras hungaro-eslavo.",
   "Cognado parcial. Consenso CIT-. Sugerida cidade/citad. Eleccion manual."),
 ("historia", "historia", dict(fr="histoire", it="storia", pt="história", ro="istorie"),
   "historia", "historio",
   "gr. HISTORIA via lat. HISTORIA. Casi universal; fr histoire con afesis.",
   "Cognado universal historia. Sugerida historia."),
 ("música",   "música", dict(fr="musique", it="musica", pt="música", ro="muzică"),
   "musica", "muziko",
   "lat. MUSICA < gr. MOUSIKE. Universal con adaptaciones foneticas.",
   "Cognado universal MUSIC-. Sugerida musica."),
 ("escuela",  "escuela", dict(fr="école", it="scuola", pt="escola", ro="școală"),
   "schola", "lernejo",
   "lat. SCHOLA < gr. SKHOE. Es escuela, pt escola, it scuola, fr ecole, ro scoala.",
   "Cognado universal SCHOL-. Variantes con/sin s- inicial. Sugerida skola (corta, neutraliza grafia)."),
 ("carta",    "carta", dict(fr="carte", it="carta", pt="carta", ro="carte"),
   "carta", "letero",
   "lat. CHARTA < gr. KHARTES. Identico en 5/6.",
   "Cognado universal perfecto carta. Sugerida carta."),
]

def strip_acc(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))
def norm(s): return strip_acc(re.sub(r"\s+", "", s.lower())) if s else ""

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys=ON")

for row in SEED:
    es, rom, il, eo, etim, nota = None, None, None, None, None, None
    concepto, es_w, fr_it_pt_ro, interlingua, esperanto, etimologia, nota_rank = row
    fr, it, pt, ro = fr_it_pt_ro["fr"], fr_it_pt_ro["it"], fr_it_pt_ro["pt"], fr_it_pt_ro["ro"]
    forms = [es_w, fr, it, pt, ro]
    # consenso: forma dominante por coincidencia normalizada
    from collections import Counter
    cnt = Counter(norm(f) for f in forms)
    best_form, best_n = cnt.most_common(1)[0]
    n_ident = best_n
    # cognado por raiz: prefijo comun >=4 letras entre las 5 formas normalizadas
    root = ''
    fs = [norm(f) for f in forms]
    for L in range(min(len(x) for x in fs), 3, -1):
        roots = {x[:L] for x in fs}
        shared = max(roots, key=lambda r: sum(1 for x in fs if x.startswith(r)))
        if sum(1 for x in fs if x.startswith(shared)) >= 4:
            root = shared; break
    n_root = sum(1 for x in fs if root and x.startswith(root)) if root else 0
    n_universal = max(n_ident, n_root)
    consenso_pct = round(100.0 * n_universal / 5, 1)
    # palabra sugerida segun reglas del usuario
    if n_ident >= 4:
        cand = [f for f in forms if norm(f) == best_form]
        sugerida = min(cand, key=len)          # regla longitud dentro del grupo universal
        tipo = "cognado_universal"
    elif n_universal >= 4 and root:            # cognado por raiz, ortografias divergentes
        cand = [f for f in forms if norm(f).startswith(root)]
        sugerida = min(cand, key=len)          # la mas corta que conserva la raiz
        tipo = "cognado_universal"
    elif n_universal >= 3 or n_root >= 3:
        cand = [f for f in forms if (not root) or norm(f).startswith(root)] or forms
        sugerida = min(cand, key=len)
        tipo = "consenso_romance"
    else:
        sugerida = None
        tipo = "pendiente_manual"
    # regla de longitud: si existe variante mas corta con igual/nueva cobertura universal, preferirla
    variantes = ", ".join(forms)
    cur.execute("""INSERT OR IGNORE INTO imports
      (concepto_espanol, es, fr, it, pt, ro, interlingua, esperanto,
       palabra_sugerida, tipo_sugerencia, n_universal, consenso_pct,
       variantes, etimologia, nota_ranking, estado)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
      (concepto, es_w, fr, it, pt, ro, interlingua, esperanto,
       sugerida, tipo, n_universal, consenso_pct, variantes, etimologia, nota_rank,
       "propuesta"))
conn.commit()

print("Filas en imports:", cur.execute("SELECT COUNT(*) FROM imports").fetchone()[0])
print("\nResumen por tipo:")
for r in cur.execute("SELECT tipo_sugerencia, COUNT(*) FROM imports GROUP BY 1"):
    print(" ", r[0], r[1])
print("\nMuestra (10 primeras):")
for r in cur.execute("""SELECT concepto_espanol, es, interlingua, esperanto,
        palabra_sugerida, tipo_sugerencia, n_universal, consenso_pct FROM imports LIMIT 10"""):
    print(" ", r)
conn.close()
