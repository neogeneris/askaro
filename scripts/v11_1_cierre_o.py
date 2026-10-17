#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V11.1 — Regla de cierre nominal: los sustantivos no pueden terminar en -e.

Estrategia por tipo de étimo:
  a) Sustantivos consonánticos latinos (sol, sal, pan, leche, sangre...):
     se restaura la vocal temática latina y se cierra en -o/-a según sexo léxico
     documentado en el propio diccionario (patrón lúna/stélla/pétra = tema -a).
  b) Temas ya vocálicos (-ine, -ite, -ure): simple cambio e->o.
  c) Compuestos/derivados: -e -> -o directo.

También aplica los casos explícitos del usuario:
  ave -> avéso ; avestruz -> avéstruso ; abuelo -> ávo ; abuela -> áva
y poda palabras compuestas con espacios (regla de composición V11 §4 / lexigo).
"""
import sqlite3, re, unicodedata

DB = '/workspace/askaro_lexico.db'
con = sqlite3.connect(DB)
cur = con.cursor()

CAUSA_E = 'Regla V11.1: prohibido sustantivo en -e; cierre neutro -o'

# Ajustes finales sobre el lote ya migrado (formas raras -> formas correctas)
ADJUST = {
    # id : nueva forma
    'ASK-SUS-0033': 'sólo',      # sol: monosílaba + o; sin tilde permissa? mantener sóle->sólo ok
    'ASK-SUS-0043': 'sanguíno',  # sanguis: i larga -> sanguíno
    'ASK-SUS-0045': 'kárno',
    'ASK-SUS-0046': 'pélo',
    'ASK-SUS-0048': 'kápitо'.replace('о','o'),
    'ASK-SUS-0050': 'pédо'.replace('о','o'),
    'ASK-SUS-0060': 'páno',
    'ASK-SUS-0196': 'sálo',
    'ASK-SUS-0137': 'vállо'.replace('о','o'),   # valle -> vallo (no válogo)
}
for id_, form in ADJUST.items():
    cur.execute("UPDATE lexico SET termino_askaro=? WHERE id=?", (form, id_))

# --- Casos explícitos del usuario ---
def set_form(id_, nueva, causa, notas_extra=None):
    row = cur.execute("SELECT termino_askaro FROM lexico WHERE id=?", (id_,)).fetchone()
    if not row:
        print('NO EXISTE', id_); return
    old = row[0]
    cur.execute("""UPDATE lexico SET termino_askaro=?, forma_anterior=COALESCE(forma_anterior,?),
                   causa_correccion=? WHERE id=?""", (nueva, old, causa, id_))
    if notas_extra:
        cur.execute("UPDATE lexico SET notas=COALESCE(notas,'')||' | '||? WHERE id=?", (notas_extra, id_))
    print(f'  {old} -> {nueva} ({id_})')

print('== CASOS EXPLICITOS USUARIO ==')
set_form('ASK-SUS-0128', 'avéso', 'Regla V11.1: ave no puede ser *avé (-e prohibido); forma avéso',
         'Ave < avis + sufijo -eso. Raíz: av-.')
set_form('ASK-SUS-1227', 'avéstruso', 'Regla V11.1: avestruz -> avéstruso (forma solicitada por el acuñador)',
         'Avestruz < avis+struthio. Prefijos heredan base: kwalavéstruso...')
set_form('ASK-SUS-0953', 'ávo', 'Regla V11.1: abuelo = ávo (< avus), forma pedida por el acuñador',
         'Ávo (abuelo) < avus. Homografía con ávo arcaico resuelta: esta es la única fila Canon.')
set_form('ASK-SUS-0954', 'áva', 'Regla V11.1: abuela = áva (< ava), capa biológica -a',
         'Áva (abuela) femenina biológica de ávo.')

# La fila Fusionada ASK-SUS-0510 también decía 'ávo'=ave; renombrar para evitar colisión real
r = cur.execute("SELECT termino_askaro, espanol FROM lexico WHERE id='ASK-SUS-0510'").fetchone()
if r and r[0] == 'ávo':
    cur.execute("UPDATE lexico SET termino_askaro='avéso', notas=COALESCE(notas,'')||' | Fusionada con avéso (V11.1)' WHERE id='ASK-SUS-0510'")
    print('  ASK-SUS-0510 (Fusionada) ávo -> avéso para liberar ávo=abuelo')

# --- Poda de compuestos con espacio (palabras compuestas -> eliminar) ---
print('== PODA COMPUESTOS CON ESPACIO ==')
comp = list(cur.execute("SELECT id, termino_askaro, espanol FROM lexico WHERE termino_askaro LIKE '% %' AND status!='Fusionada'"))
deleted = []
for id_, t, esp in comp:
    # conservar si existe lema atómico equivalente en español aproximado; si no, fusionar a primera palabra
    cur.execute("UPDATE lexico SET status='Fusionada', causa_correccion='Poda V11.1 §4: palabra compuesta eliminada del léxico atómico', notas=COALESCE(notas,'')||' | Compuesto eliminado: usar composición analítica " + t.replace("'"," ") + "' WHERE id=?", (id_,))
    deleted.append((t, esp))
for d in deleted: print('  fundida:', d)

# --- Verificación final: ningún sustantivo activo termina en -e ---
bad = list(cur.execute("SELECT id,termino_askaro FROM lexico WHERE termino_askaro LIKE '%e' AND clase_gramatical='Sustantivo' AND status!='Fusionada'"))
print('Sustantivos -e restantes:', bad)

con.commit()
print('OK commit')
