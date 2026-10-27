-- =====================================================================
-- verificacion.sql — Fase 1: comprobaciones post-creación de lexico.db
-- Ejecución: sqlite3 lexico.db < verificacion.sql
-- Uso recomendado (modo consola legible):
--   sqlite3 -box lexico.db ".read verificacion.sql"
-- =====================================================================

SELECT '=== 1. Tablas creadas (esperado: emoji_candidatos, emoji_colisiones, lexico) ===' AS chequeo;
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;

SELECT '=== 2. Índices idx_* creados (esperado: 9) ===' AS chequeo;
SELECT COUNT(*) AS indices FROM sqlite_master
WHERE type='index' AND name LIKE 'idx_%';

SELECT '=== 3. Triggers creados (esperado: 4) ===' AS chequeo;
SELECT name FROM sqlite_master WHERE type='trigger' ORDER BY name;

SELECT '=== 4. Vistas creadas (esperado: 5) ===' AS chequeo;
SELECT name FROM sqlite_master WHERE type='view' ORDER BY name;

SELECT '=== 5. Semilla insertada en emoji_colisiones (esperado: 6) ===' AS chequeo;
SELECT COUNT(*) AS filas_colisiones FROM emoji_colisiones;

SELECT '=== 6. lexico vacía (esperado: 0) ===' AS chequeo;
SELECT COUNT(*) AS filas_lexico FROM lexico;

SELECT '=== 7. Integridad (esperado: ok) ===' AS chequeo;
PRAGMA integrity_check;

SELECT '=== 8. Test emoji duplicado (esperado: ABORT "Emoji duplicado: 🪨") ===' AS chequeo;
-- Esta inserción DEBE fallar; el resto del script ya se ejecutó arriba.
INSERT INTO lexico (emoji, concepto_es, es, en, fr, it, pt,
                    ro, ia, eo, categoria, cognado, forma_ganadora,
                    fuente_ganadora)
VALUES ('🪨','test','a','b','c','d','e','f','g','h',
        'sustantivo','universal','test','es');

-- Si por alguna razón la inserción hubiera prosperado, deshacer así:
-- DELETE FROM lexico WHERE concepto_es = 'test';

-- =====================================================================
-- NOTA (verificación ejecutada con pysqlite3 / SQLite 3.51.1):
--   La CLI del sistema es SQLite 3.40.1, que no puede ABRIR esta BD:
--   rechaza el esquema de los triggers con RAISE(ABORT, '...' || ...)
--   y devuelve "malformed database schema" (error 11). No es un bug de
--   executescript() sino del parser 3.40.1; la concatenación en RAISE es
--   válida desde hace años y funciona en 3.51.1.
--   Por eso la verificación se corre con:  python3 verificar.py
--   (mismas 8 consultas de este archivo). La CLI solo sirve para tablas
--   sin triggers, p.ej.: sqlite3 lexico.db "SELECT COUNT(*) FROM emoji_colisiones;"
--   también falla al abrir la BD completa.
-- =====================================================================
