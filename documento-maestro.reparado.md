# Askáro �� Especificación Formal V10.4 (Documento Maestro Unificado Monolítico)
## Interlingua Auxiliar de Base Neolatina (Romance Asiático)
**Fecha de Compilación:** 2026-10-10  
**Estado:** *Especificación Oficial Completa y Monolítica (V1.0 a V10.3)*

---

## 1. Arquitectura y Núcleo Axiomático

### 1.1 Principio de Isomorfismo y Neutro Base (`-o`)
La versión V5.7 de la Arquitectura de Lenguaje Comprimido y Determinista se fundamenta en un principio de **isomorfismo de traducción bidireccional (lossless translation)** e **invariancia funcional**:

1. **La terminación `-o` como Neutro Base Universal (Erradicación del Género Gramatical en Inanimados)**: A diferencia de los lenguajes naturales romances (donde *la carta*, *la mesa* o *el problema* tienen género gramatical arbitrario), en esta arquitectura **TODOS los objetos inanimados, conceptos y entidades abstractas utilizan strictly el Neutro Base en `-o`** (`kárto`, `méso`, `sistémo`, `dáto`, `káso`, `kóso`). Queda **estrictamente prohibido asignar la desinencia `-a` a objetos inanimados**.
2. **Flexión `-a` / `-or` Exclusiva para Sexo Biológico en Seres Vivos**: La flexión femenina en **`-a`** (o masculino específico en **`-or`**) se reserva **únicamente para seres vivos y agentes con sexo biológico** (`káto` -> `káta` *gata*, `usuário` -> `usuária` *usuaria*).
3. **Casos Nasales de Objetos Inanimados**: Al ser neutros en **`-o`**, el acusativo de todo objeto inanimado termina siempre en **`-om`** (`kártom`, `dátom`, `sistémom`, `kósom`), jamás en `-am`.


### 1.2 Regla de Eliminación de `pro-` (Positivo No Marcado / Economía de Marcas)
Se canoniza la simplificación morfológica y economía de marcas para la polaridad y tipificación nominal:
1. **Positivo No Marcado (Raíz Desnuda)**: El estado positivo o estándar de un concepto **no lleva prefijo** (`abérto`, `káldo`, `víto`, `lúso`). Se erradica el uso del prefijo `pro-` para marcar el estado positivo en reposo.
2. **Polo Negativo (`de-` / `a-`)**: El polo opuesto o inverso se marca con **`de-`** (`deabérto`, `dekáldo`, `devíto`) o **`a-`** para privación presencial (`alúso`).
3. **Tercer Polo / Inerte (`a-`)**: El estado neutro o inerte utiliza **`a-`** (`aabérto`, `akáldo`, `avíto`).

### 1.3 Modalidades de Representación: Scriptio Continua y Espaciado Universal
El lenguaje posee un diseño sintáctico determinista unificado que se adapta sin fricción a cualquier medio de transmisión:
1. **Scriptio Continua para Alta Densidad**: La omisión de espacios entre palabras es totalmente válida en flujos de datos o parsing informático en $O(1)$, ya que las fronteras de palabra, caso (`-om`, `-em`) y envoltura verbal (`ask-...-ár/-ér/-ír`) son deterministas.
2. **Espaciado Ortográfico Universal**: Para la lectura humana, la transmisión estándar y la síntesis de voz (TTS / Text-to-Speech), se utilizan espacios estándar entre palabras para garantizar la inteligibilidad visual y la prosodia natural.

### 1.4 Representación Intermedia Analítica (IR / Interlingua)
Askáro actúa como una **Representación Intermedia Reestructurada (IR)**. Todo texto de origen se descompone, desambigua y reestructura en sus componentes sintácticos explícitos:

`[Sujeto explícito/desambiguado] + [Pila Preverbal (5 capas)] + [Objeto-om / Dativo-em / Preposición] + ask-[Infijo]-Raíz-ár/-ér/-ír`

### 1.5 Tolerancia a Fallos, Préstamos y Nombres de Especies
El sistema está diseñado con una alta **resiliencia y tolerancia a fallos** frente a textos que contengan préstamos lingüísticos, palabras extranjeras o nombres técnicos no asimilados:
1. **Nombres de Especies y Términos Consolidados**: En especies animales o términos zoológicos/botánicos fijados por el uso común o la biología (por ejemplo, *mula*), **no se fuerza una masculinización artificial a *mulo*** si esto distorsiona la denominación estándar o genera confusión.
2. **Inserción de Palabras Extranjeras**: Si un texto contiene términos externos no asimilados (ej. *software*, *DNA*), las marcas circundantes (el artículo `la`, la preposición `to` o el marcador de acusativo `-om` si se acopla) permiten que el parser e interprete humano identifiquen el rol sintáctico sin que el sistema colapse.

---

### 1.6 Principio de Invariancia de la Raíz
Se establece como axioma fundamental de la arquitectura la **Invariancia Absoluta de la Raíz Léxica**:

1. **Carga Operativa a la Izquierda (Prefijación e Infijación)**: Toda la carga funcional y modificatoria de la oración ��incluyendo tiempo (`pr��`, `prō`), aspecto (`dūr`, `sinc`), modales (`mând`, `d��v`, `pōt`), negación (`no`), voz pasiva (`pās` / `-pas-`), derivaciones nominales (`ag-`, `ak-`, `kual-`, `inst-`, `lok-`, `kol-`, `dim-`, `aug-`, `dok-`, `pra-`) y prefijos verbales operativos (`-de-`, `-fal-`, `-kos-`, `-dos-`, `-re-`)�� es **estrictamente prefixal e infijal a la izquierda**.
2. **Raíz Intacta e Inmune**: La raíz o lexema base (`procés-`, `fok-`, `sistém-`, `dát-`, `kós-`, `ped-`) **permanece totalmente intacta, uniforme y libre de apofonía o deformaciones derivativas/conjugativas** en cualquier contexto sintáctico o discursivo.
3. **Casos Nasales Directos a la Raíz**: Las marcas de caso nasales (`-o` nominativo, `-om` acusativo, `-em` dativo, `-im` adverbial) y las envolturas verbales (`-ár`, `-ér`, `-ír`) se añaden directamente al extremo final de la raíz.
4. **Reconocimiento del Límite Argumental en $O(1)$**: Al no competir con sufijos derivativos deformantes en la cola del vocablo, el *parser* computacional y el receptor humano reconocen el límite argumental y el rol sintáctico de la entidad en complejidad $O(1)$ sin requerir *lookahead*.


---

### 1.7 Nota de Diseño �� Transiciones de Estado y Evaluación de `ad-`

Se consideró la posibilidad de marcar transiciones con el prefijo **`ad-`** (del latín *ad*, "hacia"), aplicable tanto a estados (`adabérto` = abriéndose) como a sustantivos. La idea refleja un patrón frecuente en muchas lenguas: marcar el estado intermedio entre dos polos, con dirección de tránsito ("en tránsito hacia").

Sin embargo, se optó por usar los verbos existentes (`askabrír`, `askserrár`, `askfokár`), que ofrecen ventajas superiores: conjugan, colapsan la pila preverbal, admiten negación clara, tienen gerundio y permiten derivación nominal. El prefijo **`ad-`** queda documentado como posibilidad para retomar en el futuro.


---

## 2. Morfología Nominal, Artículo Universal, Casos, Prosodia y Diacríticos

### 2.1 El Artículo Definido Universal (`la`)
Se canoniza el artículo **`la`** como el **determinante definido universal e invariable**:
* **Invariancia Total**: Se utiliza sin variación para singular, plural, masculino, femenino y neutro (`la usuário`, `la kárto`, `la dátoms`, `la servóro`).
* **Función Delimitadora**: Sirve como "campana de apertura" que marca el inicio del grupo nominal y rompe la monotonía vocálica respecto a la terminación neutra `-o`.

### 2.2 El Sistema de Casos Nasales y Casos Oblicuos Vectoriales
El rol sintáctico de cada entidad dentro de la oración se determina mediante marcadores nasales en posición final o mediante preposiciones vectoriales puras:

* **Nominativo / Sujeto (`-o` / `-a`)**: Forma base limpia del sustantivo (`káto`, `káta`, `sistémo`, `kóso`).
* **Acusativo / Objeto Directo (`-om` / `-am`)**: Adición de la nasal **`-m`** a la vocal temática activa (`kátom`, `kártom`, `sistémom`, `kósom`).
* **Dativo / Objeto Indirecto o Destino (`-em` / `-aem` o preposición `to`)**:
  * Forma sintética: sustitución por la vocal de dirección **`-e-`** + nasal **`-m`** (`sistémem`, `kátem`).
  * Forma analítica: preposición **`to`** + artículo **`la`** + sustantivo base (`to la servóro`, `to la usuário`).
* **Adverbio de Modo e Instrumental (`-im`)**: Derivación directa reemplazando la vocal temática por **`-im`** (`velocítim` = *velozmente*, `sistémim` = *sistemáticamente*, `módim` = *de cierto modo*).
* **Casos Oblicuos Vectoriales (Locativo, Instrumental, Ablativo)**:
  * **Locativo ("en / dentro de")**: Preposición **`en`** (`en la dómo` = en la casa) o sufijo opcional **`-in`** (`dómin`).
  * **Instrumental ("con / mediante")**: Preposición **`kun`** (`kun la mikroskópo` = con el microscopio) o desinencia adverbial **`-im`** (`mikroskópim`).
  * **Ablativo / Origen ("desde / de / por causa de")**: Preposición **`ex`** / **`de`** (`ex la urbo` = desde la ciudad) o sufijo opcional **`-ex`** (`úrbex`).

### 2.3 Posesivo Analítico Transparente (`de`)
El posesivo en Askáro utiliza la preposición **`de`** seguida del pronombre o sustantivo poseedor en forma base (observando la regla de mayúscula gramatical obligatoria en pronombres):
* `la kárto de Mo` = mi carta (Sujeto / Nominativo).
* `la kártom de Mo` = mi carta (Objeto Directo / Acusativo, con `-m` en el sustantivo poseído).
* `la kártom de To` = tu carta.
* `la kártom de Ko` = su carta (de él/ella/ello).
* `la kártom de Mos` = nuestra carta.
* `la kártom de Tos` = su carta (de ustedes).

### 2.4 Ortografía y Prosodia Determinista (Regla del Conteo de Vocales)
Para garantizar que la pronunciación y acentuación sean 100% predecibles:
1. **Palabras de 1 vocal (Monosilábicas)**: **NUNCA** llevan tilde gráfica (`Mo`, `To`, `Ko`, `ko`, `kom`, `kur`, `kan`, `pre`, `pro`, `vi`, `va`, `hic`, `is`, `al`, `mag`, `min`, `no`, `si`, `sik`, `nok`, `dok`, `so`, `re`, `to`, `de`, `en`, `kun`, `falls`, `On`, `rel`, `abs`, `pās`, `nul`, `un`, `du`, `tri`, `kin`, `seks`, `sep`, `ok`, `nov`, `ten`, `cen`, `mil`).
2. **Palabras de 2 o más vocales**: **SIEMPRE** llevan **exactamente 1 tilde gráfica** en la vocal que recibe el golpe de voz tónico (`dáto`, `sistémo`, `servóro`, `kártom`, `módim`, `sistémim`, `síi`, `alíter`, `étunc`, `áutunc`, `véltunc`, `áutsi`, `vélsi`, `koém`, `kúi`, `kómo`, `Úbi`, `Kíotem`, `Kvándo`, `Kvomódo`, `kóso`, `kúa`, `cénto`).

### 2.5 Economía Cuantitativa de Plurales (Estilo Mandarín)
El plural en **`-s`** es estricto y transparente:
* **Sin cuantificador explícito**: La marca de plural **`-s`** es **OBLIGATORIA** (`dátoms` = varios datos, `múlos` = mulas).
* **Con cuantificador explícito (`úno`, `dúo`, `múlto`, `ómno`, `kúa-cen`)**: La marca de plural en el sustantivo se **SUPRIME ESTRICTAMENTE** (`dúo dátom`, `ómno dátom`, `kúa-cen dómo`).

### 2.6 Normalización Fonotáctica e Inventario Completo de Fonemas (IAST y Pāṇini)
El sistema formaliza el espectro fonónico completo del Sánscrito (IAST / Devanāgarī) de 5 puntos de articulación (*vargas*), manteniendo un **subconjunto activo neolatino 1:1** en ASCII:

| Punto de Articulación | Sorda Simple | Sorda Aspirada | Sonora Simple | Sonora Aspirada | Nasal de Clase |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Velares (*Kanthya*)** | **`k`** | **`kh`** | **`g`** | **`gh`** | **`ṅ`** / **`ng`** |
| **Palatales (*Tālavya*)** | **`c`** (`/tʃ/`) | **`ch`** | **`j`** (`/��/`) | **`jh`** | **`ñ`** |
| **Retroflejas (*Mūrdhanya*)** | **`ṭ`** | **`ṭh`** | **`ḍ`** | **`ḍh`** | **`ṇ`** |
| **Dentales (*Dantya*)** | **`t`** | **`th`** | **`d`** | **`dh`** | **`n`** |
| **Labiales (*Oṣṭhya*)** | **`p`** | **`ph`** | **`b`** | **`bh`** | **`m`** |

* **Regla Fonotáctica Activa ASCII**:
  1. `/k/` $\rightarrow$ **`k`** fija siempre. Erradicación de `q` y `c` dura.
  2. `/s/` $\rightarrow$ **`s`** fija siempre.
  3. `/tʃ/` ("ch") $\rightarrow$ **`c`** fija siempre (siguiendo el estándar IAST).
  4. `/ɡ/` $\rightarrow$ **`g`** dura fija siempre.

### 2.7 Sistema de Capas Diacríticas e Isomorfismo ASCII (`^`)
Para lectura humana y marcado prosódico, el sistema ofrece dos notaciones 1:1 equivalentes:

| Categoría Funcional | Notación Unicode / Macrón | Notación ASCII Puro (`^`) | Metáfora Operativa | Ejemplos |
| :--- | :---: | :---: | :--- | :--- |
| **Pila Preverbal / Auxiliares** | **Macrón (`¯`)** | **Circunflejo (`^`)** | *Rueditas laterales* (TAM/Modal) | `pr��` / `prê`, `prō` / `prô`, `d��v` / `dêv`, `pās` / `pâs` |
| **Sustantivos / Declinación** | **Nasal (`-m`) / Anusvāra (`̇`)** | **Nasal (`-m`) / Punto (`.`)** | *Anclas argumentales* | `sistémom`, `kérvė` / `kérve.` |
| **Núcleo Verbal (Envoltura)** | **Tilde Aguda (`´`) en `-ár/-ér/-ír`** | **Tilde Aguda (`´`) en `-ár/-ér/-ír`** | *Pedal principal* (Colapso de pila) | `askvisár`, `asktenér`, `askaudír` |

---


### 2.8 Matriz de Prefijos Nominales Derivativos (Carga a la Izquierda)

Para proteger la integridad de la raíz nominal y reservar la cola de la palabra exclusivamente para las marcas de caso nasales (`-o`, `-om`, `-em`), Askáro erradica los sufijos derivativos romances tradicionales (`-dor`, `-ción`, `-dad`, `-miento`, `-ismo`, `-ista`) y los sustituye por la **Matriz de Prefijos Nominales Derivativos**:

| Prefijo | Función Semántica | Ejemplo Canónico | Significado Exacto en Askáro | Equivalente Romance Tradicional |
| :---: | :--- | :--- | :--- | :--- |
| **`ag-`** | Agente de la acción | **`ag-procéso`** / `ag-procésom` | *el que procesa / el procesador* | *-dor / -tor* |
| **`ak-`** | Acción o resultado | **`ak-procéso`** | *el proceso / la acción de procesar* | *-ción / -miento* |
| **`kual-`** | Cualidad o propiedad | **`kual-procéso`** | *la procesabilidad / cualidad del proceso* | *-dad / -bilidad* |
| **`inst-`** | Instrumento o herramienta | **`inst-procéso`** | *la herramienta o instrumento de proceso* | *-dor / -miento* |
| **`lok-`** | Lugar o espacio | **`lok-procéso`** | *el lugar o planta de procesamiento* | *-dero / -terio / -ría* |
| **`kol-`** | Colectivo o conjunto | **`kol-procéso`** | *el conjunto de procesos / lote* | *-do / -ría / -ción* |
| **`dim-`** | Diminutivo o escala menor | **`dim-procéso`** | *el subproceso / procesito* | *-ito / -ico* |
| **`aug-`** | Aumentativo o macro-escala| **`aug-procéso`** | *el gran proceso / macroproceso* | *-ón / -azo* |
| **`dok-`** | Doctrina, teoría o sistema| **`dok-procéso`** | *el procesismo / la teoría del proceso* | *-ismo* |
| **`pra-`** | Practicante o especialista| **`pra-procéso`** | *el procesista / especialista en procesos*| *-ista* |


## 3. Sistema Pronombral y Desambiguación de 3.ª Persona

### 3.1 Matriz Unificada de Pronombres Personales, Pro-Formas y Comodines

| Persona / Categoría | Sujeto / Nominativo (Mayúscula) | Acusativo (`-m`) | Dativo (`-em` / `to`) | Posesivo (`de`) |
| :--- | :--- | :--- | :--- | :--- |
| **1.ª Sing. (Yo)** | **`Mo`** | `Mom` | `Moem` / `to Mo` | `de Mo` |
| **1.ª Plural Inclusivo/Neutro** | **`Mos`** (Mo + To + otros) / **`Mas`** (fem) | `Mosom` / `Masam` | `Mosem` / `Masam` | `de Mos` / `de Mas` |
| **1.ª Plural Exclusivo** | **`Nos`** (Mo + otros, sin To) | `Nosom` | `Nosem` | `de Nos` |
| **2.ª Sing. (Tú)** | **`To`** | `Tom` | `Toem` / `to To` | `de To` |
| **2.ª Plural (Ustedes)** | **`Tos`** (neutro) / **`Tas`** (fem) | `Tosom` / `Tasam` | `Tosem` / `Tasem` | `de Tos` |
| **3.ª Sing. Humano Neutro** | **`Ko`** (*él / persona*) | `Kom` | `Koem` / `to Ko` | `de Ko` |
| **3.ª Sing. Humano Fem.** | **`Ka`** (*ella*) | `Kam` | `Kaem` / `to Ka` | `de Ka` |
| **3.ª Sing. Humano Masc.** | **`Kor`** (*él masculino*) | `Korm` | `Korem` / `to Kor` | `de Kor` |
| **3.ª Sing. Inanimado / Entidad**| **`Eo`** (*ello / objeto*) | `Eom` | `Eoem` / `to Eo` | `de Eo` |
| **3.ª Sing. Anafórico (Pro-forma)**| **`Ílo`** (*lo / ello mencionado*) | **`Ílom`** | `Íloem` / `to Ílo` | `de Ílo` |
| **Pronombre Logofórico** | **`Lo`** (*él mismo, hablante citado*) | `Lom` | `Loem` / `to Lo` | `de Lo` |
| **Pronombre Negativo** | **`No`** (*nadie / nada / ninguno*) | `Nom` | `Noem` / `to No` | `de No` |
| **Pronombre Indeterminado / Comodín**| **`On`** (*uno / alguien / se*) | `Onom` | `Onem` / `to On` | `de On` |
| **3.ª Plural Animat. Neutro** | **`Kos`** (*ellos / personas*) | `Kosom` | `Kosem` | `de Kos` |
| **3.ª Plural Animat. Femenino** | **`Kas`** (*ellas*) | `Kasam` | `Kasem` | `de Kas` |
| **3.ª Plural Inanimado** | **`Eos`** (*ellos / objetos*) | `Eosom` | `Eosem` | `de Eos` |

### 3.2 Formación de Reflexivos y Recíprocos Mediante `rel` + Acusativo
Askáro elimina la necesidad de pronombres reflexivos independientes acoplando la partícula de visión relativa **`rel`** con la forma acusativa del pronombre correspondiente:

* **`rel Mom`** $\rightarrow$ `Mo pr��s rel Mom asklavár.` *(Me lavo a mí mismo).*
* **`rel Tom`** $\rightarrow$ `To pr��s rel Tom asklavár.` *(Te lavas a ti mismo).*
* **`rel Kom`** $\rightarrow$ `Ko pr��s rel Kom askvisár.` *(Se ve a sí mismo).*
* **`rel Kam`** $\rightarrow$ `Ka pr��s rel Kam askvisár.` *(Se ve a sí misma).*
* **`rel Korm`** $\rightarrow$ `Kor pr��s rel Korm askvisár.` *(Se ve a sí mismo).*
* **`rel Eom`** $\rightarrow$ `Eo pr��s rel Eom askmodifikár.` *(Se modifica a sí mismo).*
* **`rel Mosom`** $\rightarrow$ `Mos pr��s rel Mosom askvisár.` *(Nos vemos a nosotros mismos).*
* **`rel Tosom`** $\rightarrow$ `Tos pr��s rel Tosom askvisár.` *(Se ven a ustedes mismos).*
* **`rel Kosom`** $\rightarrow$ `Kos pr��s rel Kosom askvisár.` *(Se ven el uno al otro / mutuamente).*

### 3.3 Desambiguación $O(1)$ sin Lookahead y Regla de Mayúscula Obligatoria
Para garantizar que un parser evalúe cada token en $O(1)$ sin requerir *lookahead* ($k=1$):
* **`To`** (mayúscula inicial): Pronombre de 2.ª persona sujeto (*Tú*).
* **`to`** (minúscula inicial): Preposición vectorial de dirección (*a / hacia*).
* **`Te`** (mayúscula inicial): Pronombre de 2.ª persona objeto/oblicuo (*A ti / Te*).
* **`te`** (minúscula inicial): Determinante demostrativo de distancia media (*ese / esa*).



### 3.5 Cuadrado de Aristóteles para Indefinidos (Composicionalidad Pura)

Askáro canoniza el Cuadrado de Aristóteles puro para cuantificadores e indefinidos mediante la combinación composicional sin alias del cuantificador (`ómno` / `úno`), el sustantivo de dominio (`persóno` / `kóso`) y el operador de negación exocéntrica (`no`):

#### 1. Dominio de Personas (Humano / Animado)

| Cantidad / Polaridad | Afirmativo | Negativo |
| :--- | :--- | :--- |
| **Universal (Todo/Todos)** | **`ómno persóno`** *(todas las personas / todos)* | **`no ómno persóno`** *(no todas las personas / no todos)* |
| **Particular (Alguno/Uno)** | **`úno persóno`** *(alguno / alguien / una persona)* | **`no úno persóno`** *(ninguna persona / nadie)* |

#### 2. Dominio de Cosas (Inanimado / Entidad)

| Cantidad / Polaridad | Afirmativo | Negativo |
| :--- | :--- | :--- |
| **Universal (Todo/Todos)** | **`ómno kóso`** *(todas las cosas / todo)* | **`no ómno kóso`** *(no todas las cosas)* |
| **Particular (Alguno/Uno)** | **`úno kóso`** *(alguna cosa / algo)* | **`no úno kóso`** *(ninguna cosa / nada)* |

#### ���� Ventaja Arquitectónica:
* **Cero Alias e Irregularidades:** Se erradica la necesidad de memorizar tablas arbitrarias e irregulares de pronombres indefinidos.
* **Composicionalidad 100% Transparente:** La cuantificación (universal `ómno` / particular `úno`), el dominio semántico (`persóno` / `kóso`) y la negación (`no`) interactúan algebraicamente sin excepciones sintácticas.

### 3.4 Variables Ordinales (Indización de Entidades y Personas)
Para evitar la ambigüedad en discursos con múltiples participantes u objetos del mismo tipo, Askáro formaliza un sistema de **variables ordinales** que permiten referenciar entidades y personas según su orden de aparición en el texto:

| Serie | Referente | Notación Documental | Forma Fusionada Natural | Significado Exacto |
| :--- | :--- | :---: | :---: | :--- |
| **Entidades (Inanimados / Cosas)** | Objeto 1 | **`E1`** | **`Eúnin`** | *La primera entidad / el primer objeto mencionado* |
| | Objeto 2 | **`E2`** | **`Edúin`** | *La segunda entidad / el segundo objeto* |
| | Objeto 3 | **`E3`** | **`Etríin`** | *La tercera entidad / el tercer objeto* |
| | Objeto 4 | **`E4`** | **`Ekúain`** | *La cuarta entidad / el cuarto objeto* |
| **Personas (Animados / Agentes)** | Persona 1 | **`P1`** | **`Púnin`** | *La primera persona / el primer sujeto* |
| | Persona 2 | **`P2`** | **`Pdúin`** | *La segunda persona / el segundo sujeto* |
| | Persona 3 | **`P3`** | **`Ptríin`** | *La tercera persona / el tercer sujeto* |
| | Persona 4 | **`P4`** | **`Pkúain`** | *La cuarta persona / el cuarto sujeto* |

#### Ejemplos de Desambiguación con Pronombres Especiales (V6.1)

1. **Plural Exclusivo (`Nos` vs. `Mos`):**
   * `Nos pr��s askpartír, to To pr��s askmanér.`  
     ���� *"Nosotros (sin ti) nos vamos, tú te quedas."*

2. **Pronombre Logofórico (`Lo` - Discurso Indirecto Desambiguado):**
   * `Ko1 pr�� askdicér ke Lo pro askfakár ílom.`  
     ���� *"Él1 dijo que él mismo (Ko1) lo haría."* (frente a `ke Ko2 pro askfakár` = que otro lo haría).

3. **Pronombre Negativo (`No`):**
   * `No pr��s askvenír.`  
     ���� *"Nadie viene."*
   * `Mo pr��s askvisár Nom.`  
     ���� *"No veo a nadie / a nada."*

4. **Variables Ordinales Fusionadas (`Eúnin`, `Edúin`, `Púnin`, `Pdúin`):**
   * `Púnin pr�� askenviár Eúnim to Pdúin.`  
     ���� *"La Persona 1 envió la Entidad 1 a la Persona 2."*
**Regla de Mayúscula Gramatical Obligatoria en Pronombres:**  
La mayúscula inicial en todos los pronombres personales, pro-formas y comodines (`Mo`, `To`, `Ko`, `Ka`, `Kor`, `Eo`, `Ílo`, `Lo`, `No`, `On`, `Mos`, `Nos`, `Mas`, `Tos`, `Tas`, `Kos`, `Kas`, `Eos`) es un **rasgo gramatical obligatorio** que distingue unívocamente la categoría pronombral de partículas, preposiciones o determinantes (evitando que `de To` se confunda con *"de hacia"*). Esta regla aplica de forma estricta en todas las posiciones sintácticas, **incluso en scriptio continua**.

---

## 4. Sistema Demostrativo, Deíctico y Adverbios de Modo

### 4.1 Determinantes y Pronombres Demostrativos

| Distancia / Esfera | Determinante | Pronombre Independiente | Adverbio de Modo ("Así") | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **Cerca del Emisor (1.ª p.)** | `hic` | `híco` / `híca` | `hícim` | *este / esta / de esta manera* |
| **Cerca del Receptor (2.ª p.)** | `is` / `te` | `íso` / `téo` / `téa` | `ísim` / `téim` | *ese / esa / de esa manera* |
| **Lejano a Ambos (3.ª p.)** | `al` / `lac` | `álo` / `láco` / `láca` | `álim` | *aquel / aquella / de aquella manera* |

---

## 5. Operadores Escalares, Comparativos y Léxico de Escala

### 5.1 Justificación del Par Escalar `mag` vs. `min`
Se canoniza **`mag`** (proveniente del latín *magis*) para "más" con el fin de **evitar la colisión homófona y sintáctica con el pronombre de 1.ª persona plural femenino `Mas`** (*nosotras*).
* `mag` = operador de mayor magnitud (*más*).
* `min` = operador de menor magnitud (*menos*).
* `Mas` = pronombre 1.ª p. plural femenino (*nosotras*).

---

## 6. Jerarquía Sintáctica, Pila Preverbal y Álgebra Condicional

### 6.1 Jerarquía de ��rdenes Sintácticos: Preferencia Canónica SOV vs. Libertad del Usuario
En Askáro, el orden sintáctico se rige por una jerarquía clara entre la norma canónica y la flexibilidad discursiva:
1. **Orden Preferente y Canónico: SOV (Sujeto - Objeto - Verbo)**:
   * **Fundamento Estadístico**: Tipológicamente y en universales lingüísticos (Greenberg), el orden SOV es el más estable y común en lenguajes con marcación explícita de caso.
   * **Encuadre Sintáctico y Colapso $O(1)$**: Permite acumular todos los argumentos antes de colapsar la pila preverbal mediante el verbo de envoltura (`ask-...-ár/-ér/-ír`).
   * **Uso en el Documento Maestro**: Por estas razones de optimización, los ejemplos oficiales de la especificación utilizan **principalmente el orden SOV**.
2. **Flexibilidad Total y Libertad del Usuario**:
   * Dado que cada rol sintáctico posee marcas unívocas (`-om` acusativo, `to` dativo, `la` artículo), **todos los demás órdenes (SVO, VSO, OVS, VOS, OSV) son 100% válidos y deterministas**.
   * **Libertad discursiva**: Los usuarios son completamente libres de utilizar el orden sintáctico en el que se sientan más cómodos en la conversación, lectura o redacción.

### 6.2 Estructura de 5 Capas de la Pila Preverbal y Exclusión Mutua
La Pila Preverbal se coloca entre el Sujeto y el Verbo. Sus 5 capas se evalúan en orden estricto de izquierda a derecha:

`[1. Tiempo (τ)] -> [2. Fase/Sincronía (φ)] -> [3. Epistémico (M_ep)] -> [4. Deóntico (M_de)] -> [5. Polaridad (P)]`

#### 6.2.1 Principio de Dispersión y Opcionalidad (0 a 5 Slots)
* **Opcionalidad Total (Pila Dispersa / *Sparse Stack*):** Ninguno de los slots de la pila preverbal es obligatorio. Una oración válida puede tener desde **0 auxiliares** (estado base indicativo/atemporal) hasta un máximo estricto de **5 auxiliares** (exactamente uno por cada capa).
* **Graduación de Complejidad (0��5 Slots):**
  * **0 Slots (Base atemporal / presente indicativo):** `Ko askfakár.` *(Él hace).*
  * **1 Slot (Tiempo simple):** `Ko pr�� askfakár.` *(Él hizo).*
  * **2 Slots (Tiempo + Modo):** `Ko pr�� dev askfakár.` *(Él debía hacer).*
  * **3 Slots (Tiempo + Epistémico + Deóntico):** `Ko pr�� prob dev askfakár.` *(Él probablemente debía hacer).*
  * **4 Slots (Tiempo + Fase + Epistémico + Deóntico):** `Ko pr�� dur prob dev askfakár.` *(Él probablemente debía continuar haciendo).*
  * **5 Slots (Pila Completa Saturada):** `Ko pr�� dur prob dev no askfakár.` *(Él probablemente debía continuar NO haciendo).*
* **Regla de Exclusión Mutua:** Dentro de cada capa individual solo puede seleccionarse **un único operador** a la vez.

#### 6.2.2 Naturaleza Semántica de la Polaridad `no` (Capa 5: Operador Lógico vs. Auxiliar)
La desinencia de polaridad **`no`** ubicada en la Capa 5 actúa formalmente como un **operador lógico de negación in-line ($
eg$)** acoplado a la pila:
1. **Alcance de Negación Verbal ($
eg$):** A diferencia de las partículas de tiempo o modo que añaden propiedades temporales o volitivas, **`no`** invierte la verdad del núcleo verbal directamente antes del colapso de envoltura (`ask-...-ár`).
2. **Evaluación de Alcance de Izquierda a Derecha:** Al situarse en la Capa 5 (la más cercana al verbo), la negación queda bajo el alcance (*scope*) de los modales y tiempos a su izquierda. Por ejemplo, `pr�� dev no askfakár` significa *"tenía la obligación de no hacer"*, mientras que `no pr�� dev askfakár` niega la obligación misma (*"no tenía la obligación de hacer"*).
3. **Diferenciación con `nok`:** Mientras que **`no`** es el operador lógico de negación preverbal ($
eg$), **`nok`** es la respuesta fáctica proposicional independiente ($0$ / *falso*).

`[1. Tiempo (τ)] -> [2. Fase/Sincronía (φ)] -> [3. Epistémico (M_ep)] -> [4. Deóntico (M_de)] -> [5. Polaridad (P)]`

#### Inventario Completo y Exhaustivo de Auxiliares Canonizados:

| Capa | Código Macrón | Notación ASCII (`^`) | Categoría Gramatical | Significado Exacto |
| :---: | :---: | :---: | :--- | :--- |
| **1. Tiempo (τ)** | **`pr��`** | `prê` | Pasado Absoluto | *Ocurrió / Pasó* |
| | **`pr��s`** | `prês` | Presente Continuo / Actual | *Ocurre ahora / Está pasando* |
| | **`prō`** | `prô` | Futuro Absoluto | *Ocurrirá / Pasará* |
| **2. Fase/Sincronía (φ)**| **`dūr`** | `dûr` | Durativo / Progresivo | *Continúa ocurriendo / Sigue* |
| | **`sinc`** | `sinc` | Sincrónico / Tiempo Real | *En tiempo real / alineado* |
| | **`desinc`**| `desinc`| Asincrónico | *Ejecución en diferido* |
| | **`pās`** | `pâs` | Pasiva Analítica | *Es / fue / será [hecho]* |
| **3. Epistémico (M_ep)**| **`c��r`** | `cêr` | Certeza Fáctica (100%) | *Ciertamente / Sin duda* |
| | **`prōb`** | `prôb` | Probabilidad Alta (~80%) | *Probablemente* |
| | **`pōs`** | `pôs` | Posibilidad (~50%) | *Es posible que / Quizás* |
| | **`hīp`** | `hîp` | Hipotético / Irreal | *En escenario hipotético / Habría* |
| | **`asūm`** | `asûm` | Asunción / Inferencia | *Se asume / Aparentemente* |
| | **`mne`** | `mne` | Registro / Memoria | *Según constancia en registro* |
| **4. Deóntico (M_de)** | **`pōt`** | `pôt` | Capacidad / Facultad | *Puede / Tiene la capacidad de* |
| | **`d��v`** | `dêv` | Obligación / Deber | *Debe / Tiene la obligación de* |
| | **`vōl`** | `vôl` | Volición / Deseo | *Quiere / Desea ejecutar* |
| | **`mând`** | `mând` | Mandato / Imperativo | *Ordena / Instruye ejecutar (¡Hazlo!)* |
| **5. Polaridad (P)** | **`n��`** | `nê` | Inversión Lógica del Predicado ($\neg P$) | *Operador de polaridad del predicado (inversión de verdad)* |


### 6.3 La Tetralogía de la Negación y Distinción Aritmética/Lógica

Para evitar cualquier solapamiento en lógica de predicados y parsing determinista, Askáro distingue cuatro niveles de negación análogos a la distinción en aritmética entre la **polaridad del número** (signo `-`) y la **operación de sustracción**:

1. **`n��`** / **`nê` (Inversión Lógica de Polaridad del Predicado $\neg P$):**  
   Ubicado exclusivamente en la **Capa 5 de la Pila Preverbal**. Es el operador unario de inversión lógica sobre el resultado del predicado verbal (análogo al signo de polaridad negativa en un valor verdadero/falso). Invierte la ejecución de la acción ($
eg P(x)$).
   * *Ejemplo:* `Ko pr�� d��v n�� askfakár.` *(Tiene la obligación de invertir el resultado de la acción: NO-hacer).*

2. **`no` (Operador Relacional y de Alcance Nominal):**  
   Utilizado antes de cuantificadores, adjetivos o grupos nominales para indicar el complemento o conjunto vacío parcial (análogo a la relación de resta/complemento).
   * *Ejemplo:* `no úno persóno` *(complemento de una persona: ninguna persona)*, `no múlto` *(no mucho)*.

3. **`No` (Pronombre Negativo Sustantivo - *"Ninguno / Nadie"*):**  
   Surge de la matriz pronombral por analogía asociativa (*Mos* -> *Mo* :: *Nos* -> *No*). Lleva mayúscula gramatical obligatoria.
   * *Ejemplo:* `No pr��s askvenír.` *(Nadie / Ninguno viene).*

4. **`nok` / `sik` / `dok` (Tokens Fácticos Independientes - Valores de Verdad $0$, $1$ y $1_{adv}$):**  
   Tokens de respuesta fáctica proposicional completa fuera de la pila.
   * *Ejemplo:* `�� ¿Ko pr�� askvenír? �� Nok.` *(�� ¿Vino? �� Falso/0).*


### 6.4 Operador de Envoltura Verbal `ask-...-ár/-ér/-ír`
* Prefijo invariable **`ask-`** (Apertura).
* Infijos operativos opcionales (`-pas-` pasiva sintética, `-n-` nulidad, `-de-` reverso, `-fal-` fallo, `-kos-` acoplamiento, `-dos-` disyunción, `-re-` repetición).
* Sufijos eufónicos continentales **`-ár`**, **`-ér`**, **`-ír`** (de las 3 conjugaciones latinas *-āre*, *-��re/-ěre*, *-īre*).
* Tilde gráfica obligatoria como gatillo de colapso de la pila verbal (*stack collapse*).

### 6.5 Álgebra Condicional, Anidamientos Excluyentes y Conectores de Rama (`étunc`, `áutunc`, `véltunc`, `áutsi`, `vélsi`, `secus`)
* **`si`**: Condicional básico (*Si...*).
* **`síi`**: Bicondicional (*Si y solo si...*).
* **`tunc`**: Consecuencia (*entonces...*).
* **`étunc`**: Y entonces / a continuación (secuencia lineal).
* **`áutunc`**: O entonces / o bien en tal caso (consecuencia alternativa excluyente).
* **`véltunc`**: O incluso entonces (consecuencia alternativa inclusiva).
* **`áutsi`**: O si / en cambio si (`else if` excluyente).
* **`vélsi`**: O incluso si (`inclusive else if`).
* **`secus`**: De lo contrario / si no (*else* final).
* **`alíter`**: De otra manera / por otro método (procedimiento alternativo).
* **`falls`**: Condicional de falla o excepción (*en caso eventual de que...*).

### 6.6 Sistema Unificado de Subordinación y Cláusulas Complejas

#### Tabla Resumen Canonizada de Relativos (Cláusulas Adjetivas):

| Función Sintáctica | Forma Canónica | Vocales | Tilde (Prosodia) | Ejemplo Canónico en Askáro |
| :--- | :---: | :---: | :---: | :--- |
| **Sujeto** | **`ko`** | 1 | **No** | `La usuário ko pr��s askadministrár...` |
| **Objeto Directo** | **`kom`** | 1 | **No** | `La kárto kom To pr�� askenviár...` |
| **Dativo** | **`koém`** | 2 (`o`, `e`) | **Sí (aguda)** | `La usuário koém Mo pr�� askenviár...` |
| **Posesivo** | **`kúi`** | 2 (`u`, `i`) | **Sí (llana)** | `La sistémo kúi servóro pr��s askoperár...` |
| **Locativo** | **`kur`** | 1 | **No** | `La dómo kur Ko pr��s askvivír...` |
| **Temporal** | **`kan`** | 1 | **No** | `La diáno kan Ko pr�� askarivár...` |
| **Modal** | **`kómo`** | 2 (`o`, `o`) | **Sí (llana)** | `La módo kómo Ko pr�� askfakár...` |

#### Tabla de Cláusulas Subordinadas Sustantivas (Completivas e Interrogativas Indirectas):

| Tipo de Cláusula | Introductor | Función Sintáctica | Ejemplo Canónico en Askáro |
| :--- | :--- | :--- | :--- |
| **Completiva Declarativa** | **`ke`** | Sustituye argumento verbal | `Mo pr��s asksabér ke la servóro pr��s askoperár.` |
| **Interrogativa Indirecta Sí/No** | **`an`** | Sustituye argumento verbal | `Mo pr��s askpreguntár an la servóro pr��s askoperár.` |
| **Interrogativa Indirecta Parcial**| **`Kv-`** (`kvo`, `kve`...) | Sustituye argumento verbal | `Mo no pr��s asksabér kvo la usuário pr��s askfakár.` |

### 6.7 Tríada de Perspectiva (`abs`, `rel`, `su`) y Partícula Evidencial Directa (`dir`)

Askáro resuelve de forma determinista la perspectiva pragmática, el foco sobre el sujeto y la fuente evidencial de la información mediante la **Tríada de Perspectiva** y el operador de atestiguamiento directo **`dir`**:

#### 1. Tríada Canónica de Perspectiva (`abs`, `rel`, `su`)

* **`abs` (Visión Absoluta):** Marco objetivo, ontológico o universal (*en su totalidad / objetivamente*).
* **`rel` (Visión Relativa):** Marco contextual o referencial (*en relación con / para tal entidad*).
* **`su` (Visión Subjetiva / Foco en Sujeto):** Marco vivencial, interno o de exclusión de foco sobre el sujeto (*solo él / desde el enfoque propio del sujeto*).

#### 2. Operador Evidencial de Atestiguamiento Directo (`dir`)

* **`dir` (Atestiguamiento Directo):** Marca que la acción expresada por el enunciado fue **observada o presenciada directamente en persona por el hablante** (*lo vi directamente / consta de primera mano*).

#### Tabla Resumen de Perspectiva y Evidencialidad:

| Estructura | Enfoque Semántico | Ejemplo Canónico | Significado Exacto |
| :--- | :--- | :--- | :--- |
| **Base Neutra** | Enunciado neutro estándar | `Ko pr��s askfakár.` | *Él hace.* |
| **Foco Sujetivo (`su`)** | Foco exclusivo en el sujeto | `Su Ko pr��s askfakár.` | *Solo él hace / Enfoque propio de él.* |
| **Atestiguamiento (`dir`)**| Evidencia visual/directa | `Ko dir pr��s askfakár.` | *Él hace (lo vi directamente).* |
| **Foco + Atestiguamiento** | Sujeto exclusivo + Evidencia directa | `Sū Ko dīr pr��s askfakár.` | *Solo él hace, y lo vi directamente.* |
| **Visión Absoluta (`abs`)**| Perspectiva universal | `abs Mo pr��s askvisár la kósom.` | *Vi la cosa en su totalidad.* |
| **Visión Relativa (`rel`)**| Perspectiva referencial | `rel Mo, la kóso pr��s askesér díficil.` | *Para mí, la cosa es difícil.* |


### 6.8 Taxonomía Formal de Pro-Formas Gramaticales vs. Comodines Léxicos

| Categoría | Forma | Tipo Gramatical | Función Sintáctica y Pragmática | Ejemplo Canónico en Askáro |
| :--- | :--- | :--- | :--- | :--- |
| **Anáfora** | **`Ílo` / `Eo`** | Pro-nombre | Sustituye a una entidad/sustantivo antecedente conocido | `Mo pr��s askvisár ílom.` *(Lo vi).* |
| **Anáfora** | **`fak`** | Pro-verbo | Sustituye a una acción/verbo antecedente conocido | `Ko prō askfakár fak.` *(Él lo hará / ejecutará esa acción).* |
| **Anáfora** | **`On`** | Pro-agente | Sustituye a un agente humano genérico o indeterminado | `On pr��s askdicér ke...` *(Se dice / Uno dice que...).* |
| **Comodín** | **`kóso`** | Comodín nominal | Llena un vacío léxico cuando se ignora o no se nombra el objeto | `To to Mo la kósom pr��s askdar.` *(Dame esa cosa).* |
| **Comodín** | **`askkosár`** | Pro-verbo genérico | Llena un vacío de acción sobre un objeto sin nombrar el verbo técnico | `Mo eom pr�� askkosár.` *(Lo cosié / procesé la cosa).* |
| **Comodín** | **`askobrár`** | Verbo de intervención | Llena un vacío de labor o trabajo físico sobre una estructura | `Mos pr�� askobrár en la dómo.` *(Estuvimos obrando en la casa).* |

---

## 7. Sistema Numérico Base 10, Multiplicadores Posicionales y Sufijos Funcionales

### 7.1 Dígitos Primarios (0��9) y Regla del Conteo de Vocales
El sistema numérico de Askáro opera en **Base 10 pura** con concatenación lineal posicional de izquierda a derecha. Los diez dígitos fundamentales se construyen sobre raíces monosilábicas (excepto `kúa`, que posee 2 vocales y lleva tilde en la `ú` para cumplir estrictamente la Regla del Conteo de Vocales):

| Cifra | Dígito Canónico | Vocales | Tilde (Prosodia) | Significado |
| :---: | :---: | :---: | :---: | :--- |
| **0** | **`nul`** | 1 | No | *cero* |
| **1** | **`un`** | 1 | No | *uno* |
| **2** | **`du`** | 1 | No | *dos* |
| **3** | **`tri`** | 1 | No | *tres* |
| **4** | **`kúa`** | 2 (`u`, `a`) | **Sí (`ú`)** | *cuatro* |
| **5** | **`kin`** | 1 | No | *cinco* |
| **6** | **`seks`** | 1 | No | *seis* |
| **7** | **`sep`** | 1 | No | *siete* |
| **8** | **`ok`** | 1 | No | *ocho* |
| **9** | **`nov`** | 1 | No | *nueve* |

### 7.2 Multiplicadores Posicionales y Sustantivos Base (`cénto`)
Las órdenes de magnitud se construyen mediante multiplicadores posicionales transparentes. El multiplicador **`cen`** ($	imes 100$) se explica y fundamenta dinámicamente sobre el sustantivo neutro base **`cénto`** (*el ciento / la centena*):

* **`ten`** (Decena / $10^1$): Derivado de `téno` / `decéno`.
* **`cen`** (Centena / $10^2$): Derivado de **`cénto`** (*el ciento / la centena*).
* **`mil`** (Millar / $10^3$): Derivado de `mílo`.
* **`mílion`** (Millón / $10^6$): Derivado de `míliono`.
* **`míliard`** (Mil millones / $10^9$): Derivado de `míliardo`.

### 7.3 Reglas de Composición Lineal (Decenas, Centenas y Millares)
Los números compuestos se forman multiplicando la cifra por la base posicional y sumando las unidades sucesivas en orden directo:

#### A. Decenas (10��99):
* **10** ($1 	imes 10$) $
ightarrow$ **`un-ten`** (o **`ten`**)
* **11** ($10 + 1$) $
ightarrow$ **`un-ten-un`**
* **12** ($10 + 2$) $
ightarrow$ **`un-ten-du`**
* **20** ($2 	imes 10$) $
ightarrow$ **`du-ten`**
* **23** ($2 	imes 10 + 3$) $
ightarrow$ **`du-ten-tri`**
* **40** ($4 	imes 10$) $
ightarrow$ **`kúa-ten`**
* **45** ($4 	imes 10 + 5$) $
ightarrow$ **`kúa-ten-kin`**
* **99** ($9 	imes 10 + 9$) $
ightarrow$ **`nov-ten-nov`**

#### B. Centenas (100��999):
* **100** ($1 	imes 100$) $
ightarrow$ **`un-cen`** (sustantivo: **`la cénto`**)
* **200** ($2 	imes 100$) $
ightarrow$ **`du-cen`** (sustantivo: **`dúo céntos`**)
* **347** ($3 	imes 100 + 40 + 7$) $
ightarrow$ **`tri-cen-kúa-ten-sep`**
* **400** ($4 	imes 100$) $
ightarrow$ **`kúa-cen`**
* **444** ($4 	imes 100 + 40 + 4$) $
ightarrow$ **`kúa-cen-kúa-ten-kúa`**
* **512** ($5 	imes 100 + 10 + 2$) $
ightarrow$ **`kin-cen-un-ten-du`**

#### C. Millares y Grandes Cifras (1000+):
* **1000** ($1 	imes 1000$) $
ightarrow$ **`un-mil`**
* **1200** ($1000 + 200$) $
ightarrow$ **`un-mil-du-cen`**
* **2026** ($2 	imes 1000 + 20 + 6$) $
ightarrow$ **`du-mil-du-ten-seks`**

### 7.4 Trinidad de Sufijos Numéricos Funcionales
Los números generan derivados gramaticales unívocos según su rol en el enunciado:

| Categoría Funcional | Sufijo | Ejemplo | Significado Exacto |
| :--- | :---: | :--- | :--- |
| **Cardinal / Cantidad Pura** | **`-o`** | `ún-o`, `dú-o`, `trí-o`, `kúa-o`, `kín-o` | *uno, dos, tres, cuatro, cinco* |
| **Ordinal / Posición** | **`-in`** | `unin`, `duin`, `triin`, `kúain` | *primero, segundo, tercero, cuarto* |
| **Partitivo / Fracción** | **`-fra`** | `dufra`, `trifra`, `kúafra`, `du tri-fra` | *mitad, tercio, cuarto, dos tercios* |
| **Multiplicativo** | **`-ple`** | `duple`, `triple`, `kúaple` | *doble, triple, cuádruple* |
| **Frecuencia / Repetición** | **`-vece`** | `un-vece`, `du-vece`, `tri-vece` | *una vez, dos veces, tres veces* |

### 7.5 Economía Cuantitativa de Plurales (Estilo Mandarín)
Cuando un sustantivo está precedido por un número o cuantificador explícito, la marca de plural **`-s`** en el sustantivo se **suprime strictly** para evitar redundancia:
* `dúo dátom` *(dos datos �� no dúo dátoms)*
* `kúa-cen dómo` *(cuatrocientas casas �� no kúa-cen dómos)*
* `omno sistémo` *(todos los sistemas)*

---

## 8. Tablas de Preposiciones, Conjunciones y Adverbios Canonizados

### 8.1 Preposiciones Vectoriales
* **`en`**: En / dentro de / sobre (Locativo).
* **`to`**: A / hacia / para (Dirección / Dativo analítico).
* **`de`**: De / desde / posesivo (Origen / Posesión).
* **`ex`**: Desde / fuera de / por causa de (Ablativo).
* **`kun`**: Con / en compañía de / mediante (Instrumental).
* **`sin`**: Sin / en ausencia de.
* **`per`**: Por / a través de / mediante.
* **`pro`**: Para / en favor de / con propósito de.
* **`sub`**: Bajo / debajo de.
* **`sup`**: Sobre / encima de.
* **`ante`**: Antes de / delante de.
* **`post`**: Después de / detrás de.
* **`inter`**: Entre (dos o más entidades).
* **`trans`**: A través de / más allá de.

### 8.2 Conjunciones y Conectores Lógicos
* **`et`**: Y (Conjunción copulativa simple).
* **`ets`**: Y además / asimismo / simultáneamente (Conjunción aditiva de co-ocurrencia).
* **`vel`**: O (Disyunción inclusiva: A o B, o ambos).
* **`aut`**: O (Disyunción exclusiva: A o B, pero no ambos).
* **`re`**: Porque / dado que (Causal).
* **`so`**: Así que / por lo tanto (Consecutivo).
* **`si`**: Si (Condicional).
* **`síi`**: Si y solo si (Bicondicional).
* **`tunc`**: Entonces (Consecuencia de condicional).
* **`étunc`**: Y entonces / a continuación (secuencia lineal).
* **`áutunc`**: O entonces / o bien en tal caso (consecuencia alternativa excluyente).
* **`véltunc`**: O incluso entonces (consecuencia alternativa inclusiva).
* **`áutsi`**: O si / en cambio si (`else if` excluyente).
* **`vélsi`**: O incluso si (`inclusive else if`).
* **`secus`**: De lo contrario / si no (*else* final).
* **`alíter`**: De otra manera / por otro método (Procedimiento alternativo).
* **`quam`**: Que / en comparación con (Comparativo).

### 8.3 Adverbios Básicos, Partículas Pragmáticas y Confirmación Fáctica
* **`An`**: Partícula interrogativa polar estructuradora (ubicada al inicio de la cláusula para señalar el marco interrogativo ¿...? en $O(1)$).
* **`Ah`**: Partícula exclamativa/emotiva espontánea (expresa énfasis, sorpresa o asombro: *¡Ah! / ¡Efectivamente!*).
* **`Ah! Sic!`**: *¡Ah, sí! / ¡Efectivamente! / ¡Confirmado!*
* **`Ah! Noc!`**: *¡Ah, no! / ¡De ninguna manera! / ¡Falso!*
* **`Ah! Dok!`**: *¡Ah, al contrario, sí! / ¡Pues claro que sí!*
* **`ya`**: Ya / actualmente / inmediatamente (Marcador temporal de aspecto realizado/presente).
* **`sik`**: Sí / confirmed / así es (Afirmación fáctica 1).
* **`nok`**: No / falso / no es así (Negación fáctica 0).
* **`dok`**: Al contrario, sí (Afirmación adversativa / *doch*).
* **`hícim`**: De este modo / así (Deíctico 1.ª p.).
* **`ísim`**: De ese modo / así (Deíctico 2.ª p.).
* **`álim`**: De aquel modo (Deíctico 3.ª p.).
* **`módim`**: De cierto modo / de alguna manera.
* **`sistémim`**: Sistemáticamente (de `sistémo` + `-im`).
* **`mag`**: Más / mayor grado.
* **`min`**: Menos / menor grado.

### 8.4 Matriz Unificada de Interrogativos Vectoriales (`Kio-`)

| Dimensión Sintáctica | Raíz Dimensional | Forma Vectorial (Analítica) | Forma Atómica (Comprimida) | Significado Exacto |
| :--- | :--- | :--- | :--- | :--- |
| **Entidad Inanimada** | `-o` / `-om` | **`Kio-o`** / **`Kio-om`** | **`Kíoo`** / **`Kíom`** $\rightarrow$ **`Kvo`** / **`Kvom`** | *¿Qué objeto / Qué cosa?* |
| **Agente Humano** | `-or` / `persono` | **`Kio-or`** | **`Kíor`** $\rightarrow$ **`Kve`** / **`Kvem`** | *¿Qué persona / Quién?* |
| **Dimensión Temporal**| **`tem`** (de `témpo`)| **`Kio-tem`** | **`Kíotem`** $\rightarrow$ **`Kvándo`** | *¿En qué tiempo / Cuándo?* |
| **Dimensión Espacial**| `ino` / `zono` | **`Kio-ino`** | **`Kíoino`** $\rightarrow$ **`Úbi`** | *¿En qué lugar / Dónde?* |
| **Causalidad Lógica** | `re` | **`Kio-re`** | **`Kíore`** $\rightarrow$ **`Kvar`** | *¿Por qué causa / Por qué?* |
| **Modo / Ejecución** | `mod` / `fak` | **`Kio-mod`** | **`Kíomod`** $\rightarrow$ **`Kvomódo`** | *¿De qué modo / Cómo?* |

---

## 9. Compilación del Benchmark de Casos de Prueba (V6.0)

### ���� Caso 01: Estado Base Neutro y Secuencia Narrativa con `étunc`
> *"El usuario presiona el botón, y entonces la máquina arranca."*
* **Traducción (SOV Canónico)**: `La usuário la botónom pr�� askpresiónár, étunc la mákino pr�� askarrancár.`
* **Análisis**: Sujeto + Acusativo (`botónom`) + Verbo + Conector secuencial (`étunc`) + Cláusula consecuente.

### ���� Caso 02: Condicional Complejo con `áutsi` (`else if`), `áutunc` y `secus` (`else`)
> *"Si la máquina procesa el dato, envía la respuesta; o si el servidor de respaldo procesa, envía hacia allí; de lo contrario, notifica el error."*
* **Traducción**: `si la mákino la dátom askprocesár tunc la responsóm askenviár; áutsi la backup-servóro pr��s askprocesár áutunc to híco askenviár; secus la errórom asknotifikár.`
* **Análisis**: Condicional `si` + Rama alternativa excluyente `áutsi` con consecuencia `áutunc` + Rama por defecto `secus` (`else`).

### ���� Caso 03: Expresión de Grandes Cantidades y Economía de Plurales
> *"Cuatrocientas cuarenta y cuatro personas procesaron mil doscientos datos en dos veces."*
* **Traducción**: `Kúa-cen-kúa-ten-kúa persono un-mil-du-cen dátom du-vece pr�� askprocesár.`
* **Análisis**: Sujeto numeral (`Kúa-cen-kúa-ten-kúa persono` sin `-s` en `persono`) + Objeto numeral (`un-mil-du-cen dátom` sin `-s` en `dátom`) + Adverbio distributivo (`du-vece`) + Verbo pasado.


### ���� Caso 04: Demostración de Perspectiva Sujetiva (`su`) y Evidencia Directa (`dir`)

Demostración de la graduación de foco y evidencia empírica en Askáro V6.0:

1. **Afirmación Base Neutra:**  
   ���� **`Ko pr��s askfakár.`**  
   *(Él hace).*

2. **Aislamiento de Foco Sujetivo (`su`):**  
   ���� **`Su Ko pr��s askfakár.`**  
   *(Solo él hace / Enfoque exclusivo en el sujeto).*

3. **Inclusión de Evidencia Directa Presencial (`dir`):**  
   ���� **`Ko dir pr��s askfakár.`**  
   *(Él hace [lo vi directamente]).*

4. **Síntesis Completa (Foco + Evidencia Directa):**  
   ���� **`Sū Ko dīr pr��s askfakár.`**  
   *(Solo él hace, y lo vi directamente).*



### 6.8 Isomorfismo Completo: Sufijos Romance vs. Prefijos Composicionales (Módulo 09)

Para garantizar la interoperabilidad entre el estilo fluido/humano (sufijación romance) y el estilo puramente analítico/agente de IA (prefijación composicional), Askáro V7.1 establece una equivalencia 1:1 estricta:

| Sufijo Romance | Prefijo Composicional | Ejemplo Sufijado | Ejemplo Prefijado | Significado Operativo |
| :---: | :---: | :--- | :--- | :--- |
| **`-ór`** | **`ag-`** | `procesór` | `agprocéso` | Agente / El que procesa |
| **`-tório`** | **`inst-`** | `procesatório` | `instprocéso` | Instrumento / Herramienta |
| **`-íto`** | **`mikro-`** | `kartíto` | `mikrokárto` | Diminutivo / Escala menor |
| **`-óto`** | **`makro-`** | `kartóto` | `makrokárto` | Aumentativo / Escala mayor |
| **`-áro`** | **`kon-`** | `kartáro` | `konkárto` | Colectivo / Conjunto |
| **`-erío` / `-íno`** | **`lok-`** | `karterío` | `lokkárto` | Ubicación / Lugar de la entidad |
| **`-ísmo`** | **`dok-`** | `sistemísmo` | `doksistémo` | Doctrina / Marco teórico |
| **`-ísto`** | **`pra-`** | `sistemísto` | `prasistémo` | Practicante / Agente ejecutor |
| **`-itá`** | **`kwal-`** | `bonitá` | `kwalbóno` | Cualidad abstracta |


### 2.9 Gerundios Morfológicos con Macrón (`-ândo`, `-êndo`, `-îndo`)
El gerundio se construye agregando la desinencia con macrón a la raíz según la conjugación verbal:
* **1.ª Conjugación (`-ár`)**: **`-ândo`** (ASCII: `-ando`) $\rightarrow$ `kaminândo`, `trabahândo`.
* **2.ª Conjugación (`-ér`)**: **`-êndo`** (ASCII: `-endo`) $\rightarrow$ `komêndo`, `procesêndo`.
* **3.ª Conjugación (`-ír`)**: **`-îndo`** (ASCII: `-indo`) $\rightarrow$ `vivîndo`, `escribîndo`.

### 2.10 Verbo de Aspecto Continuo `askandár` (Andar / Caminar / Auxiliar)
Se canoniza el verbo **`askandár`** (Stem: `and-`, Prosodia: 3 sílabas, tilde en `á`) con doble función sintáctica:
1. **Uso como Verbo Pleno (Movimiento)**: `Mo askandár.` $\rightarrow$ *Ando / camino.*
2. **Uso como Auxiliar Progresivo (Iberorromance `andar + gerundio`)**: `Mo askandár trabahândo.` $\rightarrow$ *Ando trabajando.*

#### Interacción con la Pila Preverbal:
* `Mo pr�� askandár trabahândo.` $\rightarrow$ *Anduve trabajando.*
* `Mo prō askandár trabahândo.` $\rightarrow$ *Andaré trabajando.*
* `Mo d��v askandár trabahândo.` $\rightarrow$ *Debo andar trabajando.*
* `Mo dūr askandár trabahândo.` $\rightarrow$ *Sigo andando trabajando.*


## 10. Pragmática de Cortesía y Registros de Solicitud

Askáro formaliza un modelo multicapa de cortesía pragmática que permite modular el grado de deferencia y formalidad en peticiones, mandatos y solicitudes sin romper el determinismo sintáctico:

| Nivel / Registro | Formulario de Cortesía | Tipo / Origen | Ejemplo Canónico en Askáro | Traducción Exacta |
| :---: | :--- | :--- | :--- | :--- |
| **Informal / Rápido** | **`pró`** | Préstamo latino directo | `Dá Mo ákvôm, pró.` / `Pró, dá Mo ákvôm.` | *Dame agua, por favor.* / *Por favor, dame agua.* |
| **Estándar** | **`pro favóro`** | Romance | `Dá Mo ákvôm, pro favóro.` | *Dame agua, por favor.* |
| **Formal** | **`si To pláse`** | Expresión condicional | `Si To pláse, dá Mo ákvôm.` | *Si te place, dame agua.* |
| **Cortés / Modal** | **`¿Pōt To...?`** | Interrogativo modal | `¿Pōt To dár Mo ákvôm?` | *¿Podrías / puedes darme agua?* |
| **Muy Formal / Ruego**| **`Mo rogár To`** | Perífrasis de ruego | `Mo rogár To, dá Mo ákvôm.` | *Te ruego, dame agua.* |

### Principios de la Pragmática en Askáro:
1. **Riqueza de Registros**: Coexisten 5 estrategias pragmáticas desde el diálogo cotidiano/rápido (`pró`) hasta el protocolo formal (`Mo rogár To`).
2. **Preservación del Parsing**: Ninguna de las partículas de cortesía interfiere con la evaluación en $O(1)$ de los argumentos nominales ni con el colapso de la pila preverbal.
3. **Flexibilidad Posicional de `pró`**: La partícula breve `pró` puede ubicarse como prefijo adverbial inicial (`Pró, dá Mo...`) o como sufijo exclamativo de cierre (`...dá Mo ákvôm, pró.`), actuando como un modulador de tono directo.

---

## 11. Módulo de Pragmática, Fórmulas de Cortesía y Saludos (`Pragmá-Sistémo`)

| Español | Askáro | Prosodia / Estructura | Regla / Etimología |
| :--- | :---: | :--- | :--- |
| **Hola** | **`Saló`** | Aguda (`sa-ló`) | Latín *salus*. |
| **Adiós** | **`Cáo`** | Llana (`cá-o`) | Italiano *ciao* (`c` = `/tʃ/`). |
| **Por favor** | **`pro`** / **`pro favóro`** | Monosílabo / Frase | Expresión de cortesía. |
| **Gracias** | **`Grátis`** | Llana (`grá-tis`) | Latín *gratias*. |
| **De nada** | **`De nílo`** | Frase (`de ní-lo`) | Lit. "De nada / De cero". |
| **Perdón** | **`Párdon`** | Llana (`pár-don`) | Latín *pardonare*. |
| **Sí** | **`Sik`** | Monosílabo fáctico | Confirmación (1). |
| **No** | **`Nok`** | Monosílabo fáctico | Negación (0). |

---

## 12. Módulo Cromático y Álgebra de Mezclas (`Krómo-Sistémo`)

### 12.1 Colores Primarios, Secundarios y Extremos
* **Primarios:** **`rójo`** (Rojo), **`bláo`** (Azul), **`flávo`** (Amarillo).
* **Extremos:** **`álbo`** (Blanco), **`négro`** (Negro).
* **Secundarios / Derivados:** **`vírdo`** (Verde = *blao-flavo*), **`naránjo`** (Naranja = *rojo-flavo*), **`purpúro`** (Púrpura = *rojo-blao*), **`pínko`** (Rosa), **`gríso`** (Gris), **`káfe`** (Marrón/Café).

---

## 13. Módulo de Parentesco, Dimensión Afectiva y Fisiología Neonatal (`Sóm-Sistémo`)

### 13.1 Árbol de Parentesco y Registros
* **Padre / Madre / Hijo / Hija / Hermano / Hermana:** **`pátro`**, **`mátra`**, **`fílo`**, **`fíla`**, **`frátro`**, **`soróro`**.
* **Hipocorísticos e Infantil:** **`pápo`** (Papá), **`mámo`** (Mamá), **`náno`** / **`nána`** (Nene/Nena).

### 13.2 Fisiología Vocálica Neonatal (Capa 0) y Par Transparente
* **Reflejos Vocálicos Primarios:** `á` (Incomodidad), `é` (Hambre), `ó` (Sueño), `ou` (Gases), `í` (Dolor), `ú` (Frío/Inseguridad).
* **Par Canónico Padre-Bebé:**
  * **`au`** $\rightarrow$ **`áuxo`** / **`auxílio`** (Llamado de socorro).
  * **`ea`** $\rightarrow$ **`eaflíko`** (Malestar / Aflicción).
* **Necesidades Básicas:** **`áfamo`** (Hambre / Apetito fisiológico).

---

## 14. Módulo de Tiempo, Calendario e Instrumentos (`Króno-Sistémo`)

### 14.1 Iso-Calendario de 13 Lunas de 28 Días (`Lúno-Sistémo`)
* **Lunas (Meses):** **`Lúno Un`**, **`Lúno Du`**, **`Lúno Tri`**, ..., **`Lúno Dec-Tri`** (13 meses regulares de 28 días = 364 días).
* **Día de Fin de Año:** **`Ánno-Día`** (Día fuera del tiempo / intercalar).
* **Días de la Semana:** **`Día Un`** (Lunes), **`Día Du`** (Martes), **`Día Tri`** (Miércoles), **`Día Kúa`** (Jueves), **`Día Kin`** (Viernes), **`Día Seks`** (Sábado), **`Día Sépte`** (Domingo).
* **Desambiguación:** **`ánno`** (año astronómico/calendárico) vs. **`anúso`** (ano / anatomía).

### 14.2 Expresiones Horarias y Partes del Día (`��ra-Sistémo`)
* **¿Qué hora es?:** *¿Ké óra es?*
* **Son las 3:** *Es óra tri.*
* **Son las 3 y cuarto:** *Es óra tri et minúto ten kin.*
* **Son las 3 y media:** *Es óra tri et minúto tri ten.*
* **Son las 4 menos cuarto:** *Es óra kúa min minúto ten kin.*
* **A las 3 / En una hora / Hace dos horas:** *A óra tri* / *En un óra* / *Ante du óras*.
* **Partes del Día:** **`matutíno`** (0:00-6:00), **`matíno`** (6:00-12:00), **`medidíe`** (12:00), **`postmedidíe`** (12:00-18:00), **`vespéro`** (18:00-0:00), **`medinókto`** (0:00).
* **Instrumentos Horarios:** **`orológio`** (reloj), **`kronómetro`** (cronómetro), **`orário`** (manecilla de horas), **`minutário`** (manecilla de minutos), **`sekundário`** (segundero).

---

## 15. Módulo Geodésico, Puntos Cardinales y Coordenadas (`Geo-Sistémo`)

### 15.1 Brújula, Prefijos y Regiones Geopolíticas
* **Sustantivos Cardinales y Prefijos:**
  * **Norte:** **`nórto`** (prefijo **`nor-`**)
  * **Sur:** **`súrto`** (prefijo **`sur-`**)
  * **Este:** **`ésto`** (prefijo **`es-`**)
  * **Oeste:** **`oésto`** (prefijo **`os-`**)
  * Compuestos: **`nor-ésto`** (NE), **`sur-oésto`** (SO).
* **Doble Capa Regional/Astronómica:**
  * **`oriénto`**: Oriente / Saliente (nacimiento del sol).
  * **`oksidénto`**: Occidente / Poniente (ocaso del sol - ajuste fonotáctico `ks`).
  * **`septentrióno`** (Norte formal), **`meridióno`** (Sur formal).
* **Coordenadas:** **`latitúdo`**, **`longitúdo`**, **`altitúdo`**, **`equatóro`**, **`hemisféro`**.

---

## 16. Módulo de Metrología Científica, SI y Magnitudes (`Phys-Sistémo`)

### 16.1 Las 7 Unidades Base del SI
`métro` (m), `kilográmo` (kg), `sekúndo` (s), `ampério` (A), `kélvo` (K), `mólo` (mol), `kandélo` (cd).

### 16.2 Unidades Derivadas del SI con Nombre Propio
`hérto` (Hz), `niúto` (N), `paskál` (Pa), `iúlo` (J), `váto` (W), `kúlombo` (C), `vólto` (V), `fárado` (F), `ómo` (Ω), `siémenso` (S), `vébero` (Wb), `téslo` (T), `énrio` (H), `lúmeno` (lm), `lúkso` (lx), `bekerélo` (Bq), `gráo` (Gy), `sivérto` (Sv), `kátalo` (kat).

### 16.3 Prefijos Multiplicadores y Fraccionarios del SI
`déka-` ($10^1$), `ékto-` ($10^2$), `kílo-` ($10^3$), `méga-` ($10^6$), `gíga-` ($10^9$), `téra-` ($10^{12}$), `péta-` ($10^{15}$), `éksa-` ($10^{18}$), `dési-` ($10^{-1}$), `sénti-` ($10^{-2}$), `míli-` ($10^{-3}$), `míkro-` ($10^{-6}$), `náno-` ($10^{-9}$), `píko-` ($10^{-12}$), `fémto-` ($10^{-15}$), `áto-` ($10^{-18}$).

### 16.4 Magnitudes Físicas y Operador de Razón `per`
`longitúdo`, `máso`, `tiémpo`, `korriénto`, `temperatúro`, `kantidá`, `intensidá`, `velosidá` (`métro per sekúndo`), `akelerasión` (`métro per sekúndo²`), `fórso` (`niúto`), `enérgio` (`iúlo`), `poténsio` (`váto`), `presióno` (`paskál`), `frekénsio` (`hérto`), `kárgo` (`kúlombo`), `densidá` (`kilográmo per métro³`), `volúmo` (`métro³`).

---

## 17. Módulo Económico, Monetario y Financiero (`Ekonómo-Sistémo`)

### 17.1 Matriz de Sustantivos Económicos Canonizados
| Concepto (Español) | Término Formal (Askáro) | Regla / Ajuste Morfosintáctico | Etiología / Lógica |
| :--- | :---: | :--- | :--- |
| **Dinero** | **`dinéro`** | Neutro Base en `-o` | Latín *denarius* / Romance. |
| **Moneda / Divisa** | **`monédo`** | Ajuste `-a` $\rightarrow$ **`-o`** | Latín *moneta*. |
| **Precio** | **`prétio`** | Conservación etimológica | Latín *pretium* (evita la africada `c` `/tʃ/`). |
| **Costo / Coste** | **`kósto`** | Ortografía con `k` | Adaptación fonotáctica. |
| **Valor** | **`valóro`** | Desinencia neutra **`-o`** | Latín *valor*. |
| **Tasa / Índice** | **`táso`** | Ajuste `-a` $\rightarrow$ **`-o`** | Latín *taxa*. |
| **Empresa / Compañía** | **`empréso`** | Ajuste `-a` $\rightarrow$ **`-o`** | Ital./Esp. *impresa/empresa*. |
| **Deuda** | **`débito`** | Raíz neolatina pura | Latín *debitum*. |
| **Crédito** | **`krédito`** | Ortografía con `k` | Latín *creditum*. |
| **Pago** | **`págo`** | Neutro Base en `-o` | Romance *pago*. |
| **Ganancia / Lucro** | **`ganánsio`** | Ajuste `-a` $\rightarrow$ **`-o`** | Romance / Latín *lucrum*. |
| **Pérdida** | **`pérdido`** | Ajuste `-a` $\rightarrow$ **`-o`** | Latín *perditum*. |
| **Mercado** | **`merkádo`** | Ortografía con `k` | Latín *mercatus*. |
| **Comercio** | **`komérsio`** | Sustitución de `c` por `s` | Latín *commercium*. |
| **Transacción** | **`transaksión`** | Terminación nominal `-ión` | Latín *transactio*. |
| **Contrato** | **`kontráto`** | Ortografía con `k` | Latín *contractus*. |
| **Factura** | **`faktúro`** | Ajuste `-a` $\rightarrow$ **`-o`** | Latín *factura*. |
| **Recibo** | **`resíbo`** | Neutro Base en `-o` | Romance *recibo*. |

### 17.2 Verbos Transaccionales y Operadores del Mercado
| Acción | Verbo Canónico (Askáro) | Estructura de Envoltura |
| :--- | :---: | :--- |
| **Comprar** | **`askkomprár`** | `ask-` + `kompr-` + `-ár` |
| **Vender** | **`askvendér`** | `ask-` + `vend-` + `-ér` |
| **Pagar** | **`askpagár`** | `ask-` + `pag-` + `-ár` |
| **Cobrar** | **`askkobrár`** | `ask-` + `kobr-` + `-ár` |
| **Deber** | **`askdebér`** | `ask-` + `deb-` + `-ér` |
| **Prestar** | **`askprestár`** | `ask-` + `prest-` + `-ár` |
| **Ahorrar** | **`askahorrár`** | `ask-` + `ahorr-` + `-ár` |
| **Gastar** | **`askgastár`** | `ask-` + `gast-` + `-ár` |
| **Ganar** | **`askganár`** | `ask-` + `gan-` + `-ár` |
| **Perder** | **`askperdér`** | `ask-` + `perd-` + `-ér` |
| **Valer** | **`askvalér`** | `ask-` + `val-` + `-ér` |
| **Costar** | **`askkostár`** | `ask-` + `kost-` + `-ár` |
| **Invertir** | **`askinvestír`** | `ask-` + `invest-` + `-ír` |

### 17.3 Ejemplos Sintácticos Transaccionales
1. **`La empréso pr��s askpagár la débitom.`** *(La empresa paga la deuda).*
2. **`Ko pr��s askvendér la dómom pro prétio álto.`** *(Él vende la casa por un precio alto).*
3. **`Mo pr��s askkobrár kin monédos.`** *(Cobré cinco monedas).*
4. **`Ko pr��s askdebér mil monédos.`** *(Él debe mil monedas).*
5. **`Mos pr��s askahorrár du sen monédos.`** *(Ahorramos doscientas monedas).*

---

## 18. Módulo de Pro-Formas y Sustitución Adjetival (`Pro-Sistémo`)

### 18.1 Canonización de `tál` como Pro-Adjetivo Universal
* **Definición:** `tál` es el pro-adjetivo universal que sustituye a un adjetivo o atributo previamente mencionado en la cláusula.
* **Prosodia:** Monosílabo invariable (`tál`).

#### Ejemplos Sintácticos:
* *La kárto es bóna, et la dátom es tál.* (La carta es buena, y el dato es tal).
* *La sistémo es rável, et la servóro es tál.* (El sistema es rápido, y el servidor es tal).
* *La dómo es grándo, et la kárto es tál.* (La casa es grande, y la carta es tal).

### 18.2 Derivaciones de la Familia de `tál`
| Forma | Función / Significado | Ejemplo Sintáctico |
| :--- | :--- | :--- |
| **`tál`** | tal / así (pro-adjetivo) | *La tál kárto.* |
| **`tálik`** | de tal tipo (adjetival relacional) | *Un kóso tálik.* |
| **`táliko`** | tal cosa (sustantivo neutro abstracto) | *Mo no askvidér tálikom.* |
| **`tálim`** | de tal modo (adverbial modal) | *Ko askfakár tálim.* |

### 18.3 Matriz Unificada del Sistema de Pro-Formas de Askáro
| Pro-forma | Entidad que Sustituye | Forma Canónica (Askáro) | Ejemplo Sintáctico |
| :--- | :--- | :---: | :--- |
| **Pronombre** | Sustantivo / Entidad | **`Ílo`** / **`Eo`** | *Mo askvisár ílom.* |
| **Pro-verbo** | Verbo / Núcleo de acción | **`fak`** / **`obr`** | *Ko askfakár fak.* |
| **Pro-adjetivo** | Adjetivo / Atributo | **`tál`** | *La dátom es tál.* |
| **Pro-adverbio** | Adverbio / Circunstancia | **`hícim`** / **`tálim`** | *Mo askfakár hícim.* |
| **Pro-agente** | Agente indeterminado | **`On`** | *On askdír ke...* |
| **Comodín Nominal** | Objeto / Cosa genérica | **`kóso`** | *Dá Mo kósom.* |
| **Comodín Verbal** | Acción genérica | **`askobrár`** | *Mo askobrár.* |


## 19. Alineamiento Ergativo y Sistema Híbrido de Doble Capa (Macro-Foco + Micro-Ergativo)

### 19.1 El Alineamiento Ergativo-Absolutivo Solo (Morfología de Argumentos Micro)
En Askáro V10.4, el sistema de casos nominales incluye el modo **Ergativo-Absolutivo**, alternativo o complementario al sistema nominativo-acusativo tradicional:

1. **Caso Absolutivo (Forma Base Neutra `-o` / `-a`):**
   - Se utiliza para el sujeto de verbos intransitivos (*"La grándo río prō asksekár"*).
   - Se utiliza para el objeto paciente de verbos transitivos (*"La cérvo la kasadóro-og pr��s askkásar"*).
   - **Economía:** El paciente no requiere desinencia nasal acusativa (`-om`), permaneciendo en la forma base limpia.

2. **Caso Ergativo (Sufijo `-og`):**
   - Reservado exclusivamente para el agente activo que ejecuta una acción transitiva sobre un paciente (*"La kasadóro-og"*).

### 19.2 El Alineamiento de Enfoque Solo (Pragmática Austronesia y Pila Preverbal Macro)
En este modo, los argumentos nominales permanecen en su forma base neutra (`-o`), y la **Pila Preverbal** actúa como el marco cinematográfico y de asignación de roles mediante los operadores con macrón:
- **`sū`**: Foco Sujeto / Agente.
- **`pāc`**: Foco Paciente / Objeto afectado.
- **`lōk`**: Foco Locativo / Escenario.
- **`īns`**: Foco Instrumental / Herramienta.
- **`b��n`**: Foco Beneficiario.
- **`dīr`**: Evidencia Directa presencial.

### 19.3 La Combinación Híbrida: Pila Macro-Foco + Marcación Micro (Invarianza $O(1)$)
La mayor innovación arquitectónica de Askáro V10.4 ocurre al acoplar la **Pila Macro** (Perspectiva cinematográfica de la cláusula) con la **Marcación Micro** (prefijos `ag-`, `pac-`, `inst-`, `lok-` o sufijo `-og` en el sustantivo):

1. **Separación de Responsabilidades:**
   - **Nivel Micro (Sustantivos):** Garantiza la verdad proposicional pura ("quién es qué").
   - **Nivel Macro (Pila Preverbal):** Establece el *zoom*, la focalización y el ángulo de cámara de la escena mental.
2. **Invarianza y Orden Totalmente Libre (*Free Word Order*):**
   Cualquier permutación de los argumentos dentro del enunciado mantiene exactamente la misma validez lógica sin requerir *lookahead*:
   - `lōk dīr pr�� askkásar ag-kasadóro inst-radáro pac-cérvo en la bósko.`
   - `pac-cérvo inst-radáro ag-kasadóro Pāc dīr pr�� askkásar.`
   - `inst-radáro ag-kasadóro pac-cérvo Īns dīr pr�� askkásar.`

3. **Diferenciación de Pronombres Tónicos y Partículas (Sostén de Macrón):**
   Para evitar colisiones entre preposiciones/negaciones monosilábicas y pronombres tónicos, se estandariza el macrón/circunflejo en pronombres:
   - **`Mō`** / **`Mô`** (*yo*), **`Tō`** / **`Tô`** (*tú*), **`Kō`** / **`Kô`** (*él*), **`Kā`** / **`Kâ`** (*ella*), **`Nō`** / **`Nô`** (*nosotros*), **`Sō`** / **`Sô`** (*vosotros*).
   - Permite expresiones como **`to Tō`** (*hacia ti*) y **`no Nō`** (*no nosotros*) sin ambigüedad alguna.
