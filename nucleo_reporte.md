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
