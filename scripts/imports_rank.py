#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ranking final de imports con umbral ESTRICTO de cognado universal.

Cambios vs. version anterior (que sobre-contaba):
  - El detector de raiz usa un ALOFONO-MAPA por raiz proto, no substrings
    genericos. Solo cuenta una variante si su reflejo fonetico regular
    desciende de esa raiz. Ej.: odi- NO cuenta 'haine' ni 'ură';
    cart- NO cuenta 'cité'/'scuola' (son cit-/schol-, otra raiz).
  - Umbral: >=4/5 = cognado_universal; ==3 = consenso_romance; <=2 = pendiente_manual.
  - Regla de longitud del usuario: entre las variantes que conservan la raiz,
    se sugiere la MAS CORTA. Se prefiere siempre una forma que conserva la
    raiz aunque sea mas larga, antes que una forma corta ajena a ella.
Reproducible: python3 scripts/imports_rank.py
"""
import sqlite3, unicodedata, re

DB="/workspace/sintesio.db"

def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if not unicodedata.combining(c))

# raiz proto -> patrones de reflejo ROMANCE legitimos (regex sobre forma normalizada)
ALOFONOS = {
 'luc':   r'^(lum|luc)',            # luz, luce, lumière, lumină
 'noct':  r'^(noc|nui|noap|not)',   # noche/noite, nuit, noapte, notte
 'aqu':   r'^(aq|ag|ap|eau)',       # agua/acqua, apă, eau
 'foc':   r'^(foc|fue|feu)',        # fuego/fogo/fuoco/foc, feu
 'ign':   r'^ig',                   # ignis->IL igne (no usado en seed)
 'terr':  r'^(ter|țar|tar)',        # tierra/terra/terre, țară
 'mar':   r'^mar',                  # mar/mare/mer
 'sol':   r'^sol',                  # sol/sole/soleil/soare
 'lun':   r'^(lun|lua)',            # luna/lune/lua/lună
 'petr':  r'^(pedr|pietr|piedr|pier|piatr)',  # pedra/pietra/piedra/pierre/piatră
 'camin': r'^(camin|chemin)',       # camino/caminho/cammino/chemin (ro drum=no)
 'com':   r'^(com|manĝ|manc|mangi|mang)',     # comer; COMEDERE vs MANDUCARE: doble herencia
 'manduc':r'^(manduc|mangi|manger|mânca)',
 'bib':   r'^(beb|bib|boiv|bea|boi)',         # beber/bere/bebér, boire, bea
 'cas':   r'^cas',                  # casa/casă (fr maison=no)
 'port':  r'^por',                  # puerta/porta/port/porte (ro ușă=no)
 'fenestr':r'^(fenestr|finestr|fereastr)',    # ventana=janela(GENUA)=no; fenêtre/fr fereastră sí
 'reg':   r'^(rey|rei|roi|re$|reg)',          # rey/rege/re
 'regin': r'^(rein|regin|rainh)',             # reina/regina/reine/rainha/regină
 'guerr': r'^(guerr|ger)',          # guerra/guerre (ro război=no)
 'pac':   r'^(paz|pace|paix)',      # paz/pace/paix
 'amor':  r'^(amor|amour)',         # amor/amore/amour
 'odi':   r'^odi',                  # odio/ódio (fr haine, ro ură = NO)
 'liber': r'^(liber|libertat|libertad|liberdade|libertate)', # libertad/liberté/libertà/liberdade/libertate
 'ver':   r'^(verdad|verit|verité|verità|adevăr)',           # verdad/vérité/verità/verdade; ro adevăr < AD+VERUM sí
 'just':  r'^(just|giust|justice|justiție)',                 # justicia/giustizia/justice/justiça/justiție
 'cit':   r'^(ciudad|citad|citt|cité|cidade|civiliza)',      # ciudad/città/cité/cidade (ro oraș=no)
 'hist':  r'^(hist|stor)',          # historia/storia/histoire/istorie
 'music': r'^(mus|muz)',            # música/musica/musique/muzică
 'schol': r'^(escuel|scuol|escol|eco|école|școal|skol)',     # escuela/scuola/escola/école/școală
 'cart':  r'^cart',                 # carta/carte/carta (todas menos... todas SI: es/it/pt IL identical)
}
ROOTMAP = {  # concepto -> raiz proto esperada
 'luz':'luc','noche':'noct','agua':'aqu','fuego':'foc','tierra':'terr','mar':'mar','sol':'sol',
 'luna':'lun','piedra':'petr','camino':'camin','comer':'com','beber':'bib','casa':'cas','puerta':'port',
 'ventana':'fenestr','rey':'reg','reina':'regin','guerra':'guerr','paz':'pac','amor':'amor','odio':'odi',
 'libertad':'liber','verdad':'ver','justicia':'just','ciudad':'cit','historia':'hist','música':'music',
 'escuela':'schol','carta':'cart'}

conn=sqlite3.connect(DB); cur=conn.cursor()
rows=cur.execute("SELECT id,concepto_espanol,es,fr,it,pt,ro FROM imports").fetchall()

for rid,concepto,es,fr,it,pt,ro in rows:
    root=ROOTMAP.get(concepto)
    forms={'es':es,'fr':fr,'it':it,'pt':pt,'ro':ro}
    keep={}
    if root and root in ALOFONOS:
        rx=re.compile(ALOFONOS[root])
        for lang,f in forms.items():
            if rx.match(norm(f)): keep[lang]=f
    n=len(keep)
    if n>=4: tipo='cognado_universal'
    elif n==3: tipo='consenso_romance'
    else: tipo='pendiente_manual'
    sugerida=None
    if tipo!='pendiente_manual' and keep:
        # regla longitud: la mas corta ENTRE LAS QUE CONSERVAN LA RAIZ
        lang=min(keep,key=lambda k:(len(norm(keep[k])),k))
        sugerida=forms[lang]
    pct=round(100.0*n/5,1)
    nota_extra='' if tipo!='pendiente_manual' else '; sin cognado claro, elegir manual'
    cur.execute("""UPDATE imports SET tipo_sugerencia=?, n_universal=?, consenso_pct=?,
                   palabra_sugerida=?, nota_ranking=COALESCE(nota_ranking,'')||? WHERE id=?""",
                (tipo,n,pct,sugerida,nota_extra,rid))
conn.commit()

print("--- Distribucion FINAL (umbral estricto) ---")
for r in cur.execute("SELECT tipo_sugerencia,COUNT(*) FROM imports GROUP BY 1 ORDER BY 2 DESC"): print(f"  {r[0]:20s} {r[1]}")
print("\n--- Cola completa ordenada por evidencia ---")
for r in cur.execute("""SELECT concepto_espanol,palabra_sugerida,tipo_sugerencia,n_universal,interlingua,esperanto
                        FROM imports_pendientes"""):
    sug=r[1] or '(manual)'
    print(f"  {r[0]:10s} -> {sug:10s} [{r[2]:18s} n={r[3]}/5] IL={r[4]:10s} EO={r[5]}")
print("\nChecks:",cur.execute("SELECT COUNT(*),SUM(palabra_sugerida IS NOT NULL) FROM imports").fetchone(),
      "integrity:",cur.execute("PRAGMA integrity_check").fetchone()[0])
conn.close()
