#!/usr/bin/env python3
"""Enriquece imports: clase_gramatical + puente Sintesio (familia/nucleo/sintesis) para las 29 filas seed."""
import sqlite3, unicodedata

def norm(s):
    if not s: return ''
    d = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','â':'a','ê':'e','î':'i','ñ':'n','ü':'u'}
    return ''.join(d.get(c.lower(), c) for c in s).lower()

s1 = sqlite3.connect('sintesio.db')

# 1. clase gramatical por lookup a concepto.clase_gramatical (normalizado)
cg_map = {}
for e, cg in s1.execute("SELECT espanol, clase_gramatical FROM concepto WHERE clase_gramatical IS NOT NULL"):
    cg_map.setdefault(norm(e), cg)
updated_cg = 0
for cid, conc in s1.execute("SELECT id, concepto_espanol FROM imports"):
    cg = cg_map.get(norm(conc))
    if cg:
        s1.execute("UPDATE imports SET clase_gramatical=? WHERE id=?", (cg.lower(), cid))
        updated_cg += 1

# 2. puente Sintesio desde sustantivo+matriz+nucleo (solo sustantivos ya clasificados)
puente = {}
for sn_id, esp, fam, nuc, syn, conf in s1.execute("""
    SELECT s.id, s.espanol, c.familia, n.simbolo, m.sintesis, m.confianza
    FROM sustantivo s
    JOIN matriz_rasgo m ON m.sustantivo_id = s.id
    LEFT JOIN nucleo n ON n.id = s.nucleo_id
    LEFT JOIN concepto c ON c.termino_askaro = s.termino
"""):
    puente.setdefault(norm(esp), (fam, nuc, syn, conf))

linked = 0
for cid, conc in s1.execute("SELECT id, concepto_espanol FROM imports WHERE clase_gramatical='sustantivo'"):
    p = puente.get(norm(conc))
    if p:
        fam, nuc, syn, conf = p
        s1.execute("UPDATE imports SET familia_sintesio=?, nucleo_sugerido=?, sintesis_sugerida=?, confianza_sintesio=? WHERE id=?",
                   (fam, nuc, syn, conf, cid))
        linked += 1

s1.commit()
print(f"clase_gramatical asignada desde concepto: {updated_cg}/29")
print(f"puente Sintesio enlazado (sustantivos): {linked}")
print("\n--- muestra ---")
for r in s1.execute("""SELECT concepto_espanol, palabra_sugerida, clase_gramatical, familia_sintesio,
                              nucleo_sugerido, substr(coalesce(sintesis_sugerida,''),1,28), confianza_sintesio FROM imports LIMIT 12"""):
    print(r)
