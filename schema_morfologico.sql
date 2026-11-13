-- =====================================================
-- ASKÁRO-A - Sistema de Gestión Morfológica
-- Script para SQLiteStudio
-- =====================================================

-- Activar verificación de claves foráneas
PRAGMA foreign_keys = ON;

-- =====================================================
-- TABLA 1: RAICES
-- Almacena las raíces léxicas puras (sin vocal temática)
-- =====================================================
CREATE TABLE IF NOT EXISTS raices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raiz TEXT NOT NULL UNIQUE,
    categoria_base TEXT NOT NULL CHECK (categoria_base IN ('verbo', 'sustantivo', 'adjetivo', 'adverbio')),
    vocal_tematica TEXT CHECK (vocal_tematica IN ('â', 'ê', 'î', 'ô', 'û') OR vocal_tematica IS NULL),
    clase_verbal TEXT CHECK (clase_verbal IN ('-âr', '-êr', '-îr', '-ôr', '-ûr') OR clase_verbal IS NULL),
    significado TEXT NOT NULL,
    nota_etimologica TEXT,
    estado TEXT NOT NULL DEFAULT 'activa' CHECK (estado IN ('activa', 'archivada', 'propuesta')),
    fecha_creacion TEXT DEFAULT (datetime('now'))
);

-- =====================================================
-- TABLA 2: CADENAS
-- Motor de sufijos productivos (reglas de derivación)
-- =====================================================
CREATE TABLE IF NOT EXISTS cadenas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cadena TEXT NOT NULL UNIQUE,
    categoria_resultante TEXT NOT NULL CHECK (categoria_resultante IN ('sustantivo', 'adjetivo', 'verboide', 'adverbio')),
    funcion TEXT NOT NULL,
    requiere_vocal_tematica INTEGER NOT NULL DEFAULT 1 CHECK (requiere_vocal_tematica IN (0, 1)),
    aplica_asibilacion INTEGER NOT NULL DEFAULT 0 CHECK (aplica_asibilacion IN (0, 1)),
    tilde_fija TEXT CHECK (tilde_fija IN ('á', 'é', 'í', 'ó', 'ú', 'â', 'ê', 'î', 'ô', 'û') OR tilde_fija IS NULL),
    ejemplo_canonico TEXT,
    prioridad INTEGER NOT NULL DEFAULT 1,
    estado TEXT NOT NULL DEFAULT 'fijado' CHECK (estado IN ('fijado', 'propuesto', 'revisar', 'lexicalizado')),
    nota TEXT
);

-- =====================================================
-- TABLA 3: PALABRAS
-- Léxico generado (derivaciones automáticas + lexicalizaciones)
-- =====================================================
CREATE TABLE IF NOT EXISTS palabras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raiz_id INTEGER NOT NULL,
    cadena_id INTEGER,
    forma TEXT NOT NULL UNIQUE,
    categoria TEXT NOT NULL CHECK (categoria IN ('sustantivo', 'adjetivo', 'verbo', 'verboide', 'adverbio')),
    significado TEXT NOT NULL,
    es_lexicalizado INTEGER NOT NULL DEFAULT 0 CHECK (es_lexicalizado IN (0, 1)),
    es_regular INTEGER NOT NULL DEFAULT 1 CHECK (es_regular IN (0, 1)),
    frecuencia_uso INTEGER NOT NULL DEFAULT 0,
    fecha_creacion TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (raiz_id) REFERENCES raices(id) ON DELETE CASCADE,
    FOREIGN KEY (cadena_id) REFERENCES cadenas(id) ON DELETE SET NULL
);

-- =====================================================
-- TABLA 4: EXCEPCIONES
-- Formas lexicalizadas que no siguen las reglas generales
-- =====================================================
CREATE TABLE IF NOT EXISTS excepciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raiz_id INTEGER NOT NULL,
    forma_irregular TEXT NOT NULL UNIQUE,
    categoria TEXT NOT NULL CHECK (categoria IN ('sustantivo', 'adjetivo', 'verbo', 'verboide', 'adverbio')),
    significado TEXT NOT NULL,
    forma_regular_esperada TEXT,
    razon TEXT,
    FOREIGN KEY (raiz_id) REFERENCES raices(id) ON DELETE CASCADE
);

-- =====================================================
-- ÍNDICES para búsquedas rápidas
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_raices_raiz ON raices(raiz);
CREATE INDEX IF NOT EXISTS idx_raices_categoria ON raices(categoria_base);
CREATE INDEX IF NOT EXISTS idx_raices_vocal ON raices(vocal_tematica);

CREATE INDEX IF NOT EXISTS idx_cadenas_categoria ON cadenas(categoria_resultante);
CREATE INDEX IF NOT EXISTS idx_cadenas_funcion ON cadenas(funcion);

CREATE INDEX IF NOT EXISTS idx_palabras_forma ON palabras(forma);
CREATE INDEX IF NOT EXISTS idx_palabras_raiz ON palabras(raiz_id);
CREATE INDEX IF NOT EXISTS idx_palabras_categoria ON palabras(categoria);
CREATE INDEX IF NOT EXISTS idx_palabras_frecuencia ON palabras(frecuencia_uso DESC);

CREATE INDEX IF NOT EXISTS idx_excepciones_raiz ON excepciones(raiz_id);

-- =====================================================
-- VISTA ÚTIL: Palabras con desglose completo
-- =====================================================
CREATE VIEW IF NOT EXISTS vista_palabras_completas AS
SELECT 
    p.id,
    p.forma,
    p.categoria,
    p.significado,
    r.raiz,
    r.vocal_tematica,
    r.clase_verbal,
    c.cadena,
    c.funcion,
    p.es_lexicalizado,
    p.frecuencia_uso
FROM palabras p
JOIN raices r ON p.raiz_id = r.id
LEFT JOIN cadenas c ON p.cadena_id = c.id;

-- =====================================================
-- DATOS DE EJEMPLO: RAÍCES VALIDADAS
-- =====================================================
INSERT INTO raices (raiz, categoria_base, vocal_tematica, clase_verbal, significado, nota_etimologica) VALUES
-- Verbos de la familia -duk- (tema en -t-)
('eduk', 'verbo', 'â', '-âr', 'educar', 'Latín educare'),
('produk', 'verbo', 'â', '-âr', 'producir', 'Latín producere'),
('konduk', 'verbo', 'â', '-âr', 'conducir', 'Latín conducere'),
('traduk', 'verbo', 'î', '-îr', 'traducir', 'Latín traducere'),
('deduk', 'verbo', 'î', '-îr', 'deducir', 'Latín deducere'),

-- Verbos fundamentales
('es', 'verbo', 'ê', '-êr', 'ser (esencia)', 'Latín esse'),
('st', 'verbo', 'â', '-âr', 'estar (estado)', 'Latín stare'),
('ten', 'verbo', 'ê', '-êr', 'tener', 'Latín tenēre'),
('vid', 'verbo', 'ê', '-êr', 'ver', 'Latín vidēre'),
('ven', 'verbo', 'î', '-îr', 'venir', 'Latín venīre'),
('vad', 'verbo', 'â', '-âr', 'ir / descender', 'Latín vadere'),

-- Verbos de movimiento 3D (vectoriales)
('vir', 'verbo', 'î', '-îr', 'ascender / subir', 'Eje V + dirección i (arriba)'),
('frent', 'verbo', 'ê', '-êr', 'avanzar', 'Eje F + dirección e (frente)'),
('post', 'verbo', 'ô', '-ôr', 'retroceder', 'Eje P + dirección o (posterior)'),
('dult', 'verbo', 'û', '-ûr', 'lateralizar derecha', 'Eje D + dirección u (derecha)'),
('dilt', 'verbo', 'î', '-îr', 'lateralizar izquierda', 'Eje D + dirección i (izquierda)'),

-- Verbos irregulares romance
('fak', 'verbo', 'â', '-âr', 'hacer / fabricar', 'Latín facere'),
('dik', 'verbo', 'â', '-âr', 'decir', 'Latín dicere'),
('aud', 'verbo', 'î', '-îr', 'oír', 'Latín audīre'),

-- Límites y bordes
('intr', 'verbo', 'â', '-âr', 'entrar', 'Latín intrare'),
('extr', 'verbo', 'â', '-âr', 'salir', 'Latín extrahere'),

-- Sustantivos base
('kasa', 'sustantivo', NULL, NULL, 'casa', 'Latín casa'),
('mano', 'sustantivo', NULL, NULL, 'mano', 'Latín manus'),
('lupo', 'sustantivo', NULL, NULL, 'lobo', 'Latín lupus'),
('persóno', 'sustantivo', NULL, NULL, 'persona', 'Latín persona'),

-- Adjetivos base
('bon', 'adjetivo', NULL, NULL, 'bueno', 'Latín bonus'),
('grand', 'adjetivo', NULL, NULL, 'grande', 'Latín grandis');

-- =====================================================
-- DATOS DE EJEMPLO: CADENAS (Sufijos Productivos)
-- =====================================================
INSERT INTO cadenas (cadena, categoria_resultante, funcion, requiere_vocal_tematica, aplica_asibilacion, tilde_fija, ejemplo_canonico, prioridad, nota) VALUES
-- Derivación verbal (Primera Capa)
('nd', 'verboide', 'gerundio', 1, 0, NULL, 'edukând', 1, 'Gerundio progresivo'),
('t', 'verboide', 'participio_resultado', 1, 0, NULL, 'edukât', 2, 'Participio pasivo / resultado'),
('nte', 'adjetivo', 'participio_activo', 1, 0, 'ê', 'edukânte', 3, 'Adjetivo deverbal activo'),
('blu', 'adjetivo', 'posibilidad', 1, 0, 'á', 'edukâblu', 4, 'Adaptado de -ble romance'),
('dóro', 'sustantivo', 'agente_general', 1, 0, 'ó', 'edukâdóro', 5, 'El que hace la acción (genérico)'),
('tóro', 'sustantivo', 'agente_de_rol', 1, 0, 'ó', 'eduktóro', 6, 'Oficio/rol lexicalizado'),
('sióno', 'sustantivo', 'accion_abstracta', 1, 1, 'ó', 'faksióno', 7, 'Acción abstracta (asibilación t→s)'),
('ménto', 'sustantivo', 'proceso', 1, 0, 'é', 'edukménto', 8, 'Proceso o resultado'),
('dório', 'sustantivo', 'lugar', 1, 0, 'í', 'edukdório', 9, 'Lugar donde se realiza la acción'),
('túro', 'sustantivo', 'cualidad_abstracta', 1, 0, 'ú', 'eduktúro', 10, 'Cualidad abstracta'),
('tívu', 'adjetivo', 'adjetivo_relacional', 1, 0, 'í', 'eduktívu', 11, 'Adjetivo derivado relacional'),
('ál', 'adjetivo', 'relacional_simple', 1, 0, 'á', 'eduktál', 12, 'Relativo a'),
('áda', 'sustantivo', 'singularativo', 1, 0, 'á', 'eduktáda', 13, 'Un acto puntual'),

-- Sufijos Evaluativos
('íto', 'sustantivo', 'diminutivo', 1, 0, 'í', 'aktíto', 20, 'Diminutivo afectivo'),
('íta', 'sustantivo', 'diminutivo_fem', 1, 0, 'í', 'aktíta', 21, 'Diminutivo afectivo femenino'),
('étto', 'sustantivo', 'despectivo', 1, 0, 'é', 'aktétto', 22, 'Despectivo / insignificante'),
('étta', 'sustantivo', 'despectivo_fem', 1, 0, 'é', 'aktétta', 23, 'Despectivo femenino'),
('átsu', 'sustantivo', 'aumentativo', 1, 0, 'á', 'aktátsu', 24, 'Aumentativo intenso'),

-- Derivación de Segunda Capa
('s', 'sustantivo', 'plural', 0, 0, NULL, 'edukdóros', 30, 'Plural regular'),
('itádo', 'sustantivo', 'cualidad_nominal', 0, 0, 'á', 'bonitádo', 31, 'Cualidad abstracta desde adjetivo'),
('óre', 'adjetivo', 'denominal', 0, 0, 'ó', 'bonitóre', 32, 'Lleno de / relativo a'),
('isâr', 'verboide', 'denominativo', 0, 0, 'í', 'bonisâr', 33, 'Hacer/volverse X (infinitivo denominativo; la categoría resultante admitida por el CHECK de cadenas es verboide)'),

-- Adverbios
('umen', 'adverbio', 'manera', 0, 0, NULL, 'eduktívumen', 40, 'Adverbio de manera');

-- =====================================================
-- DATOS DE EJEMPLO: PALABRAS GENERADAS (de eduk-)
-- =====================================================
INSERT INTO palabras (raiz_id, cadena_id, forma, categoria, significado, es_lexicalizado, es_regular, frecuencia_uso) VALUES
-- Raíz 1 = eduk
(1, NULL, 'edukâr', 'verbo', 'educar', 0, 1, 100),
(1, 1, 'edukând', 'verboide', 'educando', 0, 1, 90),
(1, 2, 'edukât', 'verboide', 'educado (hecho)', 0, 1, 85),
(1, 3, 'edukânte', 'adjetivo', 'educante / el que educa', 0, 1, 80),
(1, 4, 'edukâblu', 'adjetivo', 'educable', 0, 1, 70),
(1, 5, 'edukâdóro', 'sustantivo', 'el que educa (genérico)', 0, 1, 75),
(1, 6, 'eduktóro', 'sustantivo', 'educador (de oficio)', 1, 0, 95),
(1, 7, 'edukâsióno', 'sustantivo', 'educación', 0, 1, 100),
(1, 8, 'edukménto', 'sustantivo', 'proceso de educación', 0, 1, 50),
(1, 9, 'edukdório', 'sustantivo', 'escuela / lugar de educación', 0, 1, 60),
(1, 10, 'eduktúro', 'sustantivo', 'educatividad', 0, 1, 30),
(1, 11, 'eduktívu', 'adjetivo', 'educativo', 0, 1, 85),
(1, 12, 'eduktál', 'adjetivo', 'relativo a la educación', 0, 1, 40),
(1, 13, 'eduktáda', 'sustantivo', 'acto educativo puntual', 0, 1, 25),
(1, 14, 'eduktíto', 'sustantivo', 'actito educativo', 0, 1, 15),
(1, 15, 'eduktétto', 'sustantivo', 'educachucho / mala educación', 0, 1, 10),
(1, 16, 'eduktátsu', 'sustantivo', 'educadazo / gran educación', 0, 1, 15),
(1, 17, 'eduktívumen', 'adverbio', 'educativamente', 0, 1, 30);

-- =====================================================
-- DATOS DE EJEMPLO: PALABRAS DE frent- (verbo vectorial)
-- =====================================================
INSERT INTO palabras (raiz_id, cadena_id, forma, categoria, significado, es_lexicalizado, es_regular, frecuencia_uso) VALUES
-- Raíz 13 = frent
(13, NULL, 'frentêr', 'verbo', 'avanzar / ir al frente', 0, 1, 90),
(13, 1, 'frentênd', 'verboide', 'avanzando', 0, 1, 80),
(13, 2, 'frentêt', 'verboide', 'avanzado', 0, 1, 75),
(13, 7, 'frentêsióno', 'sustantivo', 'avance', 0, 1, 70),
(13, 5, 'frentêdóro', 'sustantivo', 'el que avanza', 0, 1, 50);

-- =====================================================
-- DATOS DE EJEMPLO: PALABRAS DE post- (verbo vectorial)
-- =====================================================
INSERT INTO palabras (raiz_id, cadena_id, forma, categoria, significado, es_lexicalizado, es_regular, frecuencia_uso) VALUES
-- Raíz 14 = post
(14, NULL, 'postôr', 'verbo', 'retroceder / ir al posterior', 0, 1, 85),
(14, 1, 'postônd', 'verboide', 'retrocediendo', 0, 1, 75),
(14, 2, 'postôt', 'verboide', 'retrocedido', 0, 1, 70),
(14, 7, 'postôsióno', 'sustantivo', 'retroceso', 0, 1, 65);

-- =====================================================
-- DATOS DE EJEMPLO: PALABRAS DE dult- (verbo vectorial)
-- =====================================================
INSERT INTO palabras (raiz_id, cadena_id, forma, categoria, significado, es_lexicalizado, es_regular, frecuencia_uso) VALUES
-- Raíz 15 = dult
(15, NULL, 'dultûr', 'verbo', 'lateralizar a la derecha', 0, 1, 70),
(15, 1, 'dultûnd', 'verboide', 'lateralizando a la derecha', 0, 1, 60),
(15, 2, 'dultût', 'verboide', 'desplazado a la derecha', 0, 1, 55),
(15, 7, 'dultûsióno', 'sustantivo', 'desplazamiento lateral derecho', 0, 1, 50);

-- =====================================================
-- DATOS DE EJEMPLO: PALABRAS DE ten- (verbo irregular romance)
-- =====================================================
INSERT INTO palabras (raiz_id, cadena_id, forma, categoria, significado, es_lexicalizado, es_regular, frecuencia_uso) VALUES
-- Raíz 8 = ten
(8, NULL, 'tenêr', 'verbo', 'tener', 0, 1, 100),
(8, 1, 'tenênd', 'verboide', 'teniendo', 0, 1, 90),
(8, 2, 'tenêt', 'verboide', 'tenido', 0, 1, 85),
(8, 7, 'tensióno', 'sustantivo', 'tenencia', 0, 1, 75),
(8, 6, 'tentóro', 'sustantivo', 'tenedor / poseedor', 1, 0, 70);

-- =====================================================
-- DATOS DE EJEMPLO: EXCEPCIONES (lexicalizaciones)
-- =====================================================
INSERT INTO excepciones (raiz_id, forma_irregular, categoria, significado, forma_regular_esperada, razon) VALUES
(6, 'esénto', 'sustantivo', 'ente / ser', 'esêtóro', 'lexicalización histórica del participio de esêr'),
(21, 'bonitádo', 'sustantivo', 'bondad', NULL, 'derivación de segunda capa desde adjetivo base');

-- =====================================================
-- VERIFICACIÓN: Consultas útiles
-- =====================================================

-- Ver todas las raíces con su clase verbal
-- SELECT raiz, clase_verbal, significado FROM raices WHERE categoria_base = 'verbo' ORDER BY clase_verbal;

-- Ver todas las palabras generadas de una raíz específica
-- SELECT * FROM vista_palabras_completas WHERE raiz = 'eduk' ORDER BY frecuencia_uso DESC;

-- Ver todas las cadenas (sufijos) disponibles
-- SELECT cadena, funcion, categoria_resultante FROM cadenas ORDER BY prioridad;

-- Contar palabras por categoría
-- SELECT categoria, COUNT(*) as total FROM palabras GROUP BY categoria ORDER BY total DESC;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
