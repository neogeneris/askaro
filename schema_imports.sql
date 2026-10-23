-- ============================================================
-- TABLA imports: cola de nuevos sustantivos para Askaro,
-- alimentada desde Wiktionary (cognades neolatinos) y comparada
-- con Interlingua (IED) y Esperanto (RADE).
-- Reglas codificadas (del usuario):
--   1. palabra_sugerida = cognado universal verdadero (>=4/5 lenguas
--      romance coinciden); si no, consenso = termino mas comun romance.
--   2. Longitud: si existe alternativa mas corta Y universal, se prefiere.
--   3. interlingua y esperanto como columnas de eleccion manual.
-- ============================================================
CREATE TABLE IF NOT EXISTS imports (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    concepto_espanol TEXT NOT NULL UNIQUE,        -- glosa de control
    es  TEXT NOT NULL,                            -- espanol
    fr  TEXT,                                     -- frances
    it  TEXT,                                     -- italiano
    pt  TEXT,                                     -- portugues
    ro  TEXT,                                     -- rumano
    interlingua TEXT,                             -- vocabulario oficial IED
    esperanto   TEXT,                             -- RADE/Fundamento
    etimologia   TEXT NOT NULL,                   -- protoforma latina/griga + trayectoria
    palabra_sugerida TEXT,                        -- regla 1+2; NULL = pendiente_manual
    tipo_sugerencia  TEXT CHECK(tipo_sugerencia IN
       ('cognado_universal','consenso_romance','pendiente_manual')),
    n_universal    INTEGER,                       -- cuantas lenguas comparten la forma dominante
    consenso_pct   REAL,                          -- n_universal/5*100
    variantes      TEXT,                           -- las 5 formas, para ver alternativas cortas
    nota_ranking   TEXT,                           -- justificacion de la eleccion (regla longitud)
    estado         TEXT DEFAULT 'propuesta' CHECK(estado IN
       ('propuesta','aprobada','rechazada','integrada')),
    askaro_termino TEXT,                           -- resultado final de seleccion manual
    fecha_revision TEXT DEFAULT (date('now'))
);
CREATE INDEX IF NOT EXISTS idx_imports_estado ON imports(estado);
CREATE INDEX IF NOT EXISTS idx_imports_tipo ON imports(tipo_sugerencia);

-- Vista de trabajo para la seleccion manual: orden por calidad de evidencia
CREATE VIEW IF NOT EXISTS imports_pendientes AS
SELECT id, concepto_espanol, palabra_sugerida, tipo_sugerencia,
       n_universal, consenso_pct, interlingua, esperanto, variantes, etimologia, nota_ranking
FROM imports
WHERE estado='propuesta'
ORDER BY CASE tipo_sugerencia
           WHEN 'cognado_universal' THEN 1
           WHEN 'consenso_romance'  THEN 2
           ELSE 3 END,
         consenso_pct DESC, LENGTH(COALESCE(palabra_sugerida,'zzzzzz'));
