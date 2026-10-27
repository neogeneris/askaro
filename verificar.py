#!/usr/bin/env python3
"""Verificación de fase 1: ejecuta las 8 consultas de verificacion.sql.

Se ejecuta con pysqlite3 (SQLite 3.51.1) porque la biblioteca del sistema
(3.40.1) no puede ABRIR una BD cuyo esquema contiene triggers con RAISE
que usa concatenación || (error 'malformed database schema'). La CLI se
reserva solo para comprobaciones que no tocan el esquema de los triggers.
"""
import sys
try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3

R = sqlite3.connect("lexico.db")
cur = R.cursor()

def show(title, sql):
    print(f"\n--- {title} ---")
    for row in cur.execute(sql):
        print(row[0] if len(row) == 1 else row)

show("1. Tablas creadas", "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
show("2. Índices idx_* (esperado 9)", "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'")
show("3. Triggers creados", "SELECT name FROM sqlite_master WHERE type='trigger' ORDER BY name")
show("4. Vistas creadas", "SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")
show("5. Semilla emoji_colisiones (esperado 6)", "SELECT COUNT(*) FROM emoji_colisiones")
show("6. lexico vacía (esperado 0)", "SELECT COUNT(*) FROM lexico")
show("7. integrity_check (esperado ok)", "PRAGMA integrity_check")

print("\n--- 8. Test emoji duplicado (esperado: fallo 'Emoji duplicado: 🪨') ---")
# Con lexico vacía el WHEN del trigger no dispara; se precarga y limpia
# una fila de prueba para ejercitarlo exactamente como pide el enunciado.
INS = """INSERT INTO lexico (emoji, concepto_es, es, en, fr, it, pt,
      ro, ia, eo, categoria, cognado, forma_ganadora, fuente_ganadora)
      VALUES (?, ?, 'a','b','c','d','e','f','g','h',
              'sustantivo','universal','test','es')"""
try:
    cur.execute(INS, ("🪨", "piedra"))          # fila de apoyo (no deja rastro)
    cur.execute(INS, ("🪨", "otro-test"))       # esta DEBE fallar
    print("FALLO DEL TEST: la inserción prosperó (no se detectó el duplicado)")
    sys.exit(1)
except Exception as ex:
    print(f"Inserción rechazada correctamente -> {ex}")
finally:
    cur.execute("DELETE FROM lexico WHERE concepto_es IN ('piedra','otro-test')")
    R.commit()

show("6 (re-confirmación). lexico sigue vacía", "SELECT COUNT(*) FROM lexico")
show("7 (re-confirmación). integrity_check", "PRAGMA integrity_check")
R.close()
print("\nVERIFICACIÓN COMPLETA")
