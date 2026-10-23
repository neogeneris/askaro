# REPORTE DE FONDEO SINTESIO × ASKÁRO — Iteración de cierre (auto-poda6)

Fecha: 2026-10-23 · BD: `sintesio.db` (WAL, FK ON, `PRAGMA integrity_check` = ok)
Backups: `sintesio.db.bak-prepoda4` (previo a reclasificación de fauna),
`sintesio.db.bak-prepoda6` (previo a esta iteración).

## Nota de canon

**52 modificadores es el canon real** de la tabla `modificador`. El "inventario de 40"
del prompt original era un error. La supuesta poda de 12 fuera de canon resultó
innecesaria: ya estaban reasignados/borrados en iteraciones previas.

## Decisión metodológica 1 — NO recalcular la matriz desde el grafo

Se simuló la regla (≥1 arista alta → alta; ≥2 medias → media; resto → baja):
538 sustantivos cambiarían de estrato y la confianza alta saltaría a **84,8%**.
**Decisión: NO aplicar.** Es inflación estructural: `anim_*` y `dim_*` se asignan por
ubicuidad (casi todo sustantivo recibe una arista de estos ejes), no por certeza
semántica. **El número real de confianza alta en matriz es 43,6%** y se mantiene sin
forzar al umbral del 50%.

---

## 1. Totales finales

| Métrica | Valor |
|---|---|
| Sustantivos (corpus Askáro) | 1.041 |
| Modificadores (canon) | 52 |
| Aristas en el grafo | 1.721 |
| Nodos del árbol | 24 |
| Sustantivos con ≥1 arista | 1.041 (100%) |
| Pendientes explícitos (0 aristas) | **0** — el UPDATE de pendientes no marcó nadie |
| Contradicciones animado∧abstracto | 0 |
| Aristas huérfanas (FK) | 0 |
| Celdas matriz incompletas | 0 |

## 2. Distribución de confianza en MATRIZ (real, sin forzar)

| Estrato | n | % |
|---|---|---|
| alta | 454 | 43,6% |
| media | 298 | 28,6% |
| baja | 289 | 27,8% |

(La pasada poda6 añadió aristas de confianza media en el **grafo**; la confianza global
de cada sustantivo en matriz no se tocó — decisión 1.)

## 3. Aristas por sustantivo

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| sustantivos | 661 | 201 | 105 | 44 | 15 | 13 | 2 |

Media: **1,65**. Máximo 7 (justificado: términos multidimensionales como papa/toro).

## 4. Pasadas de clasificación registradas

- `auto-poda4: matching normalizado` — fauna: 119 aristas (media).
- `auto-poda6: matching normalizado` — sociedad/género/aproximación: **14 aristas nuevas** (media):
  soc_sagrado 4 (sacerdote, monje, monja, obispo) · soc_fem 5 (madre, soróra, soróro, hermana×2) ·
  soc_masc 3 (padre, frátro, toro) · soc_respetado 1 (kapitáno) · soc_divino 1 (éo/dios).
- `auto-poda6: unidad temporal inherente` — 0 aristas nuevas (ver §5).

### Hallazgos honestos de la verificación

1. **Estado previo**: los 6 "fallos de matching" ya estaban parcialmente cubiertos por
   clasificaciones semánticas anteriores (soc_respetado/soc_sagrado/soc_divino aparecían
   "sin uso" en mi conteo anterior por un bug de set-complement en el script de métricas —
   corregido aquí con SQL directo).
2. **Patrones del prompt vs. corpus**: de las palabras pedidas, **no existen** en Askáro:
   líder, jefe, anciano, deidad, ángel, macho, hembra, mucho, varios, algunos, pocos, año
   ("año" solo existe como homónimo *ano* = pato; no se clasificó como temporal para no
   contaminar al ave). Papa/monja aparecen duplicados (papa secular + pápo pontificio;
   dos formas de "hermana", tres de "vaca"); INSERT OR IGNORE evitó duplicados exactos.
3. **Detección de falsos positivos**: 'ángelus'→ángel daría soc_divino falso (abs_mental);
   'año'→anio daría auto_temporal falso sobre ano=pato. Se excluyeron ambos.
4. **Higiene**: 20 aristas preexistentes (con sistema_origen='australiano') quedaron
   etiquetadas erróneamente con la nota poda6 por colisión de texto; limpiadas.
5. **Deuda técnica detectada**: el UNIQUE(sustantivo_id, modificador_id, sistema_origen)
   permite **134 pares dupeados** differing solo en sistema_origen (toro→val_peligroso×2,
   gallina×2, etc.). No se podaron (fuera de alcance); candidatos a dedupe en próxima iteración.

## 5. Revisión flujo / auto_* (decisión documentada)

- **hora → auto_temporal**: SÍ procede, pero la arista **ya existía** (pasada abs_temporal).
  Añade coherencia vietnamita; nada nuevo que insertar.
- **año**: inexistente como temporal en el corpus (§4.2). Hueco mantenido.
- **metro → auto_medida**: **NO**. 'métro' en Askáro significa *medida* genérica, no unidad
  de medida inherente (unidades tipo metro/kilo no están lexicalizadas como clase). Forzarlo
  sería inventar. Hueco mantenido.
- **río/flúvio → flujo**: **NO**. En el sistema vietnamita que valida `flujo`, marca ANIMADOS
  que se mueven por flujo, no masas de agua estáticas. 'flumíno' ya lleva cons_denso+dim_3d y
  'agua' lleva cons_liquido, que captura el rasgo relevante. Extenderlo a inanimados sería
  inventar una atestiguación nueva. Hueco mantenido.

## 6. Los 11 modificadores sin uso: hueco real vs. dominio

| Modificador | Tipo | Motivo |
|---|---|---|
| loc_exacto | **Hueco estructural** | Askáro no tiene sustantivos locativos (son preposiciones/adposiciones) |
| loc_direccional | **Hueco estructural** | ídem |
| loc_interior | **Hueco estructural** | ídem |
| forma_esf_art | **Hueco de corpus** | sin esféricos artificiales explícitos en el léxico |
| val_peyorativo | **Hueco de corpus** | léxico denotativo neutro; sin sustantivos peyorativos |
| flujo | **Hueco lingüístico** | solo animados por flujo (vietnamita); ningún candidato válido (§5) |
| auto_medida | **Hueco de corpus** | Askáro no lexicaliza unidades de medida como sustantivos de clase (§5) |
| cant_aprox | **Hueco de categoría gramatical** | 'mucho/varios/pocos' son pronombres/determinantes, no sustantivos del corpus |
| cant_conjunto | **Hueco de corpus** | sin sustantivos colectivos explícitos |
| tam_extra_g | **Hueco morfológico** | aumentativos extremos bantúes son morfología, no léxico |
| tam_extra_p | **Hueco morfológico** | idem diminutivos |

Ninguno queda como "fallo de matching pendiente": los 6 sociales fueron cubiertos en §4.

## 7. Seam ñ / acentos (nota para la próxima iteración)

`termino_norm`/`espanol_norm` eliminan ñ→n y acentos, pero los IDs de modificador los
conservan (`tam_pequeño`). Un patrón normalizado 'pequeno' nunca matchea el id `tam_pequeño`
(causó un fallo de FK en poda3). Mitigación actual: matching solo sobre columnas `*_norm`
de sustantivo; ids literales. Futuro: NFD + strip combining marks en tablas de lookup o
mapa explícito norm→id. **Además**: 'año'→'anio' colisiona con 'ano' (pato) — mismo seam,
dirección inversa; verificar homófonos normalizados antes de cualquier matching futuro.

## 8. Criterios de éxito (corregidos) y estado real

| Criterio | Estado |
|---|---|
| ≥1 arista de alta/media O pendiente explícito | ✅ 100% (1.041/1.041; pendientes: 0) |
| 100% de sustantivos con arista o pendiente explícito | ✅ |
| Todas las celdas de matriz con valor (aunque N/A) | ✅ |
| Sin contradicciones (animado=sí ∧ abstracto=sí) | ✅ 0 |
| Confianza alta ≥50% | ❌ **43,6% — deliberado** (decisión 1: no forzar; el 84,8% derivable del grafo es inflación estructural) |
| Árbol cubre ≥80% | ✅ |
| ≥20 modificadores en uso | ✅ **41/52** |
| Modificadores sin uso documentados como huecos | ✅ (§6) |

## 9. Deudas pendientes

1. **Cobertura vs. confianza**: promover media→alta exige gold standard manual (~100 términos), no reglas ciegas.
2. **Densidad (1,65 aristas/sust)**: pasadas análogas para herramientas/alimentos restantes; no inflar con aristas débiles.
3. **Dedupe de pares con distinto sistema_origen** (134 casos) — decidir política: ¿fusión con nota o preservación multidimensional?
4. **Huecos estructurales** (§6): ampliar léxico Askáro o declarar permanentes locativos/medida/colectivos.

## 10. Los 10 sustantivos más difíciles de clasificar

| Término | Español | Problema |
|---|---|---|
| pneuma | espíritu/aire | animado vs. abstracto vs. masa-gas; triple rama |
| skia | sombra | inmaterial no abstracto; sin hoja clara en el árbol |
| selene | luna | celeste: ¿3D o sagrado? estatus sin evidencia classifier |
| helios | sol | ídem; candidato divino no atestiguado |
| onar | sueño | estado mental vs. entidad; auto_clasif dudoso |
| chronos | tiempo | abs_temporal; frontera con flujo/auto_temporal |
| hydor | agua | masa sin dimensionalidad fija (líquido vs. contenedor) |
| pyr | fuego | ¿denso? ¿peligroso? categoría intermedia clásica |
| moira | destino/parte | abstracto + cantidad + social simultáneos |
| kardia | corazón | órgano par/no-par dudoso; dimensión ambigua |

(Todos con confianza baja/media y nota de caso pendiente donde corresponde.)

## Entregables

- `sintesio.db` — completa, WAL, FK verificada (integrity_check ok)
- `sintesio_matriz.csv` — 1.041 filas + header; columna `sintesis` recalculada desde el grafo
- `sintesio_grafo.dot` — 1.721 aristas coloreadas por confianza; 11 nodos sin uso en gris discontinuo
- `sintesio_arbol.yaml` — 24 nodos
- `sintesio_reporte.md` — este documento

---

## 9. Gold Standard — Selección de 100 términos (TAREA 1, iteración gold)

**Tabla:** `gold_standard` (separada de la clasificación automática; no la reemplaza, la valida).
**Estado:** los 100 términos están SELECCIONADOS pero NO clasificados a mano (`clasificado_por='pendiente'`). La curaduría es trabajo del humano/curador.
**Reproducible con:** `python gold_select_final.py` (semilla fija: ROW_NUMBER por id + random.seed(100)).
**CSV para curar:** `sintesio_gold.csv` (columnas lista para anotar veredicto del curador).

### Estratificación solicitada y cumplida
| Estrato | n | Función |
|---|---|---|
| media | 40 | candidatos a promoción |
| baja | 30 | casos que el agente no supo clasificar |
| alta | 20 | control de bugs |
| azar (seed=100) | 10 | control de sesgo |

### Diversidad
- **16 grupos distintos representados** (≥10 requerido): sociedad 13, cuerpo 14, tecnologia 11, naturaleza 9, educacion 8, deporte 8, economia 7, casa 6, nsm 5, geografia 5, comida 4, arte 3, sin-grupo 3, parentesco 2, familia-k 1, abstracto 1.
- **Máximo por grupo: 14** (≤15 requerido).
- Mezcla animados/abstractos/inanimados: animados(matriz)=10, abstractos=38, inanimados=52 (en total; por estrato abajo).

### Desviaciones documentadas respecto al enunciado
1. **Estratos media y baja no contienen NINGÚN sustantivo con animado='si'** en matriz_rasgo (los 131 animados del corpus son todos confianza alta; consecuencia de las pasadas de fauna previas). Para garantizar mezcla de animacidad se incluyeron **5 proxies animales del estrato baja** (káta/gata, gátto/gata, avéso/ave, passéro/gorrion, pengíno/pengüino), marcados en `nota_curador='proxy-animal (matriz dice animado=no)'`. Estos casos son además **detectores de error sistemático**: si el curador confirma que son animados, la heurística de animacidad tiene un bug de asignación de confianza. En el estrato media no existe ni siquiera un candidato animal (0 sustantivos naturaleza/comida en media), por lo que ese estrato queda abstracto/inanimado por construcción — registrado como limitación del muestreo, no forzado.
2. El enunciado se cortó tras "TAREA 1" (faltan TAREAS 2+). Solo se ejecutó la selección; no se midió tasa de acierto porque aún no hay clasificaciones manuales que comparar.

### Siguiente paso (fuera de esta tarea)
El curador completa `sintesio_gold.csv` / `gold_standard.clasificado_por`; entonces se calcula la tasa de acierto por estrato y se decide la promoción media→alta término por término (nunca por regla ciega del grafo — ver decisión §8).
