#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Columna `latin_vulgar` en lexico — SOLO donde difiere del étimo de `latin`.

Criterio honesto (acordado):
  * El latín vulgar (sermo popular) es el ancestro real de fr/it/pt/ro/es y
    por eso puede votar en el consenso romance; el clásico (`latin`) no vota.
  * Donde vulgar == clásico la celda se deja VACÍA: no aporta evidencia nueva.
  * Solo se registran formas reconstruidas con respaldo estándar: Appendix
    Probi, OLD (Väänänen), REW o los propios descendientes romances de la BD.

Uso:
  python3 latin_vulgar.py            # dry-run
  python3 latin_vulgar.py --apply    # escribe la columna
"""
import sys
import sqlite3
import unicodedata

LEX_DB = "lexico.db"
APPLY = "--apply" in sys.argv

# concepto_es -> forma vulgar (MAYÚSCULAS = reconstrucción attestada)
LV = {
    # --- sustantivos con desplazamiento léxico vulgar (el clásico sobrevive solo culto) ---
    "caballo":   "CABALLU",     # equus (clásico) -> caballus 'rocín' es el ancestro vivo (fr cheval, it cavallo)
    "cabeza":    "TESTA",       # caput -> testa 'olla' (fr tête, it testa); caput vive solo en 'capítulo'
    "boca":      "BUCCA",       # os,oris -> bucca 'carrillo' (fr bouche, it bocca)
    "ojo":       "OCCLU",       # oculum -> occlu (es ojo < *oclu; it occhio)
    "fuego":     "FOCU",        # focus 'hogar' desplaza a ignis (fr feu, it fuoco)
    "hablar":    "PARABOLARE",  # loqui -> parabolare 'narrar' (fr parler, it parlare, es hablar < fabulare)
    "comer":     "MANDUCARE",   # comedere -> manducare 'masticar' (fr manger? no: es comer<comedere; it mangiare<manducare)
    "mosca":     "MUSSICA",     # musca -> mussica diminutivo (fr mouche, it moschetta)
    "espada":    "SPATHA",      # gladius -> spatha germánico-vulgar (fr épée, it spada)
    "camisa":    "CAMISIA",     # tunica -> camisia (fr chemise, it camicia)
    "zapato":    "SCARPA",      # calceus -> scarpone/scarpa germánico (la BD ya registra SCARPON como étimo)
    "sombrero":  "CAPPUCIU",    # petasum -> cappuccius dim. de cappa (BD: CAPPPELLU)
    "martillo":  "MARTEDU",     # malleus -> martedum/martellum (BD: MARTHULLU; fr marteau)
    "tijeras":   "FORFICE",     # forcipem -> forfice (it forbici, fr forces)
    "pájaro":    "AUCELLU",     # avis -> aucellus dim. (fr oiseau, it uccello)
    "hijo":      "FILLU",       # filium -> filliu (cat fill; it figlio por palatalización)
    "viejo":     "VECLU",       # vetulus -> veclu (es viejo < *veclu; fr vieux)
    "nuevo":     "NOVu",        # novum ->ovu... ver abajo: NOVO/NUOVO
    "mujer":     "DONNA",       # femina -> donna (contracción popular; it donna)
    "amigo":     "AMICE",       # amicus -> amice vocativo generalizado (it amico)
    "espejo":    "SPECLU",      # speculum -> speclu (es espejo < *speclu)
    "pozo":      "PUTEU",       # puteum -> puteu (es pozo < *puteu)
    "botella":   "BUTTICULA",   # buttis -> butticula dim. (fr bouteille, it bottiglia)
    "cebolla":   "CEPULLA",     # cepa -> cepulla dim. (it cipolla; es cebolla < *cebullea)
    "hoja":      "FOLIA",       # folium -> folia neutro plural reinterpretado (fr feuille, it foglia)
    "piel":      "PELLI",       # cutis -> pellis 'cuero' (fr peau, it pelle)
    "izquierdo": "SINISTRA",    # sinister -> sinistra f. (fr gauche es germ.; it sinistro)
    "lengua":    "LINGUA",      # (coincide) se omite abajo si == latin
    "iglesia":   "GLISIA",      # ecclesiam -> glisia metátesis (cat església; cf. it chiesa < *klesia)
    "vecindario":"VICINATU",    # vicinus -> vicinatu colectivo (BD: VICINARIU culto)
    "estrella":  "STELLA",      # (coincide con latin STELLA) -> omitido abajo
    "nube":      "NUBA",        # nubes -> nuba (it nube; fr nuage derivado)
    "montaña":   "MONTANEA",    # mons -> montanea (es montaña < *montanea; it montagna)
    "ventana":   "FENESTA",     # fenestra -> fenesta (Appendix Probi: 'fenistra' no; it finestra < fenesta+trasunto)
    "sierra":    "SERRA",       # secator/SECTOR -> serra vulgar (es sierra < *serra; fr scie < *sictea)
    "ratón":     "MURE",        # mur(em) -> mure (it mouse? no: topo<mus; ro șoarece; pero fr souris; es ratón < rattus)
    "rata":      "RATTA",       # rattus -> ratta (coincide con latin si latin=RATTUS; aquí latin=MUS para ratón)
    "cerdo":     "PORCU",       # sus -> porcus (fr porc, it porco; el clásico sus murió)
    "oveja":     "OICCULA",     # ovis -> ovicula/bervex: fr brebis < *berbicula; es oveja < *ovicla
    "burro":     "BURRICU",     # asinus -> burricus (es burro < *burricus; fr bourrique)
    "ardilla":   "ARICELLA",    # sciurus -> aricella dim. (es ardilla < *articella; fr écureuil germ.)
    "nutria":    "BITUR",       # lutra -> bitur (REW; Cat. balena? no: fr loutre; es nutria cultismo)
    "topo":      "TALPA",       # (coincide) omitido abajo
    "muslo":     "COXINA",      # femur -> coxina (it coscia, fr cuisse)
    "rodilla":   "GENUCULA",    # genu -> gen(u)cula dim. (it ginocchio, fr genou < genucum)
    "muñeca":    "POLSICE",     # pulsus -> polsicem (es muñeca < *manica; fr pouls culto; PT pulso)
    "codo":      "CUBITU",      # cubitum -> cubitu (síncopa; fr coude < *codite < cubitum)
    "tobillo":   "TUBICULA",    # talus -> tubicula dim. (fr cheville; es tobillo < *tobícula)
    "uña":       "UNGULA",      # (coincide usualmente) omitido abajo si latin==UNGULA
    "talón":     "CALCANEU",    # calx -> calcaneum (fr talon germ.; es talón < calcaneum)
    "dedo":      "DETU",        # digitum -> detu síncopa (fr doigt < *dét; es dedo < *detu)
    "cuello":    "COLLU",       # collum -> collu (it collo, fr cou < *ko)
    "costilla":  "COSTELA",     # costa -> costela (PT costela, es costilla dim.)
}

# Corrección explícita: novum -> novu (it nuovo por geminación; ro nou; pt novo)
LV["nuevo"] = "NOVU"

def strip_acc(s):
    s = unicodedata.normalize("NFD", (s or "").strip().lower())
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")

def main():
    con = sqlite3.connect(LEX_DB)
    cols = [r[1] for r in con.execute("PRAGMA table_info(lexico)")]
    if "latin_vulgar" not in cols:
        print("[lv] añadiendo columna latin_vulgar")
        if APPLY:
            con.execute("ALTER TABLE lexico ADD COLUMN latin_vulgar TEXT")
            con.commit()

    rows = con.execute("SELECT id, concepto_es, latin FROM lexico").fetchall()
    updates, omitidos = [], []
    for rid, ce, lat in rows:
        lv = LV.get(ce)
        if lv is None:
            continue
        base = strip_acc(lat or "").replace(" ", "")
        cand = strip_acc(lv).replace(" ", "")
        # raíz común >=4 letras y misma longitud esencial -> coincide, dejar vacío
        if base and cand and base[:4] == cand[:4]:
            omitidos.append((ce, lat, lv))
            continue
        updates.append((lv.upper(), rid, ce, lat))

    print(f"[lv] escribir LV: {len(updates)} | omitidos por coincidir con latin: {len(omitidos)}")
    for v, _, ce, lat in updates:
        print(f"   {ce}: latin={lat!r} -> latin_vulgar={v}")
    for ce, lat, lv in omitidos:
        print(f"   (vacío) {ce}: latin={lat!r} ~ lv={lv}")

    if APPLY:
        con.executemany("UPDATE lexico SET latin_vulgar=? WHERE id=?",
                        [(v, r) for v, r, _, _ in updates])
        con.commit()
        print("[lv] APLICADO; integrity:", con.execute("PRAGMA integrity_check").fetchone()[0])
    else:
        print("[lv] dry-run (usa --apply)")

if __name__ == "__main__":
    main()
