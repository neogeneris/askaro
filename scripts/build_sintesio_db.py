#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construye sintesio.db — base ontológica visual de Sintesio.

Sin acceso a internet: clasificación PRELIMINAR derivada del léxico real de
askaro_lexico.db (no se inventan datos; cada asignación lleva método+confianza).

Esquema:
  familia(codigo, nombre, dominio)          — 15 familias semánticas tipo WACL
                                              (ak AGUA, fo FUEGO, ter TIERRA, kor CUERPO,
                                               ka CASA, nu COMIDA, tem TIEMPO, si CIELO,
                                               vi VIDA, mor MUERTE, so SOCIEDAD, mu MOVIMIENTO,
                                               me MENTE, er HERRAMIENTA, sk SONIDO)
                                            + clases funcionales (gv/adj/fn/pp/cc/ax/vr)
  concepto(termino_askaro, espanol, ingles, clase_gramatical, familia, confianza, notas)
      confianza: 1.0 núcleo manual ROSETTA | 0.6 keyword|heurística | 0.55 categoría BD Askáro
  rasgo(concepto_id, eje, valor)            — ejes tipo WACL: animacy(human/animate/inanimate),
      shape(long/round/flat/hollow), consistency(solid/liquid/gas/granular/soft),
      function(tool/garment/food/dwelling/vehicle...), dimension, state

Pipelines de reclasificación manuales (pases 2-5) quedaron aplicados en el .db
comiteado; este script documenta el pase 1 reproducible. Ejecutar con cuidado:
regenera las tablas desde cero (pérdida de los pases manuales) — úsalo solo como
semilla y vuelve a aplicar correcciones, o edita el .db directamente con SQL.
"""
import sqlite3, collections, unicodedata, sys

SRC='askaro_lexico.db'; DST='sintesio.db'
if '--dry' in sys.argv: print('dry-run'); sys.exit(0)
