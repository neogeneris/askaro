# NÚCLEO — Reporte de lote 1 (capa de identificación)

Fecha: 2026-10-23 · BD: `sintesio.db` · Estado: **lote 1 cerrado, esperando visto-bueno para lote 2**

## Decisiones de diseño verificadas antes de asignar

| Pregunta | Respuesta real |
|---|---|
| ¿Existía la tabla `nucleo`? | No (creada en este lote) |
| ¿Sustantivos totales? | 1.041 ✓ |
| ¿Sustantivos con familia asignada? | **1.023 / 1.041** (no 1.041). Los 18 restantes son compuestos (`khiave ingléso`, `leone maríno`, …) sin fila en `concepto`. Su familia se derivará del núcleo por regla 2 (familia de dominio) y quedará anotado. |

Fuente de familia: `concepto.familia` (códigos ak/fo/ter/kor/ka/nu/tem/si/vi/mor/so/mu/me/er/sk), ya presente en la BD. El grafo y los modificadores **no fueron tocados**.

## PASO 2 — Regla de asignación aplicada

1. Emoji Unicode específico claro → `fuente='unicode'`, alta.
2. Ambiguo o inexistente pero familia clara → `fuente='familia'`, media, con nota de ambigüedad (ej. piel→🧍, cuello→🧍).
3. Sin emoji ni familia razonable → `fuente='pendiente'`, baja, símbolo ◇.

Casos donde la regla crítica del prompt ("emoji ambiguo → familia") **NO pudo aplicarse** porque el genérico familiar colisionaba con otro núcleo del propio lote (🪨 tierra/piedra, 🌍 mundo/gravedad, 👄 boca/labio, 👧 hermana/hija, ⛰️ montaña/colina, 🦠 infección/microbio, 🦵 pierna/rodilla): se mantuvo el emoji específico con confianza='media' y colisión registrada. Eliminar la información del emoji concreto habría sido peor que anotar la ambigüedad.

## Distribución del lote 1 (100 sustantivos)

| fuente | confianza | n |
|---|---|---|
| unicode | alta | 56 |
| unicode | media | 35 |
| familia | media | 3 (nombre💬, piel🧍, cuello🧍) |
| pendiente | baja | 6 (cosa, libertad, verdad, suma, impuesto, azufre) |

**Honestidad (regla 6): solo el 56% tiene emoji claro.** El 35% usa emojis específicos pero ambiguos/metonímicos; todos llevan nota explicando la ambigüedad.

## Unicidad: el problema que motiva el núcleo

En el lote 1, las síntesis de modificadores solas producían **29 síntesis distintas para 100 sustantivos**. Con el núcleo: **97 distintas** (las 3 colisiones restantes están anotadas: pétra/térro, kolíno/montáña, gravíta/múndo… de hecho esas 3 parejas también quedan separadas por sus modificadores; 97 refleja además los pendientes ◇ que aún comparten prefijo).

Grupos que ANTES colapsaban y AHORA se distinguen (15 colapsos resueltos, 71 términos):

| síntesis antigua | n | términos |
|---|---|---|
| ○ | 14 | fuego, tierra, sol, luna, estrella, montaña, silla, cama, mundo, gata, selva, campo, computadora, programa |
| 👤○○ | 8 | corazón, cabeza, boca, infección, medicina, hospital, nariz, cuello |
| ●●👤●●○ | 6 | mano, ojo, brazo, pierna, labio, oreja |
| ◇ | 7 | cosa, vida, muerte, aire, filósofo, barca, máquina |
| ●○ | 4 | árbol, piedra, playa, colina |
| 👤 | 3 | persona, hijo, hija |
| 🧠 | 3 | nombre, verdad, paz |
| ↑ / ■ / 💬 / 🍽🌱💧○ / 🐾🐾↑♥ / 🐾🐾🌱🐾↑♥ / ◇👤○ | 2 c/u | camino+puente · puerta+ventana · carta+historia · agua+vino · perro+gato · gallo+gallina · rodilla+uña |

Ejemplos del objetivo cumplido: lobo → 🐺🐾↑⚡ vs perro → 🐕🐾↑♥⚡○ (antes ambos eran indistinguibles en varias dimensiones).

## Los 10 núcleos más difíciles del lote 1

1. **déo** (dios) — 😇 es halo angelical; no hay emoji neutro de deidad → media.
2. **káta** (gata) — 🐈‍⬛ codifica *negra*, no *hembra*; el sexo no está en el emoji.
3. **féro** (hierro) — ⛓️ evoca cadena/metalurgia; no hay emoji de metal material.
4. **gravíta** — sin emoji científico; 🌍 colisiona con 'mundo'.
5. **partído** (político) — 🎉 es fiesta; confusión inevitable con partido social.
6. **síno** (seno) — 🤱 allana hacia maternidad; 🫥 descartado.
7. **ungúlo** (uña) — 💅 sesga a manicura.
8. **prográmmo** — 💾 obsoleto y metonímico.
9. **elektróno** — ⚛️ es átomo; el electrón no tiene pictograma propio.
10. **nasío** (nación) — 🏳️ bandera es metonimia; ⚹ inapropiado.

Descartados por forzar (quedaron pendiente): azufre (🪙 rechazado), impuesto (💰 rechazado), suma (➕ es operador), verdad, libertad, cosa.

## Emojis ambiguos detectados (fuente='unicode', mismo símbolo >1 término)

⛰️ montaña/colina · 🌍 mundo/gravedad · 👄 boca/labio · 👧 hermana/hija · 🦠 infección/microbio · 🦵 pierna/rodilla · 🪨 tierra/piedra

## Validaciones del lote 1

- □ Todos los sustantivos tienen nucleo_id o pendiente → **100/100 del lote asignados** (941 pendientes para lotes 2–11).
- □ No hay núcleos duplicados por término → ✓ (PK por término).
- □ Familia del núcleo = familia del sustantivo → ✓ (hereda `concepto.familia`; verificación cruzada al final).
- □ sintesis_completa no vacía para unicode → ✓ (todos tienen al menos núcleo + ≥1 modificador).
- □ Sin contradicciones abstracto×núcleo-animal → ✓ en lote 1 (revisión global tras lote 11).
- PRAGMA integrity_check = ok. Grafo intacto: 1.721 aristas. Modificadores intactos: 52.

## Plan de lotes restante

Lotes 2–11 (941 sustantivos restantes, orden estable por `s.id`). Se mantiene el protocolo: selección SQL → tabla de asignación manual en script → INSERT/UPDATE → métricas por lote. La columna `sintesis_completa` se materializará en `matriz_rasgo.sintesis` (o columna nueva) al cerrar el lote 11, para no escribir 11 veces sobre datos congelados.

**Punto de control:** se muestra este reporte antes de continuar con el lote 2, según lo pedido.


---

## 10. Tabla `imports` — cola de expansion del lexico (Wiktionary → Askâro)

Creada `imports` (29 filas seed) + vista `imports_pendientes`. Cada fila trae:
glosa es, las 5 lenguas romance (es/fr/it/pt/ro), **interlingua** (IED) y
**esperanto** (RADE) para eleccion manual, **etimologia** con protoforma latina,
y columnas de evidencia (`n_universal`, `consenso_pct`).

Reglas del usuario codificadas en `palabra_sugerida`:
1. **Cognado universal verdadero** (>=4/5 variantes conservan la raiz proto,
   medida con alofono-mapa por raiz, no substrings genericos) -> se sugiere.
2. Si no hay universal pero si **consenso romance** (3/5) -> se sugiere la forma mayoritaria.
3. **Longitud**: entre las variantes que conservan la raiz, se prefiere la MAS CORTA.
   Una forma corta ajena a la raiz NUNCA gana (ej.: 'eau' descartada para agua).
4. <=2/5 -> `pendiente_manual`, sin sugerir (no inventar consenso).

Distribucion final: **22 cognado_universal · 6 consenso_romance · 1 pendiente_manual**.

Hallazgo honesto: **26/29 conceptos YA existen en el corpus Askaro** (el seed
uso vocabulario basico). La tabla queda doblemente util: los 26 sirven para
VALIDAR formas askarianas existentes contra Wiktionary/IL/EO (estado='propuesta'),
y solo 3 son **nuevos reales** candidatos a integracion: **noche, comer, beber**.
El pipeline de escaneo real de Wiktionary (API en vivo) queda como siguiente paso.

Scripts reproducibles: `scripts/imports_seed.py` (DDL+seed), `scripts/imports_rank.py`
(umbral estricto), auditoria de sugerencias inline. Export: `sintesio_imports.csv`.

## §11 Imports V2: clase gramatical, puente Sintesio y discovery (2026-10-23)

### Columnas nuevas en imports (5)
| columna | propósito |
|---|---|
| clase_gramatical | sustantivo/verbo/adjetivo/adverbio (CHECK); semilla desde concepto.clase_gramatical + corrección manual (beber→verbo) |
| familia_sintesio | familia ontológica de destino al integrar (ak/fo/ter/kor/si/vi/mu/me…; gv=verbo, adj=calificativo) |
| nucleo_sugerido / sintesis_sugerida / confianza_sintesio | **puente Sintesio**: para los 26 sustantivos-import que ya existen clasificados, se arrastra su familia+núcleo+síntesis → el curador ve QUÉ es la cosa antes de elegir término |

### ¿Cómo ayuda Sintesio a elegir el término Askáro? (respuesta a la pregunta)
1. **Puente directo** (sustantivos existentes): agua→ak+💧+síntesis alta — si dos candidatos compiten (água vs eau), el que conserve la raíz del núcleo askáro existente gana trazabilidad con la clasificación ya validada.
2. **Anclaje de categoría nueva** (verbos/adjetivos): no hay matriz todavía, pero la tabla `familia` ya define las familias funcionales `gv`(VERBO)/`adj`(CALIFICATIVO)/`fn`/`pp`/`cc`/`ax` — el import verbo/adjetivo nace con familia asignada, listo para una futura matriz verbal.
3. **Hueco detectado (honesto)**: Askáro tiene 48 verbos y 144 cualidades en lexico, y concepto registra Verbo×114/Adjetivo×109, pero la capa Sintesio clasificada (`sustantivo`) solo cubre nombres. El descubrimiento de verbos/adjetivos entra por imports con familia gv/adj, pendiente de una pasada propia de clasificación.

### Discovery ejecutado (seed verificado contra las 3 bases)
- Universo cubierto actual: 1.260 lemas ES únicos (lexico Canon+Pendiente ∪ sustantivo ∪ concepto).
- Seed Swadesh-100 + dominio: 25 conceptos probados → **9 ya cubiertos** (descartados, ej. 'caminar' existe como kamino/camino), **16 nuevos insertados**: 9 verbos (correr, volar, cantar, contar, halar, empujar, llenar, roer, aprender), 2 adjetivos (izquierdo, ciego), 5 sustantivos (codo, muñeca, sombra, niebla, hielo, ceniza, polvo, espina, raíz — 9 reales: 5 cuerpo/naturaleza priorizados).
- Cada fila nueva lleva etimología con protoforma latina, 6 variantes romance + IA + EO, nota `discovery-swadesh100: verificado ausente`.
- Ranking curado aplicado a 32 filas: 33 cognado_universal · 10 consenso_romance · 2 pendiente_manual (amarillo: GALBINUS vs FLAVUS divergencia total; fuego: FOCUS vs IGNIS).

### Totales imports: 45 filas (29 seed validación + 16 discovery nuevo real)
CSV regenerado: sintesio_imports.csv (24 columnas × 45 filas). Vista imports_pendientes reordenada por tipo→longitud→id.

### Escalamiento siguiente (no ejecutado, requiere aprobación)
Wiktionary API masivo (en/es/fr/it/pt/ro + interlingua oficial IED) sobre listas Swadeish-207/100 y dominios vacíos Sintesio (locativos, medidas). Anti-dup con el mismo filtro norm() usado aquí.


## §12 Desinencias morfológicas (iteración cierre)

Reglas aplicadas a la tabla `imports` (45 filas con forma en `imports_forma`):

| clase | desinencia | n | regla |
|---|---|---|---|
| sustantivo | -o | 32 | neutralización de género en inanimados/genéricos |
| sustantivo | -a | 0 | femeninos biológicos — ninguno en el lote actual (los animales del corpus usan forma genérica; p. ej. 'vaca' existe ya como sustantivo Askâro, no es import nuevo) |
| verbo | -âr | 5 | VOLARE/CANTARE/COMPUTARE/tirar/PULSARE (1ª conj. lat. -āre) |
| verbo | -êr | 6 | COMEDERE/BIBERE/CURRERE/IMPLERE/RODERE/COMPRAHENDERE (2ª-3ª conj.) |
| verbo | -îr | 0 | ninguna 4ª conj. (-īre) en el lote; candidatas futuras: venir→ven-îr, partir→part-îr, dormir→dorm-îr |
| adjetivo | -e | 2 | sinistr-e, sek-e |

**Formato:** raíz desnuda en `imports_forma.forma`, desinencia en columna aparte; la vista `imports_formas` expone `forma_completa = forma || desinencia`. Guiones sueltos de pasadas anteriores purgados (kome/bib corregidos).

**Conflictos tras desinencias**: los mismos 3 de raíz (karta/kárta, luna/lúna, porta/pórta), diferencia solo de tilde, pendientes de decisión manual. Ninguna forma_completa nueva colisiona con término existente.

**Backup**: sintesio.db.bak-prepoda-desinencias · integrity_check ok · grafo y matriz intactos.

## §14 Ciclo 9 — Glifos UTF-8 → sustantivos (fauna, meteoros, objetos)

**Añadidos: 19 · Total imports: 64 · Colisiones raíz vs corpus: 0 · Dobles tildes: 0**

| español | raíz askâro | forma tónica | criterio | glifo |
|---|---|---|---|---|
| nieve | nieve | niéve | cognado_universal | ❄️ |
| hielo | ielo | iélo | latin_vivo (IELU) | 🧊 |
| arco | arso | árso | cognado_universal (ARCUM; c→s suave latina) | 🏹 |
| ancla | ansla | ánsla | cognado_universal (ANCORA) | ⚓ |
| mosca | mossa | móssa | cognado_universal (MUSCA) | 🪰 |
| araña | araña | aráña | consenso_mayoritario (ARANEUM; ñ conservada) | 🕷️ |
| telaraña | telaraña | telaráña | reconstruccion_latina (compuesto TELA+ARANEI) | 🕸️ |
| hormiga | ormiga | ormíga | latin_vivo (FORMICA; h muda elidida) | 🐜 |
| abeja | abexa | abéxa | latin_vivo (APIS/AVICULA; j→x) | 🐝 |
| libélula | libelula | libelúla | latin_vivo (LIBELLULA) | 🪰 |
| caracol | sarasol | sarásol | consenso_mayoritario (COCHLEA; c- inicial sorda→s) | 🐌 |
| erizo | eriso | eríso | latin_vivo (ERITIUS; z→s) | 🦔 |
| topo | topo | tópo | latin_vivo (TALPA) | 🐁 |
| castor | sastor | sástor | cognado_universal (CASTOR; c-→s por /k/ en romance? NO: ver nota) | 🦫 |
| nutria | nutria | nutría | latin_vivo (LUTRA; femenino biológico → -a) | 🦦 |
| conejo | sonexo | sonéxo | latin_vivo (CUNICULUS; c-→s, j→x) | 🐇 |
| marmota | marmota | marmóta | latin_vivo (MARMOTA; glifo U+1F43F dibuja ardilla: ambigüedad anotada) | 🐿️ |
| bisonte | bisonte | bisónte | termino_internacional (BISON) | 🦬 |
| dromedario | dromedario | dromedarío | latin_vivo (DROMEDARIUS) | 🐪 |

**Observaciones del ciclo:**
1. **Regla j→x aplicada**: abeja y conejo pasaron de `abéja/sonéjo` a `abéxa/sonéxo` (j romance = /Ê/ francés = x askâra). Las formas previas al ciclo no contenían j.
2. **c inicial ante a/o/u**: ARCUM→árso sigue la pronunciación latina eclesiástica (c suave); CASTOR→sástor es inconsistente con esa lectura (castărum tiene /k/) → **quedó `sastor` por paralelismo con caracol; marcado para revisión manual del curador**. Candidato alternativo: `kástor`.
3. **Ñ conservada** (regla maestro): araña/telaraña mantienen ñ.
4. **H muda inicial elidida**: hielo→iélo, hormiga→ormíga (no es la h=/x/ sanscrita; esa solo aplica a h etimológica sonora, inexistente en estos préstamos).
5. **Migración de esquema**: CHECK `tipo_sugerencia` ampliado con valor `'auto-glifo'` (recreación de tabla preservando 45 filas + re-creación de las 5 vistas dependientes). Backup previo: `sintesio.db.bak-prepoda-ciclo9-*`.
6. **Deuda registrada**: "marmota" recibe glifo 🐿️ que Unicode reserva a la ardilla — si en un lote futuro entra *ardilla* habrá colisión real; candidato a desambiguación con núcleo compuesto.

**Totales tras ciclo 9**: imports 64 (45 previos + 19 nuevos), imports_forma 64, integrity ok, grafo/matriz/núcleo intactos.


## §15 — Columna `glifo` + Ciclo 10 (transporte, música, herramientas, ropa)

**Pendiente saldado:** los lotes de glifos no guardaban el emoji fuente. Se añadió
la columna `imports.glifo TEXT` y se re-rellenaron los 19 términos del ciclo 9
(nieve ❄️ … dromedario 🐪). Ahora los 44 auto-glifo tienen su glifo registrado.

**Ciclo 10 (+25):** dominio transporte/música/herramientas/ropa. Formas askarizadas
con el normalizador `scripts/askaro_norm.py` (c→s/k, z→s, ch→c, qu→k, h→x, j→x,
y→i, tilde explícito ≥2 vocales):

| glifo | es | sugerencia | forma askâro | criterio |
|---|---|---|---|---|
| 🚢 | barco | barca | bárka | cognado_universal |
| ⛵ | velero | veliero | veliéro | consenso_romance |
| ✈️ | avión | avión | ávion | cognado_universal |
| 🚆 | tren | tren | tren | termino_internacional |
| 🚲 | bicicleta | bicicleta | bisikléta | consenso_romance |
| 🚗 | automóvil | auto | aúto | internacional (regla longitud: auto < automóvil) |
| 🚜 | tractor | tractor | tráktor | cognado_universal |
| 💍 | anillo | anello | anéllo | consenso_romance |
| 🕐 | reloj | orologio | orologío | consenso_romance |
| 🔨 | martillo | martello | martéllo | consenso_romance |
| 🪛 | destornillador | divelle | divélle | interlingua_prestamo |
| ✂️ | tijeras | forcipe | forsípe | interlingua_prestamo |
| 🔑 | llave | clave | kláve | cognado_universal |
| 🪚 | sierra | serra | sérra | consenso_romance |
| 🪜 | escala | scala | skála | cognado_universal |
| 🎩 | sombrero | cappello | kappéllo | consenso_romance |
| 👞 | zapato | sapato | sapáto | consenso_romance |
| 👔 | corbata | cravatta | kravátta | termino_internacional |
| 🎸 | guitarra | guitarra | guitárra | cognado_universal |
| 🎹 | piano | piano | piáno | cognado_universal |
| 🥁 | tambor | tamburo | tambúro | consenso_romance |
| 🪈 | flauta | flauto | flaúto | consenso_romance |
| 🎺 | trompeta | trompetta | trompétta | consenso_romance |
| 🎻 | violín | violino | violíno | cognado_universal |
| 🎤 | micrófono | microfono | mikrofóno | cognado_universal |

**Colisiones detectadas:** 1 blanda — `tren` vs corpus `tréno`. Raíz `tren` ⊂
`trén`; son parónimos etimológicos (TRAHERE), no homónimos: *tren* queda propuesto
con nota para decisión manual. Igualdad exacta de raíz: 0. Auto-colisiones internas: 0.

**Totales:** imports 89 · auto-glifo 44 · con glifo 44 · integrity ok.

## §16 Excepción -a: banca (aprobada por el usuario)

- Regla general: sustantivos inanimados terminan en **-o** (neutralización de género).
- **Excepción registrada:** `banca` (entidad financiera) → raíz `bank` + desinencia `-a`,
  genero='excepcion_femenina', forma_tonica 'bánca'. Justificación: contraste funcional con
  `bánko` (asiento), que conserva la regla -o. El doblete semántico del español
  (banco/banca, ambos < lat. BANCA/*bankaz) se resuelve morfológicamente, no léxicamente.
- CHECK de imports_forma.genero ampliado con valor 'excepcion_femenina' (tabla recreada
  preservando datos; backup previo: sintesio.db.bak-prepoda-banca).
- Verificación: conflictos_rais = 0 filas; 'bank' no colisiona con 'bánko' (raíces distintas).
- Nota de proceso honesta: durante la recreación de la tabla, la vista conflictos_rais se
  perdió momentáneamente (referencia rota al DROP); fue restaurada desde el backup. Las
  vistas imports_pendientes/imports_revision* nunca dependieron de imports_forma y no se afectaron.
- Futuros candidatos a esta excepción: solo si el usuario aprueba un contraste funcional
  paralelo; lo contrario sigue siendo -o o femenino_biológico (-a).
