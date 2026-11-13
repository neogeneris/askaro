-- =====================================================
-- ASKÁRO-A — PLANTILLA MAESTRA DE DERIVACIÓN (v3.0)
-- Raíz canónica: ak- (actuar) · 90 ítems en 9 bloques
-- Sintético → motor `cadenas` | Analítico → tablas nuevas
-- Re-ejecutable (CREATE IF NOT EXISTS + INSERT OR IGNORE)
-- Convenciones v3.0: áéíóú tónica explícita · âêîôû vocal
-- temática verbal · macrón āēīōū auxiliar preverbal
-- =====================================================
PRAGMA foreign_keys = ON;

-- TABLA 5: FAROS_ASPECTO (Bloque 2)
CREATE TABLE IF NOT EXISTS faros_aspecto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    funcion TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('sintetico','analitico')),
    formula TEXT NOT NULL,
    auxiliar TEXT,
    forma_dependiente TEXT,
    ejemplo_ak TEXT NOT NULL,
    glosa_es TEXT NOT NULL,
    nota TEXT,
    estado TEXT NOT NULL DEFAULT 'fijado' CHECK (estado IN ('fijado','propuesto','revisar'))
);

-- TABLA 6: PILA_MODALES (Bloque 3; extiende pila_preverbal capas 1-4)
CREATE TABLE IF NOT EXISTS pila_modales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    funcion TEXT NOT NULL,
    auxiliar TEXT NOT NULL,
    contraccion TEXT,
    seleccion TEXT NOT NULL DEFAULT 'âs + inf' CHECK (seleccion IN ('âs + inf','inf solo','âs + adj')),
    ejemplo_ak TEXT NOT NULL,
    glosa_es TEXT NOT NULL,
    nota TEXT,
    estado TEXT NOT NULL DEFAULT 'fijado'
);

-- TABLA 7: FOCOS_COGNITIVOS (Bloque 4; alineada con tabla roles)
CREATE TABLE IF NOT EXISTS focos_cognitivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    funcion TEXT NOT NULL,
    operador TEXT NOT NULL,
    rol_alineado TEXT,
    ejemplo_ak TEXT NOT NULL,
    glosa_es TEXT NOT NULL,
    nota TEXT,
    estado TEXT NOT NULL DEFAULT 'fijado'
);

-- TABLA 8: DETERMINANTES_COLECTIVOS (Bloque 6)
CREATE TABLE IF NOT EXISTS determinantes_colectivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    funcion TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('sintetico','analitico')),
    forma TEXT NOT NULL,
    ejemplo TEXT NOT NULL,
    glosa_es TEXT NOT NULL,
    nota TEXT,
    estado TEXT NOT NULL DEFAULT 'fijado'
);

-- TABLA 9: CONECTORES (Bloque 7)
CREATE TABLE IF NOT EXISTS conectores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    funcion TEXT NOT NULL,
    particula TEXT NOT NULL,
    ejemplo TEXT NOT NULL,
    glosa_es TEXT NOT NULL,
    nota TEXT,
    estado TEXT NOT NULL DEFAULT 'fijado'
);

-- TABLA 10: CUANTIFICADORES_LOGICOS (Bloque 8; coherente con doc. maestro §ómno/úno)
CREATE TABLE IF NOT EXISTS cuantificadores_logicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    funcion TEXT NOT NULL,
    formula TEXT NOT NULL,
    ejemplo_ak TEXT NOT NULL,
    glosa_es TEXT NOT NULL,
    nota TEXT,
    estado TEXT NOT NULL DEFAULT 'fijado'
);

-- TABLA 11: PREDICACION (Bloque 9 + registro de plantilla Bloque 5)
CREATE TABLE IF NOT EXISTS predicacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    funcion TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('sintetico','analitico','mixto')),
    formula TEXT NOT NULL,
    ejemplo_ak TEXT NOT NULL,
    glosa_es TEXT NOT NULL,
    nota TEXT,
    estado TEXT NOT NULL DEFAULT 'fijado'
);

CREATE INDEX IF NOT EXISTS idx_faros_funcion ON faros_aspecto(funcion);
CREATE INDEX IF NOT EXISTS idx_modales_aux ON pila_modales(auxiliar);
CREATE INDEX IF NOT EXISTS idx_focos_op ON focos_cognitivos(operador);
CREATE INDEX IF NOT EXISTS idx_conect_part ON conectores(particula);

-- =====================================================
-- BLOQUE 1 — Núcleo Derivacional → motor sintético `cadenas`
-- (IDs existentes verificados: 1 nd, 2 t, 3 nte, 4 blu, 5 dóro,
--  6 tóro, 7 sióno, 8 ménto, 9 dório, 10 túro, 11 tívu, 12 ál,
--  13 áda, 14 íto, 16 étto, 18 átsu, 23 umen)
-- Reordenación de prioridad para resolver la colisión D.11/E.01
-- =====================================================
UPDATE cadenas SET prioridad = 5 WHERE id = 2;   -- -t participio → D.04 ákto
UPDATE cadenas SET prioridad = 6 WHERE id = 4;   -- -blu          → D.13 aktáblu
UPDATE cadenas SET prioridad = 7 WHERE id = 14;  -- -íto dimin.   → E.01 aktíto
UPDATE cadenas SET prioridad = 8 WHERE id = 16;  -- -étto despect → E.02 aktétto
UPDATE cadenas SET prioridad = 9 WHERE id = 18;  -- -átsu aument. → E.03 aktátsu

INSERT OR IGNORE INTO cadenas (id,cadena,categoria_resultante,funcion,requiere_vocal_tematica,aplica_asibilacion,tilde_fija,ejemplo_canonico,prioridad,estado,nota) VALUES
 (24,'-âr','verboide','verbo_base',0,0,NULL,'aktâr',2,'fijado','D.01 infinitivo / tema verbal â'),
 (25,'-énte','adjetivo','participante_activo',1,0,'é','akénte',3,'fijado','D.02 variante acentuada plena de -nte (cad. 3), fijada por plantilla v3.0'),
 (26,'-u','adjetivo','adjetivo_simple',1,0,NULL,'áku',4,'fijado','D.03 adjetivo simple; par morfológico del adverbio -umen'),
 (27,'-sióno','sustantivo','accion_abstracta',1,1,'ó','aksióno',7,'propuesto','D.05 registro explícito de la regla t→s (misma función que cad. 7)'),
 (28,'-dóro','sustantivo','agente_general',1,0,'ó','akdóro',5,'propuesto','D.07 alomorfo post-consonántico sin vocal de apoyo (cf. -adóro)'),
 (29,'-tório','sustantivo','lugar',1,0,'í','aktório',9,'propuesto','D.08 alomorfo pleno de -dório (cad. 9): conserva -t- ante -r'),
 (30,'-tro','sustantivo','instrumento',1,0,NULL,'áktro',10,'fijado','D.10 instrumento (lat. -trum); áktro es llana → tilde en á por hiato/regla general'),
 (31,'-íto-pac','sustantivo','paciente',1,0,'í','kasíto',20,'propuesto','D.11 paciente; COLISIÓN morfológica con diminutivo -íto (E.01): desambiguación por rol sintáctico (pat); ejemplo alternativo kasíto para no duplicar aktíto'),
 (32,'in-','adjetivo','negacion_adjetival',1,0,NULL,'inaktívu',11,'fijado','D.14 prefijo negativo (carga funcional a la izquierda, doc. maestro §1)'),
 (33,'de-','verboide','reverso',1,0,NULL,'deaktâr',12,'fijado','D.16 prefijo reversivo'),
 (34,'re-','verboide','iterativo',1,0,NULL,'reaktâr',13,'fijado','D.17 prefijo iterativo');

-- =====================================================
-- BLOQUE 2 — Faros de Aspecto (5)
-- =====================================================
INSERT OR IGNORE INTO faros_aspecto (codigo,funcion,tipo,formula,auxiliar,forma_dependiente,ejemplo_ak,glosa_es,nota) VALUES
 ('F.01','base / durativo','analitico','âs + inf','âs','inf','âs aktâr','actuar / está actuando','marca verbal âs (tabla marcas_verbales)'),
 ('F.02','incoativo','analitico','áin + inf','áin','inf','áin aktâr','empieza a actuar','nuevo faro; candidato a fusión con īn (pila_preverbal capa 2)'),
 ('F.03','progresivo','analitico','áes + ger(-ând)','áes','gerundio','áes akând','está actuando (ahora)','gerundio akând = raíz+VT â+nd (cad. 1); áes ≠ âs (distinción acentual fonémica)'),
 ('F.04','perfectivo','analitico','â + part(-ât)','â','participio','â aktât','actuó / ha actuado','participio aktât = tema -t- + -ât (cad. 2); marca perfectiva â'),
 ('F.05','perfecto / estativo','analitico','âstu + adj(-âtu)','âstu','adjetivo','âstu aktâtu','está actuado (estado)','resultativo -âtu derivado del participio; paralelo de estar');

-- =====================================================
-- BLOQUE 3 — Pila Preverbal: modales/evidenciales (22)
-- =====================================================
INSERT OR IGNORE INTO pila_modales (codigo,funcion,auxiliar,contraccion,seleccion,ejemplo_ak,glosa_es,nota) VALUES
 ('O.01','causativo','kās',NULL,'âs + inf','kās âs aktâr','hacer actuar',NULL),
 ('O.02','permiso','līs',NULL,'âs + inf','līs âs aktâr','autorizado a actuar',NULL),
 ('O.03','prohibición','vēt',NULL,'âs + inf','vēt âs aktâr','prohibido actuar',NULL),
 ('O.04','capacidad','pōv',NULL,'âs + inf','pōv âs aktâr','poder actuar','el doc. maestro registraba la variante pōt; v3.0 fija pōv'),
 ('O.05','obligación','dēv',NULL,'âs + inf','dēv âs aktâr','deber actuar','ya atestiguado en documento-maestro (§modales)'),
 ('O.06','conativo','tēnt',NULL,'âs + inf','tēnt âs aktâr','intentar actuar',NULL),
 ('O.07','habitual','sūl',NULL,'âs + inf','sūl âs aktâr','soler actuar',NULL),
 ('O.08','síncrono','sīnc',NULL,'âs + inf','sīnc âs aktâr','actuar simultáneamente','coincidente con sīnc de pila_preverbal capa 2 (aspectual)'),
 ('O.09','asíncrono / serial','dēsinc',NULL,'âs + inf','dēsinc âs aktâr','actuar en serie','coincidente con dēsinc capa 2'),
 ('O.10','volición / futuro','vōl','v''âs','âs + inf','v''âs aktâr','quiere actuar / actuará','elisión obligatoria vōl + âs → v''âs'),
 ('O.11','memoria / pasado','mnē','mn''âs','âs + inf','mn''âs aktâr','actuó (lo recuerda)','pasado episódico/experiencial; complementa prē (pasado general de tiempos)'),
 ('O.12','evidencia directa','dīr',NULL,'âs + inf','dīr âs aktâr','lo vi actuar',NULL),
 ('O.13','evidencia reportada','rēp',NULL,'âs + inf','rēp âs aktâr','dicen que actúa',NULL),
 ('O.14','evidencia inferida','īnf',NULL,'âs + inf','īnf âs aktâr','deduzco que actúa',NULL),
 ('O.15','certeza','cēr',NULL,'âs + inf','cēr âs aktâr','seguro que actúa',NULL),
 ('O.16','probabilidad','prōb',NULL,'âs + inf','prōb âs aktâr','probablemente actúa',NULL),
 ('O.17','posibilidad hipotética','pōs',NULL,'âs + inf','pōs âs aktâr','quizás actúa',NULL),
 ('O.18','hipótesis','hīp',NULL,'âs + inf','hīp âs aktâr','supongamos que actúa',NULL),
 ('O.19','asunción','asūm',NULL,'âs + inf','asūm âs aktâr','doy por sentado que actúa',NULL),
 ('O.20','simulación','sīm',NULL,'âs + inf','sīm âs aktâr','parece que actúa',NULL),
 ('O.21','mandato','mānd',NULL,'inf solo','mānd aktâr!','¡actúa! (orden)','imperativo: mānd rige infinitivo desnudo (sin âs)'),
 ('O.22','necesidad','nēc',NULL,'âs + inf','nēc âs aktâr','es necesario actuar',NULL);

-- =====================================================
-- BLOQUE 4 — Cinematografía Cognitiva (8)
-- =====================================================
INSERT OR IGNORE INTO focos_cognitivos (codigo,funcion,operador,rol_alineado,ejemplo_ak,glosa_es,nota) VALUES
 ('C.01','visión absoluta','ābs',NULL,'ābs âs aktâr','actuar (plano general)','marco objetivo/desmarcado'),
 ('C.02','visión relativa','rēl',NULL,'rēl âs aktâr','actuar (marco subjetivo)',NULL),
 ('C.03','foco sujeto','sū','Agente (ag)','sū aktâr','él actúa (énfasis en agente)',NULL),
 ('C.04','foco paciente','pāc','Paciente (pat)','pāc aktâr','es actuado (énfasis en objeto)','desinencia -om en el SN focalizado'),
 ('C.05','foco locativo','lōk','Espaciotiempo (ub)','lōk aktâr','allí se actúa','alineado con macrogrupo UB de la ontología'),
 ('C.06','foco instrumental','īns','Instrumento (it)','īns aktâr','con esto se actúa',NULL),
 ('C.07','foco beneficiario','bēn','Propósito (fin)','bēn aktâr','para él se actúa',NULL),
 ('C.08','espejo (reflexivo)','sē',NULL,'sē aktâr','actuar sobre sí mismo',NULL);

-- =====================================================
-- BLOQUE 5 — Evaluativos (3) → motor en cadenas 14-18; registro aquí
-- =====================================================
INSERT OR IGNORE INTO predicacion (codigo,funcion,tipo,formula,ejemplo_ak,glosa_es,nota) VALUES
 ('E.01','diminutivo afectivo','sintetico','{R}+{VT}+-íto / -íta','aktíto / aktíta','actito (pequeño, querido)','cadenas 14/15; documentada colisión con D.11 (paciente)'),
 ('E.02','despectivo','sintetico','{R}+{VT}+-étto / -étta','aktétto / aktétta','actucho (insignificante)','cadenas 16/17'),
 ('E.03','aumentativo','sintetico','{R}+{VT}+-átsu','aktátsu','actazo (grande, intenso)','cadena 18');

-- =====================================================
-- BLOQUE 6 — Determinantes y Colectivos (10)
-- =====================================================
INSERT OR IGNORE INTO determinantes_colectivos (codigo,funcion,tipo,forma,ejemplo,glosa_es,nota) VALUES
 ('T.01','colectivo dual','sintetico','ám- + pron.','ámbe akdóro','ambos actores',NULL),
 ('T.02','colectivo plural','sintetico','cóm- + pron.','cómbe akdóro','la manada de actores',NULL),
 ('T.03','distributivo','analitico','kad un','kad un akdóro','cada uno actúa',NULL),
 ('T.04','numeral','analitico','raíz dígito','du ákto','dos actos','con cuantificador explícito se suprime el plural (doc. maestro)'),
 ('T.05','ordinal','sintetico','{-dígito}ín','ákto duín','segundo acto','ordinal pospuesto al SN; lectura [ákto [duín]]'),
 ('T.06','cuantitativo','analitico','múlto','múlto ákto','muchos actos',NULL),
 ('T.07','partitivo','analitico','pat di','pat di ákto','parte del acto',NULL),
 ('T.08','fracción','sintetico','-fra / párte','ákto trífra','un tercio del acto',NULL),
 ('T.09','multiplicativo','sintetico','-plo','ákto tríplo','acto triple',NULL),
 ('T.10','colectivo numérico','sintetico','-áro','ákto triáro','terna de actos','-áro reservado a colectivos numéricos (evita confusión con denominal -óre)');

-- =====================================================
-- BLOQUE 7 — Marcadores Relacionales (13)
-- =====================================================
INSERT OR IGNORE INTO conectores (codigo,funcion,particula,ejemplo,glosa_es,nota) VALUES
 ('R.01','comitativo','kun','kun akdóro','con el actor',NULL),
 ('R.02','instrumental','ut','ut áktro','con el instrumento',NULL),
 ('R.03','abesivo','sin','sin aktâr','sin actuar',NULL),
 ('R.04','benefactivo','pa + pron.','pa miôt','para mí','miôt = pronombre de 1ª persona oblicuo/focalizado'),
 ('R.05','espacial','ub / in','ub aktório','en el lugar','ub = marcador ubento (roles.ub)'),
 ('R.06','temporal','ant / post','post aktâr','después de actuar',NULL),
 ('R.07','posesivo','di / contracción','di ákto mid','mi acto','mid = posesivo átono enclítico'),
 ('R.08','causal (lógica)','re','re aktâr','porque actúa',NULL),
 ('R.09','final','pa','pa aktâr','para actuar',NULL),
 ('R.10','consecutivo','ton','ton aktâr','así que actúa',NULL),
 ('R.11','condicional','si','si aktâr','si actúa',NULL),
 ('R.12','concesivo','dem','dem aktâr','aunque actúa',NULL),
 ('R.13','adversativo','sed','sed aktâr','pero actúa',NULL);

-- =====================================================
-- BLOQUE 8 — Cuantificadores Lógicos (4)
-- =====================================================
INSERT OR IGNORE INTO cuantificadores_logicos (codigo,funcion,formula,ejemplo_ak,glosa_es,nota) VALUES
 ('Q.01','∃ afirmativo','úno + N','úno akdóro','alguien que actúa','coherente con doc. maestro: úno persóno/kóso'),
 ('Q.02','¬∃ negativo','no úno + N / No','No akdóro','nadie actúa','negación exocéntrica no; doble lectura (oracional / NP)'),
 ('Q.03','∀ afirmativo','ómno + N','ómno akdóro','todos actúan',NULL),
 ('Q.04','¬∀ negativo','no ómno + N','no ómno akdóro','no todos actúan','¬∀ ≠ ∃¬: el orden lineal estricto preserva la lectura escopada');

-- =====================================================
-- BLOQUE 9 — Predicación de Cualidad y Capacidad (5)
-- =====================================================
INSERT OR IGNORE INTO predicacion (codigo,funcion,tipo,formula,ejemplo_ak,glosa_es,nota) VALUES
 ('P.01','cualidad general','analitico','âs + adj(-u)','âs aktívu','es activo','atribución esencial (ser)'),
 ('P.02','cualidad temporal','analitico','âstu + adj','âstu aktívu','está activo (ahora)','estado cambiante (estar); mismo auxiliar que F.05'),
 ('P.03','capacidad pasiva','sintetico','-áblu','âs aktáblu','es actuable','cadena 4 (posibilidad)'),
 ('P.04','capacidad activa','analitico','pōv + inf','pōv âs aktâr','puede actuar','proyección predicativa de O.04'),
 ('P.05','negación operativa','analitico','no / ñâs','ñâs aktívu','no es activo','no = negación proposicional; ñâs = negación atributiva/categoremática');

-- =====================================================
-- FIN — Plantilla Maestra v3.0 (90 ítems: 20+5+22+8+3+10+13+4+5)
-- =====================================================
