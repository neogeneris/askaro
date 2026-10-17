# AskÃ¡ro â€” EspecificaciÃ³n Formal V10.4 (Documento Maestro Unificado MonolÃ­tico)
## Interlingua Auxiliar de Base Neolatina (Romance AsiÃ¡tico)
**Fecha de CompilaciÃ³n:** 2026-10-10  
**Estado:** *EspecificaciÃ³n Oficial Completa y MonolÃ­tica (V1.0 a V10.3)*

---

## 1. Arquitectura y NÃºcleo AxiomÃ¡tico

### 1.1 Principio de Isomorfismo y Neutro Base (`-o`)
La versiÃ³n V5.7 de la Arquitectura de Lenguaje Comprimido y Determinista se fundamenta en un principio de **isomorfismo de traducciÃ³n bidireccional (lossless translation)** e **invariancia funcional**:

1. **La terminaciÃ³n `-o` como Neutro Base Universal (ErradicaciÃ³n del GÃ©nero Gramatical en Inanimados)**: A diferencia de los lenguajes naturales romances (donde *la carta*, *la mesa* o *el problema* tienen gÃ©nero gramatical arbitrario), en esta arquitectura **TODOS los objetos inanimados, conceptos y entidades abstractas utilizan strictly el Neutro Base en `-o`** (`kÃ¡rto`, `mÃ©so`, `sistÃ©mo`, `dÃ¡to`, `kÃ¡so`, `kÃ³so`). Queda **estrictamente prohibido asignar la desinencia `-a` a objetos inanimados**.
2. **FlexiÃ³n `-a` / `-or` Exclusiva para Sexo BiolÃ³gico en Seres Vivos**: La flexiÃ³n femenina en **`-a`** (o masculino especÃ­fico en **`-or`**) se reserva **Ãºnicamente para seres vivos y agentes con sexo biolÃ³gico** (`kÃ¡to` -> `kÃ¡ta` *gata*, `usuÃ¡rio` -> `usuÃ¡ria` *usuaria*).
3. **Casos Nasales de Objetos Inanimados**: Al ser neutros en **`-o`**, el acusativo de todo objeto inanimado termina siempre en **`-om`** (`kÃ¡rtom`, `dÃ¡tom`, `sistÃ©mom`, `kÃ³som`), jamÃ¡s en `-am`.


### 1.2 Regla de EliminaciÃ³n de `pro-` (Positivo No Marcado / EconomÃ­a de Marcas)
Se canoniza la simplificaciÃ³n morfolÃ³gica y economÃ­a de marcas para la polaridad y tipificaciÃ³n nominal:
1. **Positivo No Marcado (RaÃ­z Desnuda)**: El estado positivo o estÃ¡ndar de un concepto **no lleva prefijo** (`abÃ©rto`, `kÃ¡ldo`, `vÃ­to`, `lÃºso`). Se erradica el uso del prefijo `pro-` para marcar el estado positivo en reposo.
2. **Polo Negativo (`de-` / `a-`)**: El polo opuesto o inverso se marca con **`de-`** (`deabÃ©rto`, `dekÃ¡ldo`, `devÃ­to`) o **`a-`** para privaciÃ³n presencial (`alÃºso`).
3. **Tercer Polo / Inerte (`a-`)**: El estado neutro o inerte utiliza **`a-`** (`aabÃ©rto`, `akÃ¡ldo`, `avÃ­to`).

### 1.3 Modalidades de RepresentaciÃ³n: Scriptio Continua y Espaciado Universal
El lenguaje posee un diseÃ±o sintÃ¡ctico determinista unificado que se adapta sin fricciÃ³n a cualquier medio de transmisiÃ³n:
1. **Scriptio Continua para Alta Densidad**: La omisiÃ³n de espacios entre palabras es totalmente vÃ¡lida en flujos de datos o parsing informÃ¡tico en $O(1)$, ya que las fronteras de palabra, caso (`-om`, `-em`) y envoltura verbal (`ask-...-Ã¡r/-Ã©r/-Ã­r`) son deterministas.
2. **Espaciado OrtogrÃ¡fico Universal**: Para la lectura humana, la transmisiÃ³n estÃ¡ndar y la sÃ­ntesis de voz (TTS / Text-to-Speech), se utilizan espacios estÃ¡ndar entre palabras para garantizar la inteligibilidad visual y la prosodia natural.

### 1.4 RepresentaciÃ³n Intermedia AnalÃ­tica (IR / Interlingua)
AskÃ¡ro actÃºa como una **RepresentaciÃ³n Intermedia Reestructurada (IR)**. Todo texto de origen se descompone, desambigua y reestructura en sus componentes sintÃ¡cticos explÃ­citos:

`[Sujeto explÃ­cito/desambiguado] + [Pila Preverbal (5 capas)] + [Objeto-om / Dativo-em / PreposiciÃ³n] + ask-[Infijo]-RaÃ­z-Ã¡r/-Ã©r/-Ã­r`

### 1.5 Tolerancia a Fallos, PrÃ©stamos y Nombres de Especies
El sistema estÃ¡ diseÃ±ado con una alta **resiliencia y tolerancia a fallos** frente a textos que contengan prÃ©stamos lingÃ¼Ã­sticos, palabras extranjeras o nombres tÃ©cnicos no asimilados:
1. **Nombres de Especies y TÃ©rminos Consolidados**: En especies animales o tÃ©rminos zoolÃ³gicos/botÃ¡nicos fijados por el uso comÃºn o la biologÃ­a (por ejemplo, *mula*), **no se fuerza una masculinizaciÃ³n artificial a *mulo*** si esto distorsiona la denominaciÃ³n estÃ¡ndar o genera confusiÃ³n.
2. **InserciÃ³n de Palabras Extranjeras**: Si un texto contiene tÃ©rminos externos no asimilados (ej. *software*, *DNA*), las marcas circundantes (el artÃ­culo `la`, la preposiciÃ³n `to` o el marcador de acusativo `-om` si se acopla) permiten que el parser e interprete humano identifiquen el rol sintÃ¡ctico sin que el sistema colapse.

---

### 1.6 Principio de Invariancia de la RaÃ­z
Se establece como axioma fundamental de la arquitectura la **Invariancia Absoluta de la RaÃ­z LÃ©xica**:

1. **Carga Operativa a la Izquierda (PrefijaciÃ³n e InfijaciÃ³n)**: Toda la carga funcional y modificatoria de la oraciÃ³n â€”incluyendo tiempo (`prÄ“`, `prÅ`), aspecto (`dÅ«r`, `sinc`), modales (`mÃ¢nd`, `dÄ“v`, `pÅt`), negaciÃ³n (`no`), voz pasiva (`pÄs` / `-pas-`), derivaciones nominales (`ag-`, `ak-`, `kual-`, `inst-`, `lok-`, `kol-`, `dim-`, `aug-`, `dok-`, `pra-`) y prefijos verbales operativos (`-de-`, `-fal-`, `-kos-`, `-dos-`, `-re-`)â€” es **estrictamente prefixal e infijal a la izquierda**.
2. **RaÃ­z Intacta e Inmune**: La raÃ­z o lexema base (`procÃ©s-`, `fok-`, `sistÃ©m-`, `dÃ¡t-`, `kÃ³s-`, `ped-`) **permanece totalmente intacta, uniforme y libre de apofonÃ­a o deformaciones derivativas/conjugativas** en cualquier contexto sintÃ¡ctico o discursivo.
3. **Casos Nasales Directos a la RaÃ­z**: Las marcas de caso nasales (`-o` nominativo, `-om` acusativo, `-em` dativo, `-im` adverbial) y las envolturas verbales (`-Ã¡r`, `-Ã©r`, `-Ã­r`) se aÃ±aden directamente al extremo final de la raÃ­z.
4. **Reconocimiento del LÃ­mite Argumental en $O(1)$**: Al no competir con sufijos derivativos deformantes en la cola del vocablo, el *parser* computacional y el receptor humano reconocen el lÃ­mite argumental y el rol sintÃ¡ctico de la entidad en complejidad $O(1)$ sin requerir *lookahead*.


---

### 1.7 Nota de DiseÃ±o â€” Transiciones de Estado y EvaluaciÃ³n de `ad-`

Se considerÃ³ la posibilidad de marcar transiciones con el prefijo **`ad-`** (del latÃ­n *ad*, "hacia"), aplicable tanto a estados (`adabÃ©rto` = abriÃ©ndose) como a sustantivos. La idea refleja un patrÃ³n frecuente en muchas lenguas: marcar el estado intermedio entre dos polos, con direcciÃ³n de trÃ¡nsito ("en trÃ¡nsito hacia").

Sin embargo, se optÃ³ por usar los verbos existentes (`askabrÃ­r`, `askserrÃ¡r`, `askfokÃ¡r`), que ofrecen ventajas superiores: conjugan, colapsan la pila preverbal, admiten negaciÃ³n clara, tienen gerundio y permiten derivaciÃ³n nominal. El prefijo **`ad-`** queda documentado como posibilidad para retomar en el futuro.


---

## 2. MorfologÃ­a Nominal, ArtÃ­culo Universal, Casos, Prosodia y DiacrÃ­ticos

### 2.1 El ArtÃ­culo Definido Universal (`la`)
Se canoniza el artÃ­culo **`la`** como el **determinante definido universal e invariable**:
* **Invariancia Total**: Se utiliza sin variaciÃ³n para singular, plural, masculino, femenino y neutro (`la usuÃ¡rio`, `la kÃ¡rto`, `la dÃ¡toms`, `la servÃ³ro`).
* **FunciÃ³n Delimitadora**: Sirve como "campana de apertura" que marca el inicio del grupo nominal y rompe la monotonÃ­a vocÃ¡lica respecto a la terminaciÃ³n neutra `-o`.

### 2.2 El Sistema de Casos Nasales y Casos Oblicuos Vectoriales
El rol sintÃ¡ctico de cada entidad dentro de la oraciÃ³n se determina mediante marcadores nasales en posiciÃ³n final o mediante preposiciones vectoriales puras:

* **Nominativo / Sujeto (`-o` / `-a`)**: Forma base limpia del sustantivo (`kÃ¡to`, `kÃ¡ta`, `sistÃ©mo`, `kÃ³so`).
* **Acusativo / Objeto Directo (`-om` / `-am`)**: AdiciÃ³n de la nasal **`-m`** a la vocal temÃ¡tica activa (`kÃ¡tom`, `kÃ¡rtom`, `sistÃ©mom`, `kÃ³som`).
* **Dativo / Objeto Indirecto o Destino (`-em` / `-aem` o preposiciÃ³n `to`)**:
  * Forma sintÃ©tica: sustituciÃ³n por la vocal de direcciÃ³n **`-e-`** + nasal **`-m`** (`sistÃ©mem`, `kÃ¡tem`).
  * Forma analÃ­tica: preposiciÃ³n **`to`** + artÃ­culo **`la`** + sustantivo base (`to la servÃ³ro`, `to la usuÃ¡rio`).
* **Adverbio de Modo e Instrumental (`-im`)**: DerivaciÃ³n directa reemplazando la vocal temÃ¡tica por **`-im`** (`velocÃ­tim` = *velozmente*, `sistÃ©mim` = *sistemÃ¡ticamente*, `mÃ³dim` = *de cierto modo*).
* **Casos Oblicuos Vectoriales (Locativo, Instrumental, Ablativo)**:
  * **Locativo ("en / dentro de")**: PreposiciÃ³n **`en`** (`en la dÃ³mo` = en la casa) o sufijo opcional **`-in`** (`dÃ³min`).
  * **Instrumental ("con / mediante")**: PreposiciÃ³n **`kun`** (`kun la mikroskÃ³po` = con el microscopio) o desinencia adverbial **`-im`** (`mikroskÃ³pim`).
  * **Ablativo / Origen ("desde / de / por causa de")**: PreposiciÃ³n **`ex`** / **`de`** (`ex la urbo` = desde la ciudad) o sufijo opcional **`-ex`** (`Ãºrbex`).

### 2.3 Posesivo AnalÃ­tico Transparente (`de`)
El posesivo en AskÃ¡ro utiliza la preposiciÃ³n **`de`** seguida del pronombre o sustantivo poseedor en forma base (observando la regla de mayÃºscula gramatical obligatoria en pronombres):
* `la kÃ¡rto de Mo` = mi carta (Sujeto / Nominativo).
* `la kÃ¡rtom de Mo` = mi carta (Objeto Directo / Acusativo, con `-m` en el sustantivo poseÃ­do).
* `la kÃ¡rtom de To` = tu carta.
* `la kÃ¡rtom de Ko` = su carta (de Ã©l/ella/ello).
* `la kÃ¡rtom de Mos` = nuestra carta.
* `la kÃ¡rtom de Tos` = su carta (de ustedes).

### 2.4 OrtografÃ­a y Prosodia Determinista (Regla del Conteo de Vocales)
Para garantizar que la pronunciaciÃ³n y acentuaciÃ³n sean 100% predecibles:
1. **Palabras de 1 vocal (MonosilÃ¡bicas)**: **NUNCA** llevan tilde grÃ¡fica (`Mo`, `To`, `Ko`, `ko`, `kom`, `kur`, `kan`, `pre`, `pro`, `vi`, `va`, `hic`, `is`, `al`, `mag`, `min`, `no`, `si`, `sik`, `nok`, `dok`, `so`, `re`, `to`, `de`, `en`, `kun`, `falls`, `On`, `rel`, `abs`, `pÄs`, `nul`, `un`, `du`, `tri`, `kin`, `seks`, `sep`, `ok`, `nov`, `ten`, `cen`, `mil`).
2. **Palabras de 2 o mÃ¡s vocales**: **SIEMPRE** llevan **exactamente 1 tilde grÃ¡fica** en la vocal que recibe el golpe de voz tÃ³nico (`dÃ¡to`, `sistÃ©mo`, `servÃ³ro`, `kÃ¡rtom`, `mÃ³dim`, `sistÃ©mim`, `sÃ­i`, `alÃ­ter`, `Ã©tunc`, `Ã¡utunc`, `vÃ©ltunc`, `Ã¡utsi`, `vÃ©lsi`, `koÃ©m`, `kÃºi`, `kÃ³mo`, `Ãšbi`, `KÃ­otem`, `KvÃ¡ndo`, `KvomÃ³do`, `kÃ³so`, `kÃºa`, `cÃ©nto`).

### 2.5 EconomÃ­a Cuantitativa de Plurales (Estilo MandarÃ­n)
El plural en **`-s`** es estricto y transparente:
* **Sin cuantificador explÃ­cito**: La marca de plural **`-s`** es **OBLIGATORIA** (`dÃ¡toms` = varios datos, `mÃºlos` = mulas).
* **Con cuantificador explÃ­cito (`Ãºno`, `dÃºo`, `mÃºlto`, `Ã³mno`, `kÃºa-cen`)**: La marca de plural en el sustantivo se **SUPRIME ESTRICTAMENTE** (`dÃºo dÃ¡tom`, `Ã³mno dÃ¡tom`, `kÃºa-cen dÃ³mo`).

### 2.6 NormalizaciÃ³n FonotÃ¡ctica e Inventario Completo de Fonemas (IAST y PÄá¹‡ini)
El sistema formaliza el espectro fonÃ³nico completo del SÃ¡nscrito (IAST / DevanÄgarÄ«) de 5 puntos de articulaciÃ³n (*vargas*), manteniendo un **subconjunto activo neolatino 1:1** en ASCII:

| Punto de ArticulaciÃ³n | Sorda Simple | Sorda Aspirada | Sonora Simple | Sonora Aspirada | Nasal de Clase |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Velares (*Kanthya*)** | **`k`** | **`kh`** | **`g`** | **`gh`** | **`á¹…`** / **`ng`** |
| **Palatales (*TÄlavya*)** | **`c`** (`/tÊƒ/`) | **`ch`** | **`j`** (`/Ê’/`) | **`jh`** | **`Ã±`** |
| **Retroflejas (*MÅ«rdhanya*)** | **`á¹­`** | **`á¹­h`** | **`á¸`** | **`á¸h`** | **`á¹‡`** |
| **Dentales (*Dantya*)** | **`t`** | **`th`** | **`d`** | **`dh`** | **`n`** |
| **Labiales (*Oá¹£á¹­hya*)** | **`p`** | **`ph`** | **`b`** | **`bh`** | **`m`** |

* **Regla FonotÃ¡ctica Activa ASCII**:
  1. `/k/` $\rightarrow$ **`k`** fija siempre. ErradicaciÃ³n de `q` y `c` dura.
  2. `/s/` $\rightarrow$ **`s`** fija siempre.
  3. `/tÊƒ/` ("ch") $\rightarrow$ **`c`** fija siempre (siguiendo el estÃ¡ndar IAST).
  4. `/É¡/` $\rightarrow$ **`g`** dura fija siempre. **Sin `u` muda**: se elimina la `u` en grupos `gu+e/i` (`sÃ¡ngine`, `gitÃ¡rro`, `pengÃ­no`). Se conserva `gu` solo donde la `u` es pronunciada como semivocal etimolÃ³gica (`guÃ©ra`, `guardÃ¢r`, `guÃ¡nto`, `guadÃ¡nyo`).
  5. *(Ratificada 2026-10-17)* **`x` = `/ks/` legÃ­tima** ante cualquier contexto, p.ej. `ex` ('desde'), `komplÃ©xe`. No se podan estas formas.
  6. *(Ratificada 2026-10-17)* **`z` legitima** en prÃ©stamos con redoblamiento o sibilante africada italorromance, p.ej. `pÃ­zzo`, `tazza`, `merlÃºzzo`, `kÃ³zzo`, `strÃºzzo`. No se convierte automÃ¡ticamente en `s`.
  7. *(Ratificada 2026-10-17)* **`w` admitida** en extranjerismos vivos, p.ej. `softwÃ¡re`, `hardwÃ¡ro`.
  8. El alfabeto se inspira en el sÃ¡nscrito (matriz *varÅ·a* IAST de Â§2.6); las letras `z`, `x`, `w` funcionan como prÃ©stamo-tipográficas al estilo de las letras marginales del DevanÄgarÄ«, sin integrarse en las cinco clases de articulaciÃ³n.

### 2.7 Sistema de Capas DiacrÃ­ticas e Isomorfismo ASCII (`^`)
Para lectura humana y marcado prosÃ³dico, el sistema ofrece dos notaciones 1:1 equivalentes:

| CategorÃ­a Funcional | NotaciÃ³n Unicode / MacrÃ³n | NotaciÃ³n ASCII Puro (`^`) | MetÃ¡fora Operativa | Ejemplos |
| :--- | :---: | :---: | :--- | :--- |
| **Pila Preverbal / Auxiliares** | **MacrÃ³n (`Â¯`)** | **Circunflejo (`^`)** | *Rueditas laterales* (TAM/Modal) | `prÄ“` / `prÃª`, `prÅ` / `prÃ´`, `dÄ“v` / `dÃªv`, `pÄs` / `pÃ¢s` |
| **Sustantivos / DeclinaciÃ³n** | **Nasal (`-m`) / AnusvÄra (`Ì‡`)** | **Nasal (`-m`) / Punto (`.`)** | *Anclas argumentales* | `sistÃ©mom`, `kÃ©rveÌ‡` / `kÃ©rve.` |
| **NÃºcleo Verbal (Envoltura)** | **Tilde Aguda (`Â´`) en `-Ã¡r/-Ã©r/-Ã­r`** | **Tilde Aguda (`Â´`) en `-Ã¡r/-Ã©r/-Ã­r`** | *Pedal principal* (Colapso de pila) | `askvisÃ¡r`, `asktenÃ©r`, `askaudÃ­r` |

---


### 2.8 Matriz de Prefijos Nominales Derivativos (Carga a la Izquierda)

Para proteger la integridad de la raÃ­z nominal y reservar la cola de la palabra exclusivamente para las marcas de caso nasales (`-o`, `-om`, `-em`), AskÃ¡ro erradica los sufijos derivativos romances tradicionales (`-dor`, `-ciÃ³n`, `-dad`, `-miento`, `-ismo`, `-ista`) y los sustituye por la **Matriz de Prefijos Nominales Derivativos**:

| Prefijo | FunciÃ³n SemÃ¡ntica | Ejemplo CanÃ³nico | Significado Exacto en AskÃ¡ro | Equivalente Romance Tradicional |
| :---: | :--- | :--- | :--- | :--- |
| **`ag-`** | Agente de la acciÃ³n | **`ag-procÃ©so`** / `ag-procÃ©som` | *el que procesa / el procesador* | *-dor / -tor* |
| **`ak-`** | AcciÃ³n o resultado | **`ak-procÃ©so`** | *el proceso / la acciÃ³n de procesar* | *-ciÃ³n / -miento* |
| **`kual-`** | Cualidad o propiedad | **`kual-procÃ©so`** | *la procesabilidad / cualidad del proceso* | *-dad / -bilidad* |
| **`inst-`** | Instrumento o herramienta | **`inst-procÃ©so`** | *la herramienta o instrumento de proceso* | *-dor / -miento* |
| **`lok-`** | Lugar o espacio | **`lok-procÃ©so`** | *el lugar o planta de procesamiento* | *-dero / -terio / -rÃ­a* |
| **`kol-`** | Colectivo o conjunto | **`kol-procÃ©so`** | *el conjunto de procesos / lote* | *-do / -rÃ­a / -ciÃ³n* |
| **`dim-`** | Diminutivo o escala menor | **`dim-procÃ©so`** | *el subproceso / procesito* | *-ito / -ico* |
| **`aug-`** | Aumentativo o macro-escala| **`aug-procÃ©so`** | *el gran proceso / macroproceso* | *-Ã³n / -azo* |
| **`dok-`** | Doctrina, teorÃ­a o sistema| **`dok-procÃ©so`** | *el procesismo / la teorÃ­a del proceso* | *-ismo* |
| **`pra-`** | Practicante o especialista| **`pra-procÃ©so`** | *el procesista / especialista en procesos*| *-ista* |


## 3. Sistema Pronombral y DesambiguaciÃ³n de 3.Âª Persona

### 3.1 Matriz Unificada de Pronombres Personales, Pro-Formas y Comodines

| Persona / CategorÃ­a | Sujeto / Nominativo (MayÃºscula) | Acusativo (`-m`) | Dativo (`-em` / `to`) | Posesivo (`de`) |
| :--- | :--- | :--- | :--- | :--- |
| **1.Âª Sing. (Yo)** | **`Mo`** | `Mom` | `Moem` / `to Mo` | `de Mo` |
| **1.Âª Plural Inclusivo/Neutro** | **`Mos`** (Mo + To + otros) / **`Mas`** (fem) | `Mosom` / `Masam` | `Mosem` / `Masam` | `de Mos` / `de Mas` |
| **1.Âª Plural Exclusivo** | **`Nos`** (Mo + otros, sin To) | `Nosom` | `Nosem` | `de Nos` |
| **2.Âª Sing. (TÃº)** | **`To`** | `Tom` | `Toem` / `to To` | `de To` |
| **2.Âª Plural (Ustedes)** | **`Tos`** (neutro) / **`Tas`** (fem) | `Tosom` / `Tasam` | `Tosem` / `Tasem` | `de Tos` |
| **3.Âª Sing. Humano Neutro** | **`Ko`** (*Ã©l / persona*) | `Kom` | `Koem` / `to Ko` | `de Ko` |
| **3.Âª Sing. Humano Fem.** | **`Ka`** (*ella*) | `Kam` | `Kaem` / `to Ka` | `de Ka` |
| **3.Âª Sing. Humano Masc.** | **`Kor`** (*Ã©l masculino*) | `Korm` | `Korem` / `to Kor` | `de Kor` |
| **3.Âª Sing. Inanimado / Entidad**| **`Eo`** (*ello / objeto*) | `Eom` | `Eoem` / `to Eo` | `de Eo` |
| **3.Âª Sing. AnafÃ³rico (Pro-forma)**| **`Ãlo`** (*lo / ello mencionado*) | **`Ãlom`** | `Ãloem` / `to Ãlo` | `de Ãlo` |
| **Pronombre LogofÃ³rico** | **`Lo`** (*Ã©l mismo, hablante citado*) | `Lom` | `Loem` / `to Lo` | `de Lo` |
| **Pronombre Negativo** | **`No`** (*nadie / nada / ninguno*) | `Nom` | `Noem` / `to No` | `de No` |
| **Pronombre Indeterminado / ComodÃ­n**| **`On`** (*uno / alguien / se*) | `Onom` | `Onem` / `to On` | `de On` |
| **3.Âª Plural Animat. Neutro** | **`Kos`** (*ellos / personas*) | `Kosom` | `Kosem` | `de Kos` |
| **3.Âª Plural Animat. Femenino** | **`Kas`** (*ellas*) | `Kasam` | `Kasem` | `de Kas` |
| **3.Âª Plural Inanimado** | **`Eos`** (*ellos / objetos*) | `Eosom` | `Eosem` | `de Eos` |

### 3.2 FormaciÃ³n de Reflexivos y RecÃ­procos Mediante `rel` + Acusativo
AskÃ¡ro elimina la necesidad de pronombres reflexivos independientes acoplando la partÃ­cula de visiÃ³n relativa **`rel`** con la forma acusativa del pronombre correspondiente:

* **`rel Mom`** $\rightarrow$ `Mo prÄ“s rel Mom asklavÃ¡r.` *(Me lavo a mÃ­ mismo).*
* **`rel Tom`** $\rightarrow$ `To prÄ“s rel Tom asklavÃ¡r.` *(Te lavas a ti mismo).*
* **`rel Kom`** $\rightarrow$ `Ko prÄ“s rel Kom askvisÃ¡r.` *(Se ve a sÃ­ mismo).*
* **`rel Kam`** $\rightarrow$ `Ka prÄ“s rel Kam askvisÃ¡r.` *(Se ve a sÃ­ misma).*
* **`rel Korm`** $\rightarrow$ `Kor prÄ“s rel Korm askvisÃ¡r.` *(Se ve a sÃ­ mismo).*
* **`rel Eom`** $\rightarrow$ `Eo prÄ“s rel Eom askmodifikÃ¡r.` *(Se modifica a sÃ­ mismo).*
* **`rel Mosom`** $\rightarrow$ `Mos prÄ“s rel Mosom askvisÃ¡r.` *(Nos vemos a nosotros mismos).*
* **`rel Tosom`** $\rightarrow$ `Tos prÄ“s rel Tosom askvisÃ¡r.` *(Se ven a ustedes mismos).*
* **`rel Kosom`** $\rightarrow$ `Kos prÄ“s rel Kosom askvisÃ¡r.` *(Se ven el uno al otro / mutuamente).*

### 3.3 DesambiguaciÃ³n $O(1)$ sin Lookahead y Regla de MayÃºscula Obligatoria
Para garantizar que un parser evalÃºe cada token en $O(1)$ sin requerir *lookahead* ($k=1$):
* **`To`** (mayÃºscula inicial): Pronombre de 2.Âª persona sujeto (*TÃº*).
* **`to`** (minÃºscula inicial): PreposiciÃ³n vectorial de direcciÃ³n (*a / hacia*).
* **`Te`** (mayÃºscula inicial): Pronombre de 2.Âª persona objeto/oblicuo (*A ti / Te*).
* **`te`** (minÃºscula inicial): Determinante demostrativo de distancia media (*ese / esa*).



### 3.5 Cuadrado de AristÃ³teles para Indefinidos (Composicionalidad Pura)

AskÃ¡ro canoniza el Cuadrado de AristÃ³teles puro para cuantificadores e indefinidos mediante la combinaciÃ³n composicional sin alias del cuantificador (`Ã³mno` / `Ãºno`), el sustantivo de dominio (`persÃ³no` / `kÃ³so`) y el operador de negaciÃ³n exocÃ©ntrica (`no`):

#### 1. Dominio de Personas (Humano / Animado)

| Cantidad / Polaridad | Afirmativo | Negativo |
| :--- | :--- | :--- |
| **Universal (Todo/Todos)** | **`Ã³mno persÃ³no`** *(todas las personas / todos)* | **`no Ã³mno persÃ³no`** *(no todas las personas / no todos)* |
| **Particular (Alguno/Uno)** | **`Ãºno persÃ³no`** *(alguno / alguien / una persona)* | **`no Ãºno persÃ³no`** *(ninguna persona / nadie)* |

#### 2. Dominio de Cosas (Inanimado / Entidad)

| Cantidad / Polaridad | Afirmativo | Negativo |
| :--- | :--- | :--- |
| **Universal (Todo/Todos)** | **`Ã³mno kÃ³so`** *(todas las cosas / todo)* | **`no Ã³mno kÃ³so`** *(no todas las cosas)* |
| **Particular (Alguno/Uno)** | **`Ãºno kÃ³so`** *(alguna cosa / algo)* | **`no Ãºno kÃ³so`** *(ninguna cosa / nada)* |

#### ðŸ”‘ Ventaja ArquitectÃ³nica:
* **Cero Alias e Irregularidades:** Se erradica la necesidad de memorizar tablas arbitrarias e irregulares de pronombres indefinidos.
* **Composicionalidad 100% Transparente:** La cuantificaciÃ³n (universal `Ã³mno` / particular `Ãºno`), el dominio semÃ¡ntico (`persÃ³no` / `kÃ³so`) y la negaciÃ³n (`no`) interactÃºan algebraicamente sin excepciones sintÃ¡cticas.

### 3.4 Variables Ordinales (IndizaciÃ³n de Entidades y Personas)
Para evitar la ambigÃ¼edad en discursos con mÃºltiples participantes u objetos del mismo tipo, AskÃ¡ro formaliza un sistema de **variables ordinales** que permiten referenciar entidades y personas segÃºn su orden de apariciÃ³n en el texto:

| Serie | Referente | NotaciÃ³n Documental | Forma Fusionada Natural | Significado Exacto |
| :--- | :--- | :---: | :---: | :--- |
| **Entidades (Inanimados / Cosas)** | Objeto 1 | **`E1`** | **`EÃºnin`** | *La primera entidad / el primer objeto mencionado* |
| | Objeto 2 | **`E2`** | **`EdÃºin`** | *La segunda entidad / el segundo objeto* |
| | Objeto 3 | **`E3`** | **`EtrÃ­in`** | *La tercera entidad / el tercer objeto* |
| | Objeto 4 | **`E4`** | **`EkÃºain`** | *La cuarta entidad / el cuarto objeto* |
| **Personas (Animados / Agentes)** | Persona 1 | **`P1`** | **`PÃºnin`** | *La primera persona / el primer sujeto* |
| | Persona 2 | **`P2`** | **`PdÃºin`** | *La segunda persona / el segundo sujeto* |
| | Persona 3 | **`P3`** | **`PtrÃ­in`** | *La tercera persona / el tercer sujeto* |
| | Persona 4 | **`P4`** | **`PkÃºain`** | *La cuarta persona / el cuarto sujeto* |

#### Ejemplos de DesambiguaciÃ³n con Pronombres Especiales (V6.1)

1. **Plural Exclusivo (`Nos` vs. `Mos`):**
   * `Nos prÄ“s askpartÃ­r, to To prÄ“s askmanÃ©r.`  
     ðŸ‘‰ *"Nosotros (sin ti) nos vamos, tÃº te quedas."*

2. **Pronombre LogofÃ³rico (`Lo` - Discurso Indirecto Desambiguado):**
   * `Ko1 prÄ“ askdicÃ©r ke Lo pro askfakÃ¡r Ã­lom.`  
     ðŸ‘‰ *"Ã‰l1 dijo que Ã©l mismo (Ko1) lo harÃ­a."* (frente a `ke Ko2 pro askfakÃ¡r` = que otro lo harÃ­a).

3. **Pronombre Negativo (`No`):**
   * `No prÄ“s askvenÃ­r.`  
     ðŸ‘‰ *"Nadie viene."*
   * `Mo prÄ“s askvisÃ¡r Nom.`  
     ðŸ‘‰ *"No veo a nadie / a nada."*

4. **Variables Ordinales Fusionadas (`EÃºnin`, `EdÃºin`, `PÃºnin`, `PdÃºin`):**
   * `PÃºnin prÄ“ askenviÃ¡r EÃºnim to PdÃºin.`  
     ðŸ‘‰ *"La Persona 1 enviÃ³ la Entidad 1 a la Persona 2."*
**Regla de MayÃºscula Gramatical Obligatoria en Pronombres:**  
La mayÃºscula inicial en todos los pronombres personales, pro-formas y comodines (`Mo`, `To`, `Ko`, `Ka`, `Kor`, `Eo`, `Ãlo`, `Lo`, `No`, `On`, `Mos`, `Nos`, `Mas`, `Tos`, `Tas`, `Kos`, `Kas`, `Eos`) es un **rasgo gramatical obligatorio** que distingue unÃ­vocamente la categorÃ­a pronombral de partÃ­culas, preposiciones o determinantes (evitando que `de To` se confunda con *"de hacia"*). Esta regla aplica de forma estricta en todas las posiciones sintÃ¡cticas, **incluso en scriptio continua**.

---

## 4. Sistema Demostrativo, DeÃ­ctico y Adverbios de Modo

### 4.1 Determinantes y Pronombres Demostrativos

| Distancia / Esfera | Determinante | Pronombre Independiente | Adverbio de Modo ("AsÃ­") | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **Cerca del Emisor (1.Âª p.)** | `hic` | `hÃ­co` / `hÃ­ca` | `hÃ­cim` | *este / esta / de esta manera* |
| **Cerca del Receptor (2.Âª p.)** | `is` / `te` | `Ã­so` / `tÃ©o` / `tÃ©a` | `Ã­sim` / `tÃ©im` | *ese / esa / de esa manera* |
| **Lejano a Ambos (3.Âª p.)** | `al` / `lac` | `Ã¡lo` / `lÃ¡co` / `lÃ¡ca` | `Ã¡lim` | *aquel / aquella / de aquella manera* |

---

## 5. Operadores Escalares, Comparativos y LÃ©xico de Escala

### 5.1 JustificaciÃ³n del Par Escalar `mag` vs. `min`
Se canoniza **`mag`** (proveniente del latÃ­n *magis*) para "mÃ¡s" con el fin de **evitar la colisiÃ³n homÃ³fona y sintÃ¡ctica con el pronombre de 1.Âª persona plural femenino `Mas`** (*nosotras*).
* `mag` = operador de mayor magnitud (*mÃ¡s*).
* `min` = operador de menor magnitud (*menos*).
* `Mas` = pronombre 1.Âª p. plural femenino (*nosotras*).

---

## 6. JerarquÃ­a SintÃ¡ctica, Pila Preverbal y Ãlgebra Condicional

### 6.1 JerarquÃ­a de Ã“rdenes SintÃ¡cticos: Preferencia CanÃ³nica SOV vs. Libertad del Usuario
En AskÃ¡ro, el orden sintÃ¡ctico se rige por una jerarquÃ­a clara entre la norma canÃ³nica y la flexibilidad discursiva:
1. **Orden Preferente y CanÃ³nico: SOV (Sujeto - Objeto - Verbo)**:
   * **Fundamento EstadÃ­stico**: TipolÃ³gicamente y en universales lingÃ¼Ã­sticos (Greenberg), el orden SOV es el mÃ¡s estable y comÃºn en lenguajes con marcaciÃ³n explÃ­cita de caso.
   * **Encuadre SintÃ¡ctico y Colapso $O(1)$**: Permite acumular todos los argumentos antes de colapsar la pila preverbal mediante el verbo de envoltura (`ask-...-Ã¡r/-Ã©r/-Ã­r`).
   * **Uso en el Documento Maestro**: Por estas razones de optimizaciÃ³n, los ejemplos oficiales de la especificaciÃ³n utilizan **principalmente el orden SOV**.
2. **Flexibilidad Total y Libertad del Usuario**:
   * Dado que cada rol sintÃ¡ctico posee marcas unÃ­vocas (`-om` acusativo, `to` dativo, `la` artÃ­culo), **todos los demÃ¡s Ã³rdenes (SVO, VSO, OVS, VOS, OSV) son 100% vÃ¡lidos y deterministas**.
   * **Libertad discursiva**: Los usuarios son completamente libres de utilizar el orden sintÃ¡ctico en el que se sientan mÃ¡s cÃ³modos en la conversaciÃ³n, lectura o redacciÃ³n.

### 6.2 Estructura de 5 Capas de la Pila Preverbal y ExclusiÃ³n Mutua
La Pila Preverbal se coloca entre el Sujeto y el Verbo. Sus 5 capas se evalÃºan en orden estricto de izquierda a derecha:

`[1. Tiempo (Ï„)] -> [2. Fase/SincronÃ­a (Ï†)] -> [3. EpistÃ©mico (M_ep)] -> [4. DeÃ³ntico (M_de)] -> [5. Polaridad (P)]`

#### 6.2.1 Principio de DispersiÃ³n y Opcionalidad (0 a 5 Slots)
* **Opcionalidad Total (Pila Dispersa / *Sparse Stack*):** Ninguno de los slots de la pila preverbal es obligatorio. Una oraciÃ³n vÃ¡lida puede tener desde **0 auxiliares** (estado base indicativo/atemporal) hasta un mÃ¡ximo estricto de **5 auxiliares** (exactamente uno por cada capa).
* **GraduaciÃ³n de Complejidad (0â€“5 Slots):**
  * **0 Slots (Base atemporal / presente indicativo):** `Ko askfakÃ¡r.` *(Ã‰l hace).*
  * **1 Slot (Tiempo simple):** `Ko prÄ“ askfakÃ¡r.` *(Ã‰l hizo).*
  * **2 Slots (Tiempo + Modo):** `Ko prÄ“ dev askfakÃ¡r.` *(Ã‰l debÃ­a hacer).*
  * **3 Slots (Tiempo + EpistÃ©mico + DeÃ³ntico):** `Ko prÄ“ prob dev askfakÃ¡r.` *(Ã‰l probablemente debÃ­a hacer).*
  * **4 Slots (Tiempo + Fase + EpistÃ©mico + DeÃ³ntico):** `Ko prÄ“ dur prob dev askfakÃ¡r.` *(Ã‰l probablemente debÃ­a continuar haciendo).*
  * **5 Slots (Pila Completa Saturada):** `Ko prÄ“ dur prob dev no askfakÃ¡r.` *(Ã‰l probablemente debÃ­a continuar NO haciendo).*
* **Regla de ExclusiÃ³n Mutua:** Dentro de cada capa individual solo puede seleccionarse **un Ãºnico operador** a la vez.

#### 6.2.2 Naturaleza SemÃ¡ntica de la Polaridad `no` (Capa 5: Operador LÃ³gico vs. Auxiliar)
La desinencia de polaridad **`no`** ubicada en la Capa 5 actÃºa formalmente como un **operador lÃ³gico de negaciÃ³n in-line ($
eg$)** acoplado a la pila:
1. **Alcance de NegaciÃ³n Verbal ($
eg$):** A diferencia de las partÃ­culas de tiempo o modo que aÃ±aden propiedades temporales o volitivas, **`no`** invierte la verdad del nÃºcleo verbal directamente antes del colapso de envoltura (`ask-...-Ã¡r`).
2. **EvaluaciÃ³n de Alcance de Izquierda a Derecha:** Al situarse en la Capa 5 (la mÃ¡s cercana al verbo), la negaciÃ³n queda bajo el alcance (*scope*) de los modales y tiempos a su izquierda. Por ejemplo, `prÄ“ dev no askfakÃ¡r` significa *"tenÃ­a la obligaciÃ³n de no hacer"*, mientras que `no prÄ“ dev askfakÃ¡r` niega la obligaciÃ³n misma (*"no tenÃ­a la obligaciÃ³n de hacer"*).
3. **DiferenciaciÃ³n con `nok`:** Mientras que **`no`** es el operador lÃ³gico de negaciÃ³n preverbal ($
eg$), **`nok`** es la respuesta fÃ¡ctica proposicional independiente ($0$ / *falso*).

`[1. Tiempo (Ï„)] -> [2. Fase/SincronÃ­a (Ï†)] -> [3. EpistÃ©mico (M_ep)] -> [4. DeÃ³ntico (M_de)] -> [5. Polaridad (P)]`

#### Inventario Completo y Exhaustivo de Auxiliares Canonizados:

| Capa | CÃ³digo MacrÃ³n | NotaciÃ³n ASCII (`^`) | CategorÃ­a Gramatical | Significado Exacto |
| :---: | :---: | :---: | :--- | :--- |
| **1. Tiempo (Ï„)** | **`prÄ“`** | `prÃª` | Pasado Absoluto | *OcurriÃ³ / PasÃ³* |
| | **`prÄ“s`** | `prÃªs` | Presente Continuo / Actual | *Ocurre ahora / EstÃ¡ pasando* |
| | **`prÅ`** | `prÃ´` | Futuro Absoluto | *OcurrirÃ¡ / PasarÃ¡* |
| **2. Fase/SincronÃ­a (Ï†)**| **`dÅ«r`** | `dÃ»r` | Durativo / Progresivo | *ContinÃºa ocurriendo / Sigue* |
| | **`sinc`** | `sinc` | SincrÃ³nico / Tiempo Real | *En tiempo real / alineado* |
| | **`desinc`**| `desinc`| AsincrÃ³nico | *EjecuciÃ³n en diferido* |
| | **`pÄs`** | `pÃ¢s` | Pasiva AnalÃ­tica | *Es / fue / serÃ¡ [hecho]* |
| **3. EpistÃ©mico (M_ep)**| **`cÄ“r`** | `cÃªr` | Certeza FÃ¡ctica (100%) | *Ciertamente / Sin duda* |
| | **`prÅb`** | `prÃ´b` | Probabilidad Alta (~80%) | *Probablemente* |
| | **`pÅs`** | `pÃ´s` | Posibilidad (~50%) | *Es posible que / QuizÃ¡s* |
| | **`hÄ«p`** | `hÃ®p` | HipotÃ©tico / Irreal | *En escenario hipotÃ©tico / HabrÃ­a* |
| | **`asÅ«m`** | `asÃ»m` | AsunciÃ³n / Inferencia | *Se asume / Aparentemente* |
| | **`mne`** | `mne` | Registro / Memoria | *SegÃºn constancia en registro* |
| **4. DeÃ³ntico (M_de)** | **`pÅt`** | `pÃ´t` | Capacidad / Facultad | *Puede / Tiene la capacidad de* |
| | **`dÄ“v`** | `dÃªv` | ObligaciÃ³n / Deber | *Debe / Tiene la obligaciÃ³n de* |
| | **`vÅl`** | `vÃ´l` | VoliciÃ³n / Deseo | *Quiere / Desea ejecutar* |
| | **`mÃ¢nd`** | `mÃ¢nd` | Mandato / Imperativo | *Ordena / Instruye ejecutar (Â¡Hazlo!)* |
| **5. Polaridad (P)** | **`nÄ“`** | `nÃª` | InversiÃ³n LÃ³gica del Predicado ($\neg P$) | *Operador de polaridad del predicado (inversiÃ³n de verdad)* |


### 6.3 La TetralogÃ­a de la NegaciÃ³n y DistinciÃ³n AritmÃ©tica/LÃ³gica

Para evitar cualquier solapamiento en lÃ³gica de predicados y parsing determinista, AskÃ¡ro distingue cuatro niveles de negaciÃ³n anÃ¡logos a la distinciÃ³n en aritmÃ©tica entre la **polaridad del nÃºmero** (signo `-`) y la **operaciÃ³n de sustracciÃ³n**:

1. **`nÄ“`** / **`nÃª` (InversiÃ³n LÃ³gica de Polaridad del Predicado $\neg P$):**  
   Ubicado exclusivamente en la **Capa 5 de la Pila Preverbal**. Es el operador unario de inversiÃ³n lÃ³gica sobre el resultado del predicado verbal (anÃ¡logo al signo de polaridad negativa en un valor verdadero/falso). Invierte la ejecuciÃ³n de la acciÃ³n ($
eg P(x)$).
   * *Ejemplo:* `Ko prÄ“ dÄ“v nÄ“ askfakÃ¡r.` *(Tiene la obligaciÃ³n de invertir el resultado de la acciÃ³n: NO-hacer).*

2. **`no` (Operador Relacional y de Alcance Nominal):**  
   Utilizado antes de cuantificadores, adjetivos o grupos nominales para indicar el complemento o conjunto vacÃ­o parcial (anÃ¡logo a la relaciÃ³n de resta/complemento).
   * *Ejemplo:* `no Ãºno persÃ³no` *(complemento de una persona: ninguna persona)*, `no mÃºlto` *(no mucho)*.

3. **`No` (Pronombre Negativo Sustantivo - *"Ninguno / Nadie"*):**  
   Surge de la matriz pronombral por analogÃ­a asociativa (*Mos* -> *Mo* :: *Nos* -> *No*). Lleva mayÃºscula gramatical obligatoria.
   * *Ejemplo:* `No prÄ“s askvenÃ­r.` *(Nadie / Ninguno viene).*

4. **`nok` / `sik` / `dok` (Tokens FÃ¡cticos Independientes - Valores de Verdad $0$, $1$ y $1_{adv}$):**  
   Tokens de respuesta fÃ¡ctica proposicional completa fuera de la pila.
   * *Ejemplo:* `â€” Â¿Ko prÄ“ askvenÃ­r? â€” Nok.` *(â€” Â¿Vino? â€” Falso/0).*


### 6.4 Operador de Envoltura Verbal `ask-...-Ã¡r/-Ã©r/-Ã­r`
* Prefijo invariable **`ask-`** (Apertura).
* Infijos operativos opcionales (`-pas-` pasiva sintÃ©tica, `-n-` nulidad, `-de-` reverso, `-fal-` fallo, `-kos-` acoplamiento, `-dos-` disyunciÃ³n, `-re-` repeticiÃ³n).
* Sufijos eufÃ³nicos continentales **`-Ã¡r`**, **`-Ã©r`**, **`-Ã­r`** (de las 3 conjugaciones latinas *-Äre*, *-Ä“re/-Ä›re*, *-Ä«re*).
* Tilde grÃ¡fica obligatoria como gatillo de colapso de la pila verbal (*stack collapse*).

### 6.5 Ãlgebra Condicional, Anidamientos Excluyentes y Conectores de Rama (`Ã©tunc`, `Ã¡utunc`, `vÃ©ltunc`, `Ã¡utsi`, `vÃ©lsi`, `secus`)
* **`si`**: Condicional bÃ¡sico (*Si...*).
* **`sÃ­i`**: Bicondicional (*Si y solo si...*).
* **`tunc`**: Consecuencia (*entonces...*).
* **`Ã©tunc`**: Y entonces / a continuaciÃ³n (secuencia lineal).
* **`Ã¡utunc`**: O entonces / o bien en tal caso (consecuencia alternativa excluyente).
* **`vÃ©ltunc`**: O incluso entonces (consecuencia alternativa inclusiva).
* **`Ã¡utsi`**: O si / en cambio si (`else if` excluyente).
* **`vÃ©lsi`**: O incluso si (`inclusive else if`).
* **`secus`**: De lo contrario / si no (*else* final).
* **`alÃ­ter`**: De otra manera / por otro mÃ©todo (procedimiento alternativo).
* **`falls`**: Condicional de falla o excepciÃ³n (*en caso eventual de que...*).

### 6.6 Sistema Unificado de SubordinaciÃ³n y ClÃ¡usulas Complejas

#### Tabla Resumen Canonizada de Relativos (ClÃ¡usulas Adjetivas):

| FunciÃ³n SintÃ¡ctica | Forma CanÃ³nica | Vocales | Tilde (Prosodia) | Ejemplo CanÃ³nico en AskÃ¡ro |
| :--- | :---: | :---: | :---: | :--- |
| **Sujeto** | **`ko`** | 1 | **No** | `La usuÃ¡rio ko prÄ“s askadministrÃ¡r...` |
| **Objeto Directo** | **`kom`** | 1 | **No** | `La kÃ¡rto kom To prÄ“ askenviÃ¡r...` |
| **Dativo** | **`koÃ©m`** | 2 (`o`, `e`) | **SÃ­ (aguda)** | `La usuÃ¡rio koÃ©m Mo prÄ“ askenviÃ¡r...` |
| **Posesivo** | **`kÃºi`** | 2 (`u`, `i`) | **SÃ­ (llana)** | `La sistÃ©mo kÃºi servÃ³ro prÄ“s askoperÃ¡r...` |
| **Locativo** | **`kur`** | 1 | **No** | `La dÃ³mo kur Ko prÄ“s askvivÃ­r...` |
| **Temporal** | **`kan`** | 1 | **No** | `La diÃ¡no kan Ko prÄ“ askarivÃ¡r...` |
| **Modal** | **`kÃ³mo`** | 2 (`o`, `o`) | **SÃ­ (llana)** | `La mÃ³do kÃ³mo Ko prÄ“ askfakÃ¡r...` |

#### Tabla de ClÃ¡usulas Subordinadas Sustantivas (Completivas e Interrogativas Indirectas):

| Tipo de ClÃ¡usula | Introductor | FunciÃ³n SintÃ¡ctica | Ejemplo CanÃ³nico en AskÃ¡ro |
| :--- | :--- | :--- | :--- |
| **Completiva Declarativa** | **`ke`** | Sustituye argumento verbal | `Mo prÄ“s asksabÃ©r ke la servÃ³ro prÄ“s askoperÃ¡r.` |
| **Interrogativa Indirecta SÃ­/No** | **`an`** | Sustituye argumento verbal | `Mo prÄ“s askpreguntÃ¡r an la servÃ³ro prÄ“s askoperÃ¡r.` |
| **Interrogativa Indirecta Parcial**| **`Kv-`** (`kvo`, `kve`...) | Sustituye argumento verbal | `Mo no prÄ“s asksabÃ©r kvo la usuÃ¡rio prÄ“s askfakÃ¡r.` |

### 6.7 TrÃ­ada de Perspectiva (`abs`, `rel`, `su`) y PartÃ­cula Evidencial Directa (`dir`)

AskÃ¡ro resuelve de forma determinista la perspectiva pragmÃ¡tica, el foco sobre el sujeto y la fuente evidencial de la informaciÃ³n mediante la **TrÃ­ada de Perspectiva** y el operador de atestiguamiento directo **`dir`**:

#### 1. TrÃ­ada CanÃ³nica de Perspectiva (`abs`, `rel`, `su`)

* **`abs` (VisiÃ³n Absoluta):** Marco objetivo, ontolÃ³gico o universal (*en su totalidad / objetivamente*).
* **`rel` (VisiÃ³n Relativa):** Marco contextual o referencial (*en relaciÃ³n con / para tal entidad*).
* **`su` (VisiÃ³n Subjetiva / Foco en Sujeto):** Marco vivencial, interno o de exclusiÃ³n de foco sobre el sujeto (*solo Ã©l / desde el enfoque propio del sujeto*).

#### 2. Operador Evidencial de Atestiguamiento Directo (`dir`)

* **`dir` (Atestiguamiento Directo):** Marca que la acciÃ³n expresada por el enunciado fue **observada o presenciada directamente en persona por el hablante** (*lo vi directamente / consta de primera mano*).

#### Tabla Resumen de Perspectiva y Evidencialidad:

| Estructura | Enfoque SemÃ¡ntico | Ejemplo CanÃ³nico | Significado Exacto |
| :--- | :--- | :--- | :--- |
| **Base Neutra** | Enunciado neutro estÃ¡ndar | `Ko prÄ“s askfakÃ¡r.` | *Ã‰l hace.* |
| **Foco Sujetivo (`su`)** | Foco exclusivo en el sujeto | `Su Ko prÄ“s askfakÃ¡r.` | *Solo Ã©l hace / Enfoque propio de Ã©l.* |
| **Atestiguamiento (`dir`)**| Evidencia visual/directa | `Ko dir prÄ“s askfakÃ¡r.` | *Ã‰l hace (lo vi directamente).* |
| **Foco + Atestiguamiento** | Sujeto exclusivo + Evidencia directa | `SÅ« Ko dÄ«r prÄ“s askfakÃ¡r.` | *Solo Ã©l hace, y lo vi directamente.* |
| **VisiÃ³n Absoluta (`abs`)**| Perspectiva universal | `abs Mo prÄ“s askvisÃ¡r la kÃ³som.` | *Vi la cosa en su totalidad.* |
| **VisiÃ³n Relativa (`rel`)**| Perspectiva referencial | `rel Mo, la kÃ³so prÄ“s askesÃ©r dÃ­ficil.` | *Para mÃ­, la cosa es difÃ­cil.* |


### 6.8 TaxonomÃ­a Formal de Pro-Formas Gramaticales vs. Comodines LÃ©xicos

| CategorÃ­a | Forma | Tipo Gramatical | FunciÃ³n SintÃ¡ctica y PragmÃ¡tica | Ejemplo CanÃ³nico en AskÃ¡ro |
| :--- | :--- | :--- | :--- | :--- |
| **AnÃ¡fora** | **`Ãlo` / `Eo`** | Pro-nombre | Sustituye a una entidad/sustantivo antecedente conocido | `Mo prÄ“s askvisÃ¡r Ã­lom.` *(Lo vi).* |
| **AnÃ¡fora** | **`fak`** | Pro-verbo | Sustituye a una acciÃ³n/verbo antecedente conocido | `Ko prÅ askfakÃ¡r fak.` *(Ã‰l lo harÃ¡ / ejecutarÃ¡ esa acciÃ³n).* |
| **AnÃ¡fora** | **`On`** | Pro-agente | Sustituye a un agente humano genÃ©rico o indeterminado | `On prÄ“s askdicÃ©r ke...` *(Se dice / Uno dice que...).* |
| **ComodÃ­n** | **`kÃ³so`** | ComodÃ­n nominal | Llena un vacÃ­o lÃ©xico cuando se ignora o no se nombra el objeto | `To to Mo la kÃ³som prÄ“s askdar.` *(Dame esa cosa).* |
| **ComodÃ­n** | **`askkosÃ¡r`** | Pro-verbo genÃ©rico | Llena un vacÃ­o de acciÃ³n sobre un objeto sin nombrar el verbo tÃ©cnico | `Mo eom prÄ“ askkosÃ¡r.` *(Lo cosiÃ© / procesÃ© la cosa).* |
| **ComodÃ­n** | **`askobrÃ¡r`** | Verbo de intervenciÃ³n | Llena un vacÃ­o de labor o trabajo fÃ­sico sobre una estructura | `Mos prÄ“ askobrÃ¡r en la dÃ³mo.` *(Estuvimos obrando en la casa).* |

---

## 7. Sistema NumÃ©rico Base 10, Multiplicadores Posicionales y Sufijos Funcionales

### 7.1 DÃ­gitos Primarios (0â€“9) y Regla del Conteo de Vocales
El sistema numÃ©rico de AskÃ¡ro opera en **Base 10 pura** con concatenaciÃ³n lineal posicional de izquierda a derecha. Los diez dÃ­gitos fundamentales se construyen sobre raÃ­ces monosilÃ¡bicas (excepto `kÃºa`, que posee 2 vocales y lleva tilde en la `Ãº` para cumplir estrictamente la Regla del Conteo de Vocales):

| Cifra | DÃ­gito CanÃ³nico | Vocales | Tilde (Prosodia) | Significado |
| :---: | :---: | :---: | :---: | :--- |
| **0** | **`nul`** | 1 | No | *cero* |
| **1** | **`un`** | 1 | No | *uno* |
| **2** | **`du`** | 1 | No | *dos* |
| **3** | **`tri`** | 1 | No | *tres* |
| **4** | **`kÃºa`** | 2 (`u`, `a`) | **SÃ­ (`Ãº`)** | *cuatro* |
| **5** | **`kin`** | 1 | No | *cinco* |
| **6** | **`seks`** | 1 | No | *seis* |
| **7** | **`sep`** | 1 | No | *siete* |
| **8** | **`ok`** | 1 | No | *ocho* |
| **9** | **`nov`** | 1 | No | *nueve* |

### 7.2 Multiplicadores Posicionales y Sustantivos Base (`cÃ©nto`)
Las Ã³rdenes de magnitud se construyen mediante multiplicadores posicionales transparentes. El multiplicador **`cen`** ($	imes 100$) se explica y fundamenta dinÃ¡micamente sobre el sustantivo neutro base **`cÃ©nto`** (*el ciento / la centena*):

* **`ten`** (Decena / $10^1$): Derivado de `tÃ©no` / `decÃ©no`.
* **`cen`** (Centena / $10^2$): Derivado de **`cÃ©nto`** (*el ciento / la centena*).
* **`mil`** (Millar / $10^3$): Derivado de `mÃ­lo`.
* **`mÃ­lion`** (MillÃ³n / $10^6$): Derivado de `mÃ­liono`.
* **`mÃ­liard`** (Mil millones / $10^9$): Derivado de `mÃ­liardo`.

### 7.3 Reglas de ComposiciÃ³n Lineal (Decenas, Centenas y Millares)
Los nÃºmeros compuestos se forman multiplicando la cifra por la base posicional y sumando las unidades sucesivas en orden directo:

#### A. Decenas (10â€“99):
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
ightarrow$ **`kÃºa-ten`**
* **45** ($4 	imes 10 + 5$) $
ightarrow$ **`kÃºa-ten-kin`**
* **99** ($9 	imes 10 + 9$) $
ightarrow$ **`nov-ten-nov`**

#### B. Centenas (100â€“999):
* **100** ($1 	imes 100$) $
ightarrow$ **`un-cen`** (sustantivo: **`la cÃ©nto`**)
* **200** ($2 	imes 100$) $
ightarrow$ **`du-cen`** (sustantivo: **`dÃºo cÃ©ntos`**)
* **347** ($3 	imes 100 + 40 + 7$) $
ightarrow$ **`tri-cen-kÃºa-ten-sep`**
* **400** ($4 	imes 100$) $
ightarrow$ **`kÃºa-cen`**
* **444** ($4 	imes 100 + 40 + 4$) $
ightarrow$ **`kÃºa-cen-kÃºa-ten-kÃºa`**
* **512** ($5 	imes 100 + 10 + 2$) $
ightarrow$ **`kin-cen-un-ten-du`**

#### C. Millares y Grandes Cifras (1000+):
* **1000** ($1 	imes 1000$) $
ightarrow$ **`un-mil`**
* **1200** ($1000 + 200$) $
ightarrow$ **`un-mil-du-cen`**
* **2026** ($2 	imes 1000 + 20 + 6$) $
ightarrow$ **`du-mil-du-ten-seks`**

### 7.4 Trinidad de Sufijos NumÃ©ricos Funcionales
Los nÃºmeros generan derivados gramaticales unÃ­vocos segÃºn su rol en el enunciado:

| CategorÃ­a Funcional | Sufijo | Ejemplo | Significado Exacto |
| :--- | :---: | :--- | :--- |
| **Cardinal / Cantidad Pura** | **`-o`** | `Ãºn-o`, `dÃº-o`, `trÃ­-o`, `kÃºa-o`, `kÃ­n-o` | *uno, dos, tres, cuatro, cinco* |
| **Ordinal / PosiciÃ³n** | **`-in`** | `unin`, `duin`, `triin`, `kÃºain` | *primero, segundo, tercero, cuarto* |
| **Partitivo / FracciÃ³n** | **`-fra`** | `dufra`, `trifra`, `kÃºafra`, `du tri-fra` | *mitad, tercio, cuarto, dos tercios* |
| **Multiplicativo** | **`-ple`** | `duple`, `triple`, `kÃºaple` | *doble, triple, cuÃ¡druple* |
| **Frecuencia / RepeticiÃ³n** | **`-vece`** | `un-vece`, `du-vece`, `tri-vece` | *una vez, dos veces, tres veces* |

### 7.5 EconomÃ­a Cuantitativa de Plurales (Estilo MandarÃ­n)
Cuando un sustantivo estÃ¡ precedido por un nÃºmero o cuantificador explÃ­cito, la marca de plural **`-s`** en el sustantivo se **suprime strictly** para evitar redundancia:
* `dÃºo dÃ¡tom` *(dos datos â€” no dÃºo dÃ¡toms)*
* `kÃºa-cen dÃ³mo` *(cuatrocientas casas â€” no kÃºa-cen dÃ³mos)*
* `omno sistÃ©mo` *(todos los sistemas)*

---

## 8. Tablas de Preposiciones, Conjunciones y Adverbios Canonizados

### 8.1 Preposiciones Vectoriales
* **`en`**: En / dentro de / sobre (Locativo).
* **`to`**: A / hacia / para (DirecciÃ³n / Dativo analÃ­tico).
* **`de`**: De / desde / posesivo (Origen / PosesiÃ³n).
* **`ex`**: Desde / fuera de / por causa de (Ablativo).
* **`kun`**: Con / en compaÃ±Ã­a de / mediante (Instrumental).
* **`sin`**: Sin / en ausencia de.
* **`per`**: Por / a travÃ©s de / mediante.
* **`pro`**: Para / en favor de / con propÃ³sito de.
* **`sub`**: Bajo / debajo de.
* **`sup`**: Sobre / encima de.
* **`ante`**: Antes de / delante de.
* **`post`**: DespuÃ©s de / detrÃ¡s de.
* **`inter`**: Entre (dos o mÃ¡s entidades).
* **`trans`**: A travÃ©s de / mÃ¡s allÃ¡ de.

### 8.2 Conjunciones y Conectores LÃ³gicos
* **`et`**: Y (ConjunciÃ³n copulativa simple).
* **`ets`**: Y ademÃ¡s / asimismo / simultÃ¡neamente (ConjunciÃ³n aditiva de co-ocurrencia).
* **`vel`**: O (DisyunciÃ³n inclusiva: A o B, o ambos).
* **`aut`**: O (DisyunciÃ³n exclusiva: A o B, pero no ambos).
* **`re`**: Porque / dado que (Causal).
* **`so`**: AsÃ­ que / por lo tanto (Consecutivo).
* **`si`**: Si (Condicional).
* **`sÃ­i`**: Si y solo si (Bicondicional).
* **`tunc`**: Entonces (Consecuencia de condicional).
* **`Ã©tunc`**: Y entonces / a continuaciÃ³n (secuencia lineal).
* **`Ã¡utunc`**: O entonces / o bien en tal caso (consecuencia alternativa excluyente).
* **`vÃ©ltunc`**: O incluso entonces (consecuencia alternativa inclusiva).
* **`Ã¡utsi`**: O si / en cambio si (`else if` excluyente).
* **`vÃ©lsi`**: O incluso si (`inclusive else if`).
* **`secus`**: De lo contrario / si no (*else* final).
* **`alÃ­ter`**: De otra manera / por otro mÃ©todo (Procedimiento alternativo).
* **`quam`**: Que / en comparaciÃ³n con (Comparativo).

### 8.3 Adverbios BÃ¡sicos, PartÃ­culas PragmÃ¡ticas y ConfirmaciÃ³n FÃ¡ctica
* **`An`**: PartÃ­cula interrogativa polar estructuradora (ubicada al inicio de la clÃ¡usula para seÃ±alar el marco interrogativo Â¿...? en $O(1)$).
* **`Ah`**: PartÃ­cula exclamativa/emotiva espontÃ¡nea (expresa Ã©nfasis, sorpresa o asombro: *Â¡Ah! / Â¡Efectivamente!*).
* **`Ah! Sic!`**: *Â¡Ah, sÃ­! / Â¡Efectivamente! / Â¡Confirmado!*
* **`Ah! Noc!`**: *Â¡Ah, no! / Â¡De ninguna manera! / Â¡Falso!*
* **`Ah! Dok!`**: *Â¡Ah, al contrario, sÃ­! / Â¡Pues claro que sÃ­!*
* **`ya`**: Ya / actualmente / inmediatamente (Marcador temporal de aspecto realizado/presente).
* **`sik`**: SÃ­ / confirmed / asÃ­ es (AfirmaciÃ³n fÃ¡ctica 1).
* **`nok`**: No / falso / no es asÃ­ (NegaciÃ³n fÃ¡ctica 0).
* **`dok`**: Al contrario, sÃ­ (AfirmaciÃ³n adversativa / *doch*).
* **`hÃ­cim`**: De este modo / asÃ­ (DeÃ­ctico 1.Âª p.).
* **`Ã­sim`**: De ese modo / asÃ­ (DeÃ­ctico 2.Âª p.).
* **`Ã¡lim`**: De aquel modo (DeÃ­ctico 3.Âª p.).
* **`mÃ³dim`**: De cierto modo / de alguna manera.
* **`sistÃ©mim`**: SistemÃ¡ticamente (de `sistÃ©mo` + `-im`).
* **`mag`**: MÃ¡s / mayor grado.
* **`min`**: Menos / menor grado.

### 8.4 Matriz Unificada de Interrogativos Vectoriales (`Kio-`)

| DimensiÃ³n SintÃ¡ctica | RaÃ­z Dimensional | Forma Vectorial (AnalÃ­tica) | Forma AtÃ³mica (Comprimida) | Significado Exacto |
| :--- | :--- | :--- | :--- | :--- |
| **Entidad Inanimada** | `-o` / `-om` | **`Kio-o`** / **`Kio-om`** | **`KÃ­oo`** / **`KÃ­om`** $\rightarrow$ **`Kvo`** / **`Kvom`** | *Â¿QuÃ© objeto / QuÃ© cosa?* |
| **Agente Humano** | `-or` / `persono` | **`Kio-or`** | **`KÃ­or`** $\rightarrow$ **`Kve`** / **`Kvem`** | *Â¿QuÃ© persona / QuiÃ©n?* |
| **DimensiÃ³n Temporal**| **`tem`** (de `tÃ©mpo`)| **`Kio-tem`** | **`KÃ­otem`** $\rightarrow$ **`KvÃ¡ndo`** | *Â¿En quÃ© tiempo / CuÃ¡ndo?* |
| **DimensiÃ³n Espacial**| `ino` / `zono` | **`Kio-ino`** | **`KÃ­oino`** $\rightarrow$ **`Ãšbi`** | *Â¿En quÃ© lugar / DÃ³nde?* |
| **Causalidad LÃ³gica** | `re` | **`Kio-re`** | **`KÃ­ore`** $\rightarrow$ **`Kvar`** | *Â¿Por quÃ© causa / Por quÃ©?* |
| **Modo / EjecuciÃ³n** | `mod` / `fak` | **`Kio-mod`** | **`KÃ­omod`** $\rightarrow$ **`KvomÃ³do`** | *Â¿De quÃ© modo / CÃ³mo?* |

---

## 9. CompilaciÃ³n del Benchmark de Casos de Prueba (V6.0)

### ðŸ§ª Caso 01: Estado Base Neutro y Secuencia Narrativa con `Ã©tunc`
> *"El usuario presiona el botÃ³n, y entonces la mÃ¡quina arranca."*
* **TraducciÃ³n (SOV CanÃ³nico)**: `La usuÃ¡rio la botÃ³nom prÄ“ askpresiÃ³nÃ¡r, Ã©tunc la mÃ¡kino prÄ“ askarrancÃ¡r.`
* **AnÃ¡lisis**: Sujeto + Acusativo (`botÃ³nom`) + Verbo + Conector secuencial (`Ã©tunc`) + ClÃ¡usula consecuente.

### ðŸ§ª Caso 02: Condicional Complejo con `Ã¡utsi` (`else if`), `Ã¡utunc` y `secus` (`else`)
> *"Si la mÃ¡quina procesa el dato, envÃ­a la respuesta; o si el servidor de respaldo procesa, envÃ­a hacia allÃ­; de lo contrario, notifica el error."*
* **TraducciÃ³n**: `si la mÃ¡kino la dÃ¡tom askprocesÃ¡r tunc la responsÃ³m askenviÃ¡r; Ã¡utsi la backup-servÃ³ro prÄ“s askprocesÃ¡r Ã¡utunc to hÃ­co askenviÃ¡r; secus la errÃ³rom asknotifikÃ¡r.`
* **AnÃ¡lisis**: Condicional `si` + Rama alternativa excluyente `Ã¡utsi` con consecuencia `Ã¡utunc` + Rama por defecto `secus` (`else`).

### ðŸ§ª Caso 03: ExpresiÃ³n de Grandes Cantidades y EconomÃ­a de Plurales
> *"Cuatrocientas cuarenta y cuatro personas procesaron mil doscientos datos en dos veces."*
* **TraducciÃ³n**: `KÃºa-cen-kÃºa-ten-kÃºa persono un-mil-du-cen dÃ¡tom du-vece prÄ“ askprocesÃ¡r.`
* **AnÃ¡lisis**: Sujeto numeral (`KÃºa-cen-kÃºa-ten-kÃºa persono` sin `-s` en `persono`) + Objeto numeral (`un-mil-du-cen dÃ¡tom` sin `-s` en `dÃ¡tom`) + Adverbio distributivo (`du-vece`) + Verbo pasado.


### ðŸ§ª Caso 04: DemostraciÃ³n de Perspectiva Sujetiva (`su`) y Evidencia Directa (`dir`)

DemostraciÃ³n de la graduaciÃ³n de foco y evidencia empÃ­rica en AskÃ¡ro V6.0:

1. **AfirmaciÃ³n Base Neutra:**  
   ðŸ‘‰ **`Ko prÄ“s askfakÃ¡r.`**  
   *(Ã‰l hace).*

2. **Aislamiento de Foco Sujetivo (`su`):**  
   ðŸ‘‰ **`Su Ko prÄ“s askfakÃ¡r.`**  
   *(Solo Ã©l hace / Enfoque exclusivo en el sujeto).*

3. **InclusiÃ³n de Evidencia Directa Presencial (`dir`):**  
   ðŸ‘‰ **`Ko dir prÄ“s askfakÃ¡r.`**  
   *(Ã‰l hace [lo vi directamente]).*

4. **SÃ­ntesis Completa (Foco + Evidencia Directa):**  
   ðŸ‘‰ **`SÅ« Ko dÄ«r prÄ“s askfakÃ¡r.`**  
   *(Solo Ã©l hace, y lo vi directamente).*



### 6.8 Isomorfismo Completo: Sufijos Romance vs. Prefijos Composicionales (MÃ³dulo 09)

Para garantizar la interoperabilidad entre el estilo fluido/humano (sufijaciÃ³n romance) y el estilo puramente analÃ­tico/agente de IA (prefijaciÃ³n composicional), AskÃ¡ro V7.1 establece una equivalencia 1:1 estricta:

| Sufijo Romance | Prefijo Composicional | Ejemplo Sufijado | Ejemplo Prefijado | Significado Operativo |
| :---: | :---: | :--- | :--- | :--- |
| **`-Ã³r`** | **`ag-`** | `procesÃ³r` | `agprocÃ©so` | Agente / El que procesa |
| **`-tÃ³rio`** | **`inst-`** | `procesatÃ³rio` | `instprocÃ©so` | Instrumento / Herramienta |
| **`-Ã­to`** | **`mikro-`** | `kartÃ­to` | `mikrokÃ¡rto` | Diminutivo / Escala menor |
| **`-Ã³to`** | **`makro-`** | `kartÃ³to` | `makrokÃ¡rto` | Aumentativo / Escala mayor |
| **`-Ã¡ro`** | **`kon-`** | `kartÃ¡ro` | `konkÃ¡rto` | Colectivo / Conjunto |
| **`-erÃ­o` / `-Ã­no`** | **`lok-`** | `karterÃ­o` | `lokkÃ¡rto` | UbicaciÃ³n / Lugar de la entidad |
| **`-Ã­smo`** | **`dok-`** | `sistemÃ­smo` | `doksistÃ©mo` | Doctrina / Marco teÃ³rico |
| **`-Ã­sto`** | **`pra-`** | `sistemÃ­sto` | `prasistÃ©mo` | Practicante / Agente ejecutor |
| **`-itÃ¡`** | **`kwal-`** | `bonitÃ¡` | `kwalbÃ³no` | Cualidad abstracta |


### 2.9 Gerundios MorfolÃ³gicos con MacrÃ³n (`-Ã¢ndo`, `-Ãªndo`, `-Ã®ndo`)
El gerundio se construye agregando la desinencia con macrÃ³n a la raÃ­z segÃºn la conjugaciÃ³n verbal:
* **1.Âª ConjugaciÃ³n (`-Ã¡r`)**: **`-Ã¢ndo`** (ASCII: `-ando`) $\rightarrow$ `kaminÃ¢ndo`, `trabahÃ¢ndo`.
* **2.Âª ConjugaciÃ³n (`-Ã©r`)**: **`-Ãªndo`** (ASCII: `-endo`) $\rightarrow$ `komÃªndo`, `procesÃªndo`.
* **3.Âª ConjugaciÃ³n (`-Ã­r`)**: **`-Ã®ndo`** (ASCII: `-indo`) $\rightarrow$ `vivÃ®ndo`, `escribÃ®ndo`.

### 2.1.bis Axioma de Cierre Nominal Reforzado — Prohibición de sustantivos en -e *(Ratificada 2026-10-17)*

Ningún sustantivo del lexigo puede finalizar en `-e`. Estrategias de cierre admitidas:

1. **Restauración de vocal temática + cierre neutro -o** para temas consonánticos latinos:
   máre → **máro**, sále → **sálo**, lége → **légo**, kárne → **kárno**, lákte → **lákto**, sángine → **sanguíno**.
2. **Sufijo derivativo transparente** cuando la raíz termina en vocal: ave → **avéso**, avestruz → **avéstruso**.
3. **Raíz pura etimológica** en parentesco: abuelo → **ávo** (< avus), abuela → **áva** (< ava; capa biológica -a legítima).
4. El femenino biológico en **-a** NO viola esta regla (áva, lúna, stélla, kúa).

Léxico fijado por el acuñador: **ávo** (abuelo), **áva** (abuela), **avéso** (ave), **avéstruso** (avestruz).
Además, quedan eliminadas del lexigo las palabras compuestas con espacio (§4): se expresan por composición analítica o prefijación.

### 2.10 Verbo de Aspecto Continuo `askandÃ¡r` (Andar / Caminar / Auxiliar)
Se canoniza el verbo **`askandÃ¡r`** (Stem: `and-`, Prosodia: 3 sÃ­labas, tilde en `Ã¡`) con doble funciÃ³n sintÃ¡ctica:
1. **Uso como Verbo Pleno (Movimiento)**: `Mo askandÃ¡r.` $\rightarrow$ *Ando / camino.*
2. **Uso como Auxiliar Progresivo (Iberorromance `andar + gerundio`)**: `Mo askandÃ¡r trabahÃ¢ndo.` $\rightarrow$ *Ando trabajando.*

#### InteracciÃ³n con la Pila Preverbal:
* `Mo prÄ“ askandÃ¡r trabahÃ¢ndo.` $\rightarrow$ *Anduve trabajando.*
* `Mo prÅ askandÃ¡r trabahÃ¢ndo.` $\rightarrow$ *AndarÃ© trabajando.*
* `Mo dÄ“v askandÃ¡r trabahÃ¢ndo.` $\rightarrow$ *Debo andar trabajando.*
* `Mo dÅ«r askandÃ¡r trabahÃ¢ndo.` $\rightarrow$ *Sigo andando trabajando.*


## 10. PragmÃ¡tica de CortesÃ­a y Registros de Solicitud

AskÃ¡ro formaliza un modelo multicapa de cortesÃ­a pragmÃ¡tica que permite modular el grado de deferencia y formalidad en peticiones, mandatos y solicitudes sin romper el determinismo sintÃ¡ctico:

| Nivel / Registro | Formulario de CortesÃ­a | Tipo / Origen | Ejemplo CanÃ³nico en AskÃ¡ro | TraducciÃ³n Exacta |
| :---: | :--- | :--- | :--- | :--- |
| **Informal / RÃ¡pido** | **`prÃ³`** | PrÃ©stamo latino directo | `DÃ¡ Mo Ã¡kvÃ´m, prÃ³.` / `PrÃ³, dÃ¡ Mo Ã¡kvÃ´m.` | *Dame agua, por favor.* / *Por favor, dame agua.* |
| **EstÃ¡ndar** | **`pro favÃ³ro`** | Romance | `DÃ¡ Mo Ã¡kvÃ´m, pro favÃ³ro.` | *Dame agua, por favor.* |
| **Formal** | **`si To plÃ¡se`** | ExpresiÃ³n condicional | `Si To plÃ¡se, dÃ¡ Mo Ã¡kvÃ´m.` | *Si te place, dame agua.* |
| **CortÃ©s / Modal** | **`Â¿PÅt To...?`** | Interrogativo modal | `Â¿PÅt To dÃ¡r Mo Ã¡kvÃ´m?` | *Â¿PodrÃ­as / puedes darme agua?* |
| **Muy Formal / Ruego**| **`Mo rogÃ¡r To`** | PerÃ­frasis de ruego | `Mo rogÃ¡r To, dÃ¡ Mo Ã¡kvÃ´m.` | *Te ruego, dame agua.* |

### Principios de la PragmÃ¡tica en AskÃ¡ro:
1. **Riqueza de Registros**: Coexisten 5 estrategias pragmÃ¡ticas desde el diÃ¡logo cotidiano/rÃ¡pido (`prÃ³`) hasta el protocolo formal (`Mo rogÃ¡r To`).
2. **PreservaciÃ³n del Parsing**: Ninguna de las partÃ­culas de cortesÃ­a interfiere con la evaluaciÃ³n en $O(1)$ de los argumentos nominales ni con el colapso de la pila preverbal.
3. **Flexibilidad Posicional de `prÃ³`**: La partÃ­cula breve `prÃ³` puede ubicarse como prefijo adverbial inicial (`PrÃ³, dÃ¡ Mo...`) o como sufijo exclamativo de cierre (`...dÃ¡ Mo Ã¡kvÃ´m, prÃ³.`), actuando como un modulador de tono directo.

---

## 11. MÃ³dulo de PragmÃ¡tica, FÃ³rmulas de CortesÃ­a y Saludos (`PragmÃ¡-SistÃ©mo`)

| EspaÃ±ol | AskÃ¡ro | Prosodia / Estructura | Regla / EtimologÃ­a |
| :--- | :---: | :--- | :--- |
| **Hola** | **`SalÃ³`** | Aguda (`sa-lÃ³`) | LatÃ­n *salus*. |
| **AdiÃ³s** | **`CÃ¡o`** | Llana (`cÃ¡-o`) | Italiano *ciao* (`c` = `/tÊƒ/`). |
| **Por favor** | **`pro`** / **`pro favÃ³ro`** | MonosÃ­labo / Frase | ExpresiÃ³n de cortesÃ­a. |
| **Gracias** | **`GrÃ¡tis`** | Llana (`grÃ¡-tis`) | LatÃ­n *gratias*. |
| **De nada** | **`De nÃ­lo`** | Frase (`de nÃ­-lo`) | Lit. "De nada / De cero". |
| **PerdÃ³n** | **`PÃ¡rdon`** | Llana (`pÃ¡r-don`) | LatÃ­n *pardonare*. |
| **SÃ­** | **`Sik`** | MonosÃ­labo fÃ¡ctico | ConfirmaciÃ³n (1). |
| **No** | **`Nok`** | MonosÃ­labo fÃ¡ctico | NegaciÃ³n (0). |

---

## 12. MÃ³dulo CromÃ¡tico y Ãlgebra de Mezclas (`KrÃ³mo-SistÃ©mo`)

### 12.1 Colores Primarios, Secundarios y Extremos
* **Primarios:** **`rÃ³jo`** (Rojo), **`blÃ¡o`** (Azul), **`flÃ¡vo`** (Amarillo).
* **Extremos:** **`Ã¡lbo`** (Blanco), **`nÃ©gro`** (Negro).
* **Secundarios / Derivados:** **`vÃ­rdo`** (Verde = *blao-flavo*), **`narÃ¡njo`** (Naranja = *rojo-flavo*), **`purpÃºro`** (PÃºrpura = *rojo-blao*), **`pÃ­nko`** (Rosa), **`grÃ­so`** (Gris), **`kÃ¡fe`** (MarrÃ³n/CafÃ©).

---

## 13. MÃ³dulo de Parentesco, DimensiÃ³n Afectiva y FisiologÃ­a Neonatal (`SÃ³m-SistÃ©mo`)

### 13.1 Ãrbol de Parentesco y Registros
* **Padre / Madre / Hijo / Hija / Hermano / Hermana:** **`pÃ¡tro`**, **`mÃ¡tra`**, **`fÃ­lo`**, **`fÃ­la`**, **`frÃ¡tro`**, **`sorÃ³ro`**.
* **HipocorÃ­sticos e Infantil:** **`pÃ¡po`** (PapÃ¡), **`mÃ¡mo`** (MamÃ¡), **`nÃ¡no`** / **`nÃ¡na`** (Nene/Nena).

### 13.2 FisiologÃ­a VocÃ¡lica Neonatal (Capa 0) y Par Transparente
* **Reflejos VocÃ¡licos Primarios:** `Ã¡` (Incomodidad), `Ã©` (Hambre), `Ã³` (SueÃ±o), `ou` (Gases), `Ã­` (Dolor), `Ãº` (FrÃ­o/Inseguridad).
* **Par CanÃ³nico Padre-BebÃ©:**
  * **`au`** $\rightarrow$ **`Ã¡uxo`** / **`auxÃ­lio`** (Llamado de socorro).
  * **`ea`** $\rightarrow$ **`eaflÃ­ko`** (Malestar / AflicciÃ³n).
* **Necesidades BÃ¡sicas:** **`Ã¡famo`** (Hambre / Apetito fisiolÃ³gico).

---

## 14. MÃ³dulo de Tiempo, Calendario e Instrumentos (`KrÃ³no-SistÃ©mo`)

### 14.1 Iso-Calendario de 13 Lunas de 28 DÃ­as (`LÃºno-SistÃ©mo`)
* **Lunas (Meses):** **`LÃºno Un`**, **`LÃºno Du`**, **`LÃºno Tri`**, ..., **`LÃºno Dec-Tri`** (13 meses regulares de 28 dÃ­as = 364 dÃ­as).
* **DÃ­a de Fin de AÃ±o:** **`Ãnno-DÃ­a`** (DÃ­a fuera del tiempo / intercalar).
* **DÃ­as de la Semana:** **`DÃ­a Un`** (Lunes), **`DÃ­a Du`** (Martes), **`DÃ­a Tri`** (MiÃ©rcoles), **`DÃ­a KÃºa`** (Jueves), **`DÃ­a Kin`** (Viernes), **`DÃ­a Seks`** (SÃ¡bado), **`DÃ­a SÃ©pte`** (Domingo).
* **DesambiguaciÃ³n:** **`Ã¡nno`** (aÃ±o astronÃ³mico/calendÃ¡rico) vs. **`anÃºso`** (ano / anatomÃ­a).

### 14.2 Expresiones Horarias y Partes del DÃ­a (`Ã“ra-SistÃ©mo`)
* **Â¿QuÃ© hora es?:** *Â¿KÃ© Ã³ra es?*
* **Son las 3:** *Es Ã³ra tri.*
* **Son las 3 y cuarto:** *Es Ã³ra tri et minÃºto ten kin.*
* **Son las 3 y media:** *Es Ã³ra tri et minÃºto tri ten.*
* **Son las 4 menos cuarto:** *Es Ã³ra kÃºa min minÃºto ten kin.*
* **A las 3 / En una hora / Hace dos horas:** *A Ã³ra tri* / *En un Ã³ra* / *Ante du Ã³ras*.
* **Partes del DÃ­a:** **`matutÃ­no`** (0:00-6:00), **`matÃ­no`** (6:00-12:00), **`medidÃ­e`** (12:00), **`postmedidÃ­e`** (12:00-18:00), **`vespÃ©ro`** (18:00-0:00), **`medinÃ³kto`** (0:00).
* **Instrumentos Horarios:** **`orolÃ³gio`** (reloj), **`kronÃ³metro`** (cronÃ³metro), **`orÃ¡rio`** (manecilla de horas), **`minutÃ¡rio`** (manecilla de minutos), **`sekundÃ¡rio`** (segundero).

---

## 15. MÃ³dulo GeodÃ©sico, Puntos Cardinales y Coordenadas (`Geo-SistÃ©mo`)

### 15.1 BrÃºjula, Prefijos y Regiones GeopolÃ­ticas
* **Sustantivos Cardinales y Prefijos:**
  * **Norte:** **`nÃ³rto`** (prefijo **`nor-`**)
  * **Sur:** **`sÃºrto`** (prefijo **`sur-`**)
  * **Este:** **`Ã©sto`** (prefijo **`es-`**)
  * **Oeste:** **`oÃ©sto`** (prefijo **`os-`**)
  * Compuestos: **`nor-Ã©sto`** (NE), **`sur-oÃ©sto`** (SO).
* **Doble Capa Regional/AstronÃ³mica:**
  * **`oriÃ©nto`**: Oriente / Saliente (nacimiento del sol).
  * **`oksidÃ©nto`**: Occidente / Poniente (ocaso del sol - ajuste fonotÃ¡ctico `ks`).
  * **`septentriÃ³no`** (Norte formal), **`meridiÃ³no`** (Sur formal).
* **Coordenadas:** **`latitÃºdo`**, **`longitÃºdo`**, **`altitÃºdo`**, **`equatÃ³ro`**, **`hemisfÃ©ro`**.

---

## 16. MÃ³dulo de MetrologÃ­a CientÃ­fica, SI y Magnitudes (`Phys-SistÃ©mo`)

### 16.1 Las 7 Unidades Base del SI
`mÃ©tro` (m), `kilogrÃ¡mo` (kg), `sekÃºndo` (s), `ampÃ©rio` (A), `kÃ©lvo` (K), `mÃ³lo` (mol), `kandÃ©lo` (cd).

### 16.2 Unidades Derivadas del SI con Nombre Propio
`hÃ©rto` (Hz), `niÃºto` (N), `paskÃ¡l` (Pa), `iÃºlo` (J), `vÃ¡to` (W), `kÃºlombo` (C), `vÃ³lto` (V), `fÃ¡rado` (F), `Ã³mo` (Î©), `siÃ©menso` (S), `vÃ©bero` (Wb), `tÃ©slo` (T), `Ã©nrio` (H), `lÃºmeno` (lm), `lÃºkso` (lx), `bekerÃ©lo` (Bq), `grÃ¡o` (Gy), `sivÃ©rto` (Sv), `kÃ¡talo` (kat).

### 16.3 Prefijos Multiplicadores y Fraccionarios del SI
`dÃ©ka-` ($10^1$), `Ã©kto-` ($10^2$), `kÃ­lo-` ($10^3$), `mÃ©ga-` ($10^6$), `gÃ­ga-` ($10^9$), `tÃ©ra-` ($10^{12}$), `pÃ©ta-` ($10^{15}$), `Ã©ksa-` ($10^{18}$), `dÃ©si-` ($10^{-1}$), `sÃ©nti-` ($10^{-2}$), `mÃ­li-` ($10^{-3}$), `mÃ­kro-` ($10^{-6}$), `nÃ¡no-` ($10^{-9}$), `pÃ­ko-` ($10^{-12}$), `fÃ©mto-` ($10^{-15}$), `Ã¡to-` ($10^{-18}$).

### 16.4 Magnitudes FÃ­sicas y Operador de RazÃ³n `per`
`longitÃºdo`, `mÃ¡so`, `tiÃ©mpo`, `korriÃ©nto`, `temperatÃºro`, `kantidÃ¡`, `intensidÃ¡`, `velosidÃ¡` (`mÃ©tro per sekÃºndo`), `akelerasiÃ³n` (`mÃ©tro per sekÃºndoÂ²`), `fÃ³rso` (`niÃºto`), `enÃ©rgio` (`iÃºlo`), `potÃ©nsio` (`vÃ¡to`), `presiÃ³no` (`paskÃ¡l`), `frekÃ©nsio` (`hÃ©rto`), `kÃ¡rgo` (`kÃºlombo`), `densidÃ¡` (`kilogrÃ¡mo per mÃ©troÂ³`), `volÃºmo` (`mÃ©troÂ³`).

---

## 17. MÃ³dulo EconÃ³mico, Monetario y Financiero (`EkonÃ³mo-SistÃ©mo`)

### 17.1 Matriz de Sustantivos EconÃ³micos Canonizados
| Concepto (EspaÃ±ol) | TÃ©rmino Formal (AskÃ¡ro) | Regla / Ajuste MorfosintÃ¡ctico | EtiologÃ­a / LÃ³gica |
| :--- | :---: | :--- | :--- |
| **Dinero** | **`dinÃ©ro`** | Neutro Base en `-o` | LatÃ­n *denarius* / Romance. |
| **Moneda / Divisa** | **`monÃ©do`** | Ajuste `-a` $\rightarrow$ **`-o`** | LatÃ­n *moneta*. |
| **Precio** | **`prÃ©tio`** | ConservaciÃ³n etimolÃ³gica | LatÃ­n *pretium* (evita la africada `c` `/tÊƒ/`). |
| **Costo / Coste** | **`kÃ³sto`** | OrtografÃ­a con `k` | AdaptaciÃ³n fonotÃ¡ctica. |
| **Valor** | **`valÃ³ro`** | Desinencia neutra **`-o`** | LatÃ­n *valor*. |
| **Tasa / Ãndice** | **`tÃ¡so`** | Ajuste `-a` $\rightarrow$ **`-o`** | LatÃ­n *taxa*. |
| **Empresa / CompaÃ±Ã­a** | **`emprÃ©so`** | Ajuste `-a` $\rightarrow$ **`-o`** | Ital./Esp. *impresa/empresa*. |
| **Deuda** | **`dÃ©bito`** | RaÃ­z neolatina pura | LatÃ­n *debitum*. |
| **CrÃ©dito** | **`krÃ©dito`** | OrtografÃ­a con `k` | LatÃ­n *creditum*. |
| **Pago** | **`pÃ¡go`** | Neutro Base en `-o` | Romance *pago*. |
| **Ganancia / Lucro** | **`ganÃ¡nsio`** | Ajuste `-a` $\rightarrow$ **`-o`** | Romance / LatÃ­n *lucrum*. |
| **PÃ©rdida** | **`pÃ©rdido`** | Ajuste `-a` $\rightarrow$ **`-o`** | LatÃ­n *perditum*. |
| **Mercado** | **`merkÃ¡do`** | OrtografÃ­a con `k` | LatÃ­n *mercatus*. |
| **Comercio** | **`komÃ©rsio`** | SustituciÃ³n de `c` por `s` | LatÃ­n *commercium*. |
| **TransacciÃ³n** | **`transaksiÃ³n`** | TerminaciÃ³n nominal `-iÃ³n` | LatÃ­n *transactio*. |
| **Contrato** | **`kontrÃ¡to`** | OrtografÃ­a con `k` | LatÃ­n *contractus*. |
| **Factura** | **`faktÃºro`** | Ajuste `-a` $\rightarrow$ **`-o`** | LatÃ­n *factura*. |
| **Recibo** | **`resÃ­bo`** | Neutro Base en `-o` | Romance *recibo*. |

### 17.2 Verbos Transaccionales y Operadores del Mercado
| AcciÃ³n | Verbo CanÃ³nico (AskÃ¡ro) | Estructura de Envoltura |
| :--- | :---: | :--- |
| **Comprar** | **`askkomprÃ¡r`** | `ask-` + `kompr-` + `-Ã¡r` |
| **Vender** | **`askvendÃ©r`** | `ask-` + `vend-` + `-Ã©r` |
| **Pagar** | **`askpagÃ¡r`** | `ask-` + `pag-` + `-Ã¡r` |
| **Cobrar** | **`askkobrÃ¡r`** | `ask-` + `kobr-` + `-Ã¡r` |
| **Deber** | **`askdebÃ©r`** | `ask-` + `deb-` + `-Ã©r` |
| **Prestar** | **`askprestÃ¡r`** | `ask-` + `prest-` + `-Ã¡r` |
| **Ahorrar** | **`askahorrÃ¡r`** | `ask-` + `ahorr-` + `-Ã¡r` |
| **Gastar** | **`askgastÃ¡r`** | `ask-` + `gast-` + `-Ã¡r` |
| **Ganar** | **`askganÃ¡r`** | `ask-` + `gan-` + `-Ã¡r` |
| **Perder** | **`askperdÃ©r`** | `ask-` + `perd-` + `-Ã©r` |
| **Valer** | **`askvalÃ©r`** | `ask-` + `val-` + `-Ã©r` |
| **Costar** | **`askkostÃ¡r`** | `ask-` + `kost-` + `-Ã¡r` |
| **Invertir** | **`askinvestÃ­r`** | `ask-` + `invest-` + `-Ã­r` |

### 17.3 Ejemplos SintÃ¡cticos Transaccionales
1. **`La emprÃ©so prÄ“s askpagÃ¡r la dÃ©bitom.`** *(La empresa paga la deuda).*
2. **`Ko prÄ“s askvendÃ©r la dÃ³mom pro prÃ©tio Ã¡lto.`** *(Ã‰l vende la casa por un precio alto).*
3. **`Mo prÄ“s askkobrÃ¡r kin monÃ©dos.`** *(CobrÃ© cinco monedas).*
4. **`Ko prÄ“s askdebÃ©r mil monÃ©dos.`** *(Ã‰l debe mil monedas).*
5. **`Mos prÄ“s askahorrÃ¡r du sen monÃ©dos.`** *(Ahorramos doscientas monedas).*

---

## 18. MÃ³dulo de Pro-Formas y SustituciÃ³n Adjetival (`Pro-SistÃ©mo`)

### 18.1 CanonizaciÃ³n de `tÃ¡l` como Pro-Adjetivo Universal
* **DefiniciÃ³n:** `tÃ¡l` es el pro-adjetivo universal que sustituye a un adjetivo o atributo previamente mencionado en la clÃ¡usula.
* **Prosodia:** MonosÃ­labo invariable (`tÃ¡l`).

#### Ejemplos SintÃ¡cticos:
* *La kÃ¡rto es bÃ³na, et la dÃ¡tom es tÃ¡l.* (La carta es buena, y el dato es tal).
* *La sistÃ©mo es rÃ¡vel, et la servÃ³ro es tÃ¡l.* (El sistema es rÃ¡pido, y el servidor es tal).
* *La dÃ³mo es grÃ¡ndo, et la kÃ¡rto es tÃ¡l.* (La casa es grande, y la carta es tal).

### 18.2 Derivaciones de la Familia de `tÃ¡l`
| Forma | FunciÃ³n / Significado | Ejemplo SintÃ¡ctico |
| :--- | :--- | :--- |
| **`tÃ¡l`** | tal / asÃ­ (pro-adjetivo) | *La tÃ¡l kÃ¡rto.* |
| **`tÃ¡lik`** | de tal tipo (adjetival relacional) | *Un kÃ³so tÃ¡lik.* |
| **`tÃ¡liko`** | tal cosa (sustantivo neutro abstracto) | *Mo no askvidÃ©r tÃ¡likom.* |
| **`tÃ¡lim`** | de tal modo (adverbial modal) | *Ko askfakÃ¡r tÃ¡lim.* |

### 18.3 Matriz Unificada del Sistema de Pro-Formas de AskÃ¡ro
| Pro-forma | Entidad que Sustituye | Forma CanÃ³nica (AskÃ¡ro) | Ejemplo SintÃ¡ctico |
| :--- | :--- | :---: | :--- |
| **Pronombre** | Sustantivo / Entidad | **`Ãlo`** / **`Eo`** | *Mo askvisÃ¡r Ã­lom.* |
| **Pro-verbo** | Verbo / NÃºcleo de acciÃ³n | **`fak`** / **`obr`** | *Ko askfakÃ¡r fak.* |
| **Pro-adjetivo** | Adjetivo / Atributo | **`tÃ¡l`** | *La dÃ¡tom es tÃ¡l.* |
| **Pro-adverbio** | Adverbio / Circunstancia | **`hÃ­cim`** / **`tÃ¡lim`** | *Mo askfakÃ¡r hÃ­cim.* |
| **Pro-agente** | Agente indeterminado | **`On`** | *On askdÃ­r ke...* |
| **ComodÃ­n Nominal** | Objeto / Cosa genÃ©rica | **`kÃ³so`** | *DÃ¡ Mo kÃ³som.* |
| **ComodÃ­n Verbal** | AcciÃ³n genÃ©rica | **`askobrÃ¡r`** | *Mo askobrÃ¡r.* |


## 19. Alineamiento Ergativo y Sistema HÃ­brido de Doble Capa (Macro-Foco + Micro-Ergativo)

### 19.1 El Alineamiento Ergativo-Absolutivo Solo (MorfologÃ­a de Argumentos Micro)
En AskÃ¡ro V10.4, el sistema de casos nominales incluye el modo **Ergativo-Absolutivo**, alternativo o complementario al sistema nominativo-acusativo tradicional:

1. **Caso Absolutivo (Forma Base Neutra `-o` / `-a`):**
   - Se utiliza para el sujeto de verbos intransitivos (*"La grÃ¡ndo rÃ­o prÅ asksekÃ¡r"*).
   - Se utiliza para el objeto paciente de verbos transitivos (*"La cÃ©rvo la kasadÃ³ro-og prÄ“s askkÃ¡sar"*).
   - **EconomÃ­a:** El paciente no requiere desinencia nasal acusativa (`-om`), permaneciendo en la forma base limpia.

2. **Caso Ergativo (Sufijo `-og`):**
   - Reservado exclusivamente para el agente activo que ejecuta una acciÃ³n transitiva sobre un paciente (*"La kasadÃ³ro-og"*).

### 19.2 El Alineamiento de Enfoque Solo (PragmÃ¡tica Austronesia y Pila Preverbal Macro)
En este modo, los argumentos nominales permanecen en su forma base neutra (`-o`), y la **Pila Preverbal** actÃºa como el marco cinematogrÃ¡fico y de asignaciÃ³n de roles mediante los operadores con macrÃ³n:
- **`sÅ«`**: Foco Sujeto / Agente.
- **`pÄc`**: Foco Paciente / Objeto afectado.
- **`lÅk`**: Foco Locativo / Escenario.
- **`Ä«ns`**: Foco Instrumental / Herramienta.
- **`bÄ“n`**: Foco Beneficiario.
- **`dÄ«r`**: Evidencia Directa presencial.

### 19.3 La CombinaciÃ³n HÃ­brida: Pila Macro-Foco + MarcaciÃ³n Micro (Invarianza $O(1)$)
La mayor innovaciÃ³n arquitectÃ³nica de AskÃ¡ro V10.4 ocurre al acoplar la **Pila Macro** (Perspectiva cinematogrÃ¡fica de la clÃ¡usula) con la **MarcaciÃ³n Micro** (prefijos `ag-`, `pac-`, `inst-`, `lok-` o sufijo `-og` en el sustantivo):

1. **SeparaciÃ³n de Responsabilidades:**
   - **Nivel Micro (Sustantivos):** Garantiza la verdad proposicional pura ("quiÃ©n es quÃ©").
   - **Nivel Macro (Pila Preverbal):** Establece el *zoom*, la focalizaciÃ³n y el Ã¡ngulo de cÃ¡mara de la escena mental.
2. **Invarianza y Orden Totalmente Libre (*Free Word Order*):**
   Cualquier permutaciÃ³n de los argumentos dentro del enunciado mantiene exactamente la misma validez lÃ³gica sin requerir *lookahead*:
   - `lÅk dÄ«r prÄ“ askkÃ¡sar ag-kasadÃ³ro inst-radÃ¡ro pac-cÃ©rvo en la bÃ³sko.`
   - `pac-cÃ©rvo inst-radÃ¡ro ag-kasadÃ³ro PÄc dÄ«r prÄ“ askkÃ¡sar.`
   - `inst-radÃ¡ro ag-kasadÃ³ro pac-cÃ©rvo Äªns dÄ«r prÄ“ askkÃ¡sar.`

3. **DiferenciaciÃ³n de Pronombres TÃ³nicos y PartÃ­culas (SostÃ©n de MacrÃ³n):**
   Para evitar colisiones entre preposiciones/negaciones monosilÃ¡bicas y pronombres tÃ³nicos, se estandariza el macrÃ³n/circunflejo en pronombres:
   - **`MÅ`** / **`MÃ´`** (*yo*), **`TÅ`** / **`TÃ´`** (*tÃº*), **`KÅ`** / **`KÃ´`** (*Ã©l*), **`KÄ`** / **`KÃ¢`** (*ella*), **`NÅ`** / **`NÃ´`** (*nosotros*), **`SÅ`** / **`SÃ´`** (*vosotros*).
   - Permite expresiones como **`to TÅ`** (*hacia ti*) y **`no NÅ`** (*no nosotros*) sin ambigÃ¼edad alguna.
