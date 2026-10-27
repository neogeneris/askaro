-- =====================================================================
-- schema.sql — FASE 1: Léxico comparado (8 lenguas)
-- Motor: SQLite3 >= 3.37 (tablas STRICT)
-- Ejecución: sqlite3 lexico.db < schema.sql
-- Idempotente: incluye DROP ... IF EXISTS al inicio (orden inverso
-- de dependencias: candidatos -> colisiones -> lexico).
-- =====================================================================
-- ---------------------------------------------------------------------
-- Configuración inicial
-- ---------------------------------------------------------------------
PRAGMA foreign_keys = ON;      -- hace cumplir las FK en cada sentencia
PRAGMA journal_mode = WAL;     -- escritura concurrente sin bloquear lecturas
PRAGMA synchronous = NORMAL;   -- equilibrio seguridad/rendimiento con WAL
-- ---------------------------------------------------------------------
-- Eliminación idempotente (orden inverso a dependencias)
-- emoji_candidatos depende de lexico; emoji_colisiones es un log sin FK.
-- ---------------------------------------------------------------------
DROP VIEW    IF EXISTS v_sin_emoji_propio;
DROP VIEW    IF EXISTS v_consenso_bajo;
DROP VIEW    IF EXISTS v_colisiones_huerfanas;
DROP VIEW    IF EXISTS v_stats_categoria;
DROP VIEW    IF EXISTS v_ganadora_no_es;
DROP TRIGGER IF EXISTS trg_lexico_update;
DROP TRIGGER IF EXISTS trg_emoji_unique_insert;
DROP TRIGGER IF EXISTS trg_concepto_unique_insert;
DROP TRIGGER IF EXISTS trg_candidato_unico_elegido;
DROP TABLE   IF EXISTS emoji_candidatos;
DROP TABLE   IF EXISTS emoji_colisiones;
DROP TABLE   IF EXISTS lexico;
-- =====================================================================
-- TABLA 1: lexico
-- Propósito: una fila por concepto, con formas en 8 lenguas
-- (es, en, fr, it, pt, ro, ia, eo), etimología latina, cognación,
-- consenso entre lenguas y emoji único por concepto.
-- =====================================================================
CREATE TABLE lexico (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    emoji              TEXT    NOT NULL UNIQUE,           -- un emoji por concepto
    concepto_es        TEXT    NOT NULL UNIQUE,           -- clave natural del concepto
    es                 TEXT    NOT NULL,                  -- español
    en                 TEXT    NOT NULL,                  -- inglés
    fr                 TEXT    NOT NULL,                  -- francés
    it                 TEXT    NOT NULL,                  -- italiano
    pt                 TEXT    NOT NULL,                  -- portugués
    ro                 TEXT    NOT NULL,                  -- rumano
    ia                 TEXT    NOT NULL,                  -- interlingua
    eo                 TEXT    NOT NULL,                  -- esperanto
    latin              TEXT    NOT NULL DEFAULT '—',      -- etimología latina ('—' si no aplica)
    categoria          TEXT    NOT NULL
                               CHECK (categoria IN ('sustantivo',
                                                    'verbo',
                                                    'adjetivo',
                                                    'adverbio')),
    swadesh            INTEGER NOT NULL DEFAULT 0
                               CHECK (swadesh IN (0, 1)),  -- pertenece a lista Swadesh
    basic_level        INTEGER NOT NULL DEFAULT 0
                               CHECK (basic_level IN (0, 1)), -- vocabulario básico
    cognado            TEXT    NOT NULL
                               CHECK (cognado IN ('universal',
                                                  'romance',
                                                  'parcial',
                                                  'ninguno')),
    lenguas_consenso   INTEGER NOT NULL DEFAULT 0
                               CHECK (lenguas_consenso BETWEEN 0 AND 8),
    forma_ganadora     TEXT    NOT NULL,                  -- forma seleccionada como estándar
    fuente_ganadora    TEXT    NOT NULL
                               CHECK (fuente_ganadora IN ('es','en','fr',
                                                          'it','pt','ro',
                                                          'ia','eo')),
    nota               TEXT,                              -- observaciones libres
    fecha_creacion     TEXT    NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT    NOT NULL DEFAULT (datetime('now')),
    CONSTRAINT emoji_no_vacio      CHECK (length(emoji) > 0),
    CONSTRAINT concepto_no_vacio   CHECK (length(concepto_es) > 0),
    CONSTRAINT ganadora_no_vacia   CHECK (length(forma_ganadora) > 0)
) STRICT;
-- =====================================================================
-- TABLA 2: emoji_colisiones
-- Propósito: log de auditoría de colisiones de emoji resueltas
-- (dos conceptos que aspiraban al mismo emoji).
-- DISEÑO: SIN foreign keys — es un log histórico, no una entidad
-- dependiente. Permite insertar la semilla ANTES de poblar `lexico`.
-- =====================================================================
CREATE TABLE emoji_colisiones (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    emoji             TEXT    NOT NULL,                   -- emoji en disputa
    concepto_ganador  TEXT    NOT NULL,                   -- concepto que se quedó el emoji
    concepto_perdedor TEXT    NOT NULL,                   -- concepto reasignado
    resolucion        TEXT    NOT NULL
                              CHECK (resolucion IN ('especifico_gana',
                                                    'mayor_puntuacion',
                                                    'segundo_candidato',
                                                    'sin_alternativa')),
    nota              TEXT,                               -- justificación de la resolución
    fecha             TEXT    NOT NULL DEFAULT (datetime('now')),
    CONSTRAINT emoji_no_vacio      CHECK (length(emoji) > 0),
    CONSTRAINT ganador_no_vacio    CHECK (length(concepto_ganador) > 0),
    CONSTRAINT perdedor_no_vacio   CHECK (length(concepto_perdedor) > 0),
    CONSTRAINT distintos           CHECK (concepto_ganador <> concepto_perdedor)
) STRICT;
-- =====================================================================
-- TABLA 3: emoji_candidatos
-- Propósito: candidatos alternativos de emoji por concepto, con
-- puntuación (0-100) y marca del elegido final.
-- DISEÑO: SÍ lleva foreign key hacia lexico(concepto_es) — el
-- candidato depende del concepto; se borra en cascada con él.
-- =====================================================================
CREATE TABLE emoji_candidatos (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    concepto_es       TEXT    NOT NULL,                   -- FK lógica al concepto
    emoji             TEXT    NOT NULL,                   -- emoji candidato
    nombre_oficial    TEXT    NOT NULL,                   -- nombre oficial Unicode
    codepoint         TEXT    NOT NULL,                   -- p.ej. U+1FAA8
    puntuacion        INTEGER NOT NULL
                              CHECK (puntuacion BETWEEN 0 AND 100),
    elegido           INTEGER NOT NULL DEFAULT 0
                              CHECK (elegido IN (0, 1)),
    nota              TEXT,
    FOREIGN KEY (concepto_es) REFERENCES lexico(concepto_es)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT codepoint_formato CHECK (codepoint GLOB 'U+[0-9A-F]*')
) STRICT;
-- =====================================================================
-- ÍNDICES
-- =====================================================================
-- Búsquedas/agregaciones frecuentes por categoría gramatical.
CREATE INDEX idx_lexico_categoria    ON lexico(categoria);
-- Filtrado por tipo de cognación.
CREATE INDEX idx_lexico_cognado      ON lexico(cognado);
-- Auditoría de conceptos con consenso alto/bajo.
CREATE INDEX idx_lexico_consenso     ON lexico(lenguas_consenso);
-- Índice parcial: solo los conceptos Swadesh (lista corta).
CREATE INDEX idx_lexico_swadesh      ON lexico(swadesh) WHERE swadesh = 1;
-- Índice parcial: solo los conceptos de nivel básico.
CREATE INDEX idx_lexico_basic        ON lexico(basic_level) WHERE basic_level = 1;
-- Análisis de qué fuente gana por concepto.
CREATE INDEX idx_lexico_fuente       ON lexico(fuente_ganadora);
-- Acceso a los candidatos de un concepto.
CREATE INDEX idx_candidatos_concepto ON emoji_candidatos(concepto_es);
-- Búsqueda rápida del candidato elegido por concepto.
CREATE INDEX idx_candidatos_elegido  ON emoji_candidatos(concepto_es, elegido);
-- Auditoría de colisiones por emoji.
CREATE INDEX idx_colisiones_emoji    ON emoji_colisiones(emoji);
-- =====================================================================
-- TRIGGERS
-- =====================================================================
-- Trg 1: mantener fecha_modificacion al día en cualquier UPDATE.
-- (NO recursivo: la condición OLD.fecha_modificacion <> NEW... evita
-- reentrarse cuando el propio trigger actualiza la columna.)
CREATE TRIGGER trg_lexico_update
AFTER UPDATE ON lexico
FOR EACH ROW
WHEN OLD.fecha_modificacion IS NOT NEW.fecha_modificacion
BEGIN
    UPDATE lexico
    SET fecha_modificacion = datetime('now')
    WHERE id = OLD.id;
END;
-- Trg 2: impedir emoji duplicado con mensaje útil (más claro que el
-- error genérico de la restricción UNIQUE).
CREATE TRIGGER trg_emoji_unique_insert
BEFORE INSERT ON lexico
FOR EACH ROW
WHEN EXISTS (SELECT 1 FROM lexico WHERE emoji = NEW.emoji)
BEGIN
    SELECT RAISE(ABORT, 'Emoji duplicado: ' || NEW.emoji);
END;
-- Trg 3: impedir concepto duplicado con mensaje útil.
CREATE TRIGGER trg_concepto_unique_insert
BEFORE INSERT ON lexico
FOR EACH ROW
WHEN EXISTS (SELECT 1 FROM lexico WHERE concepto_es = NEW.concepto_es)
BEGIN
    SELECT RAISE(ABORT, 'Concepto duplicado: ' || NEW.concepto_es);
END;
-- Trg 4: garantizar un solo candidato elegido por concepto.
CREATE TRIGGER trg_candidato_unico_elegido
BEFORE UPDATE OF elegido ON emoji_candidatos
FOR EACH ROW
WHEN NEW.elegido = 1
 AND EXISTS (SELECT 1 FROM emoji_candidatos
             WHERE concepto_es = NEW.concepto_es
               AND elegido = 1
               AND id <> NEW.id)
BEGIN
    SELECT RAISE(ABORT, 'Ya hay un candidato elegido para: ' || NEW.concepto_es);
END;
-- =====================================================================
-- VISTAS
-- =====================================================================
-- Vista 1: conceptos representados con emoji aproximado (sin emoji
-- propio literal); sirve para revisión manual de calidad visual.
CREATE VIEW v_sin_emoji_propio AS
SELECT concepto_es, emoji, nota
FROM lexico
WHERE nota LIKE '%sin emoji%' OR nota LIKE '%aproximado%';
-- Vista 2: conceptos con consenso bajo (<3 lenguas) — candidatos a
-- revisión de la forma ganadora.
CREATE VIEW v_consenso_bajo AS
SELECT concepto_es, cognado, lenguas_consenso, forma_ganadora, nota
FROM lexico
WHERE lenguas_consenso < 3
ORDER BY lenguas_consenso ASC, concepto_es ASC;
-- Vista 3: colisiones cuyos conceptos aún no existen en lexico
-- (auditoría de coherencia log <-> tabla maestra).
CREATE VIEW v_colisiones_huerfanas AS
SELECT ec.*
FROM emoji_colisiones ec
LEFT JOIN lexico l1 ON ec.concepto_ganador  = l1.concepto_es
LEFT JOIN lexico l2 ON ec.concepto_perdedor = l2.concepto_es
WHERE l1.concepto_es IS NULL OR l2.concepto_es IS NULL;
-- Vista 4: estadísticas agregadas por categoría gramatical.
CREATE VIEW v_stats_categoria AS
SELECT categoria,
       COUNT(*)                 AS total,
       SUM(swadesh)             AS swadesh_count,
       SUM(basic_level)         AS basic_count,
       ROUND(AVG(lenguas_consenso), 2) AS consenso_promedio
FROM lexico
GROUP BY categoria;
-- Vista 5: conceptos cuya forma ganadora NO es española (el estándar
-- salió de otra lengua — caso interesante para el análisis comparado).
CREATE VIEW v_ganadora_no_es AS
SELECT concepto_es, forma_ganadora, fuente_ganadora, lenguas_consenso
FROM lexico
WHERE fuente_ganadora <> 'es'
ORDER BY lenguas_consenso DESC;
-- =====================================================================
-- SEMILLA DE COLISIONES (6 filas)
-- Se inserta en emoji_colisiones: al no tener FK, no requiere que
-- `lexico` esté poblado (corrección de diseño de la fase 1).
-- =====================================================================
INSERT INTO emoji_colisiones
    (emoji, concepto_ganador, concepto_perdedor, resolucion, nota)
VALUES
    ('🪨', 'piedra', 'tierra', 'especifico_gana',
     'piedra es el referente literal de 🪨; tierra usa 🌍'),
    ('🪰', 'mosca', 'libélula', 'especifico_gana',
     'mosca es el referente literal de 🪰; libélula usa 🦋 con nota'),
    ('🏙️', 'ciudad', 'metrópolis', 'especifico_gana',
     'ciudad es el referente directo; metrópolis usa 🌆'),
    ('📜', 'pergamino', 'historia', 'especifico_gana',
     'pergamino es el referente literal; historia usa 📖'),
    ('🐁', 'topo', 'ratón', 'mayor_puntuacion',
     'topo usa 🐁 por falta de emoji propio; ratón usa 🐭'),
    ('🐿️', 'marmota', 'ardilla', 'mayor_puntuacion',
     'marmota usa 🐿️ por falta de emoji propio; ardilla usa 🐿️ con nota');
