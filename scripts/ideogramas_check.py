#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditoria de colisiones de ideogramas (hanzi) para sustantivos Askaro.
Metodo: glosa espanola -> traduccion china (OpenCC s2t, tradicional) -> hanzi.
Una colision = dos terminos Askaro distintos que mapean al MISMO hanzi unico."""
import sqlite3, re, collections, opencc

s2t = opencc.OpenCC('s2t')  # simplificado -> tradicional
con = sqlite3.connect('/workspace/askaro_lexico.db')
rows = con.execute("""SELECT id, termino_askaro, espanol FROM lexico
                      WHERE clase_gramatical='Sustantivo' AND status IN ('Canon','Pendiente')""").fetchall()

hanzi_re = re.compile(r'[\u4e00-\u9fff]')
def clean_gloss(g):
    if not g: return ''
    g = g.split('/')[0].split('(')[0].strip().rstrip(',;.')
    return g

mapping = {}   # ask -> hanzi string
for aid, ask, esp in rows:
    g = clean_gloss(esp)
    if not g or len(g) > 25: continue
    zh = s2t.convert(g)
    hz = ''.join(hanzi_re.findall(zh))
    if hz:
        mapping[ask.strip()] = hz

single = {k:v for k,v in mapping.items() if len(v)==1}
multi  = {k:v for k,v in mapping.items() if len(v)>1}

# colisiones: mismo hanzi para terminos askaros distintos
inv = collections.defaultdict(list)
for k,v in single.items(): inv[v].append(k)
col = {h:sorted(ks) for h,ks in inv.items() if len(ks)>1}

print(f"Sustantivos activos: {len(rows)}")
print(f"Mapeados a >=1 hanzi: {len(mapping)}")
print(f"  - hanzi UNICO (candidatos a ideograma directo): {len(single)}")
print(f"  - compuesto/multi-hanzi: {len(multi)}")
print(f"Hanzi distintos usados en unicose: {len(set(single.values()))}")
print(f"\n=== COLISIONES (mismo hanzi, terminos distintos) ===")
for h, ks in sorted(col.items()):
    print(f"{h}: {', '.join(ks)}")
print(f"\nTotal pares colisionantes: {sum(len(c)*(len(c)-1)//2 for c in col.values())}")

import json
with open('/workspace/scripts/ideogramas_map.json','w') as f:
    json.dump({'unico':single,'multi':multi}, f, ensure_ascii=False, indent=0)
