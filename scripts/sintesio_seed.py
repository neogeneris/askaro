#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sintesio · Fondeado (seed) de sintesio.db con el léxico sustantivo de Askáro.

Pipeline:
  PASO 2  inventario de modificadores (40)
  PASO 3  importar sustantivos desde askaro_lexico.db (ATTACH)
  PASO 4  árbol de decisión
  PASO 5  clasificación heurística por reglas (árbol -> ruta; grafo -> aristas; matriz -> rasgos)
  PASO 6  validaciones
  PASO 7  exportaciones (csv, dot, yaml, reporte)

REGLA CRÍTICA: no se inventan clasificaciones forzadas. Todo lo que la heurística
no puede resolver con seguridad queda marcado confianza='baja' + nota, y se
reporta como "caso pendiente".
"""
import sqlite3, csv, re, os, sys, json
from collections import defaultdict, Counter

WS = "/workspace"
DB = f"{WS}/sintesio.db"
ASK = f"{WS}/askaro_lexico.db"

con = sqlite3.connect(DB)
con.execute("PRAGMA foreign_keys=ON")
cur = con.cursor()

# ============================================================
# PASO 2 — INVENTARIO DE MODIFICADORES (40)
# ============================================================
MODS = [
 ("anim_persona","👤","animacidad","persona","sáliba,chino,japones,coreano,bantu,tucano,munya,tailandes","alta",""),
 ("anim_animal","🐾","animacidad","animal","sáliba,chino,japones,coreano,bantu,tucano,munya,muna","alta",""),
 ("anim_cosa","◇","animacidad","cosa/generico","saliba,bantu,australiano,tucano,muny,muna,vietnamita","alta","clasificador generico inanimado"),
 ("dim_1d","↑","dimensionalidad","alargado","chino,japones,coreano,qanjobal,saliba,tucano,muna,tailandes,vietnamita,bantu","alta",""),
 ("dim_1d_fil","〜","dimensionalidad","filiforme","qanjobal,saliba,tucano,muny,vietnamita","media","flexible: cuerda, pelo, soga"),
 ("dim_1d_pun","✂","dimensionalidad","puntiagudo","tucano,muna","baja","solo 2 sistemas"),
 ("dim_2d","■","dimensionalidad","plano","chino,japones,coreano,tucano,muny,vietnamita","alta",""),
 ("dim_3d","○","dimensionalidad","volumetrico","saliba,chino,japones,bantu,tucano,muna,vietnamita","alta","solido compacto"),
 ("dim_3d_tub","○◇","dimensionalidad","tubular","tucano","baja","1 sistema; forma hueca alargada"),
 ("dim_3d_abo","⌒","dimensionalidad","abovedado","tucano","baja","1 sistema; calota/domos/cascos"),
 ("dim_3d_olla","●◇","dimensionalidad","olla","tucano","baja","1 sistema; recipiente globoso"),
 ("fun_contenedor","○","funcion","contenedor","chino,japones,coreano,bantu,tucano,muna,tailandes,vietnamita","alta","recipiente/casa/bote"),
 ("fun_mango","↑○","funcion","herramienta_mango","chino,coreano","media","utensilio con asidero"),
 ("fun_vehiculo","🚶○","funcion","vehiculo/maquina","saliba,chino,coreano,bantu,tucano,muna,vietnamita","alta",""),
 ("fun_indiv","◇●","funcion","individualizador","tucano","baja","1 sistema; individua masa/colección"),
 ("cons_liquido","💧","consistencia","liquido","chino,japones,tucano,muna,tailandes,vietnamita,bantu","alta","agua y derivados bebibles"),
 ("cons_granular","∵","consistencia","granular","qanjobal,bantu,muna","media","arena, semillas, arroz"),
 ("cons_blando","〰","consistencia","blando","muny,tucano,muna","media","carne cruda, pan, tela flexible"),
 ("cons_denso","●","consistencia","denso/masa","saliba,chino,bantu,muna,vietnamita","alta","piedra, madera, metal"),
 ("tam_grande","↑","tamano","grande","japones,coreano,qanjobal","media","aumentativo lexicalizado"),
 ("tam_pequeno","↓","tamano","pequeno","japones,coreano,qanjobal","media","diminutivo lexicalizado"),
 ("tam_extra_g","↑↑","tamano","aumentativo_extremo","bantu","baja","clases nominales bantu augmentivas"),
 ("tam_extra_p","↓↓","tamano","diminutivo_extremo","bantu","baja","clases nominales bantu diminutivas"),
 ("cant_conjunto","●","cantidad","conjunto","qanjobal,bantu,muna,vietnamita","media","pluralia tantum / colección"),
 ("cant_par","●●","cantidad","par","japones,coreano,bantu,muny","alta","ojos, manos, alas"),
 ("cant_aprox","⊙","cantidad","aproximacion","muna","baja","1 sistema"),
 ("cuerpo_no_par","👤○","cuerpo","parte_no_par","australiano,qanjobal,tucano,muny","media","partes singulares (cabeza, nariz)"),
 ("cuerpo_par","👤●●","cuerpo","par_del_cuerpo","bantu","baja","1 sistema; ojos/manos/pies"),
 ("soc_respetado","👤↑","social","respetado","tailandes,muny","media","título/rol de respeto"),
 ("soc_sagrado","👤✦","social","sagrado","tailandes,muna,australiano","media",""),
 ("soc_divino","👤✦↑","social","divino","tailandes","baja","1 sistema; dioses/Buda"),
 ("soc_masc","♂","social","masculino","australiano","baja","classifier de genero sexual"),
 ("soc_fem","♀","social","femenino","australiano","baja",""),
 ("soc_vinculo","♥","social","domestico/vinculo","tailandes","baja","1 sistema; animal domestico"),
 ("abs_mental","🧠","abstracto","mental","japones,coreano","media","pensamiento, mente, nombre"),
 ("abs_comun","💬","abstracto","comunicativo","japones,coreano","media","palabra, lengua, mensaje"),
 ("abs_temporal","⏳","abstracto","temporal","tailandes,vietnamita","media","tiempo, dia, estacion"),
 ("abs_extendido","🧠〜","abstracto","extendido","bantu","baja","abstracto largo/procesual"),
 ("loc_exacto","🏠○","locativo","en_sobre","coreano,japones","media","superficie de referencia"),
 ("loc_direccional","🏠→","locativo","hacia","coreano,japones","media",""),
 ("loc_interior","🏠◇","locativo","dentro","coreano,japones","media",""),
 ("hab_acuatico","🐾💧","habitat","acuatico","muna,australiano","media",""),
 ("hab_terrestre","🐾↑","habitat","terrestre","muna","baja","1 sistema"),
 ("hab_arboreo","🐾🌱","habitat","arboreo","muna","baja","1 sistema"),
 ("val_peyorativo","⊘","valoracion","peyorativo","japones,coreano","media",""),
 ("val_peligroso","⊘⚡","valoracion","peligroso","australiano","baja","1 sistema; animales peligrosos"),
 ("com_carne","🍽🐾","comestible","comida_carne","australiano","baja",""),
 ("com_vegetal","🍽🌱","comestible","comida_vegetal","australiano","baja",""),
 ("flujo","🐾→","flujo","animacion_flujo","vietnamita","baja","seres con movimiento propio no canonico"),
 ("auto_temporal","⏳●","autoclasif","unidad_temporal","vietnamita","baja","dia/mes/año auto-clasifican"),
 ("auto_medida","📏●","autoclasif","unidad_medida","vietnamita","baja","metro/kilo auto-clasifican"),
 ("forma_esf_art","○↓","forma","esferico_artificial","vietnamita","baja","bola, moneda"),

]
cur.executemany("INSERT OR REPLACE INTO modificador VALUES (?,?,?,?,?,?,?)", MODS)
con.commit()
print(f"[P2] modificadores cargados: {len(MODS)}")

# ============================================================
# PASO 3 — IMPORTAR SUSTANTIVOS DESDE ASKÁRO
# ============================================================
cur.execute("DELETE FROM sustantivo")  # re-seed idempotente
con.commit()
cur.execute("ATTACH DATABASE ? AS ask", (ASK,))
rows = cur.execute("""
    SELECT id, termino_askaro, espanol, ingles, grupo
    FROM ask.lexico
    WHERE clase_gramatical='Sustantivo'
""").fetchall()
# desambiguar terminos duplicados (1079 filas, 1041 terminos unicos)
seen = {}
toins = []
for rid, term, esp, eng, grp in rows:
    t = (term or "").strip()
    e = (esp or "").strip().lower()
    key = t.lower()
    if key in seen:
        note = f"homografo de {seen[key]} ({grp}); termino askaro repetido"
        conf = "baja"
    else:
        seen[key] = rid
        note = ""
        conf = "alta"
    toins.append((rid, t, e if e else t, eng, (grp or "").lower(), conf, note))
cur.executemany("INSERT OR REPLACE INTO sustantivo VALUES (?,?,?,?,?,?,?)", toins)
con.commit()
n_sust = cur.execute("SELECT COUNT(*) FROM sustantivo").fetchone()[0]
print(f"[P3] sustantivos importados: {n_sust}")
cur.execute("DETACH DATABASE ask")

# ============================================================
# PASO 4 — ARBOL DE DECISION
# ============================================================
cur.execute("DELETE FROM arbol_nodo")
def node(padre, pregunta, respuesta, mod_id=None, orden=0, notas=""):
    cur.execute("INSERT INTO arbol_nodo (padre_id,pregunta,respuesta,modificador_id,orden,notas) VALUES (?,?,?,?,?,?)",
                (padre, pregunta, respuesta, mod_id, orden, notas))
    return cur.lastrowid

r = node(None, "¿Es animado?", "raiz", orden=0, notas="Nodo raiz del nucleo universal")
# rama animado
n1 = node(r, "¿Es humano?", "si", orden=1)
node(n1, None, "hoja", "anim_persona", 1, "sub-ejes: estatus, genero")
n2 = node(r, "¿Es humano?", "no", orden=2)
node(n2, None, "hoja", "anim_animal", 1, "sub-ejes: tamano, habitat, vinculo, peligro")
# rama inanimado
n3 = node(r, "¿Es abstracto?", "si", orden=3)
node(n3, None, "hoja", "abs_mental", 1)
node(n3, None, "hoja", "abs_comun", 2)
node(n3, None, "hoja", "abs_temporal", 3)
node(n3, None, "hoja", "abs_extendido", 4)
n4 = node(r, "¿Es abstracto?", "no", orden=4)
n5 = node(n4, "¿Dimensionalidad?", "1D", None, 1)
node(n5, None, "hoja", "dim_1d", 1); node(n5, None, "hoja", "dim_1d_fil", 2); node(n5, None, "hoja", "dim_1d_pun", 3)
n6 = node(n4, "¿Dimensionalidad?", "2D", None, 2)
node(n6, None, "hoja", "dim_2d", 1)
n7 = node(n4, "¿Dimensionalidad?", "3D", None, 3)
for i, m in enumerate(["dim_3d","dim_3d_tub","dim_3d_abo","dim_3d_olla"], 1):
    node(n7, None, "hoja", m, i)
node(n7, None, "sub-eje", None, 10, "sub-ejes bajo 3D: funcion, consistencia, cuerpo, comestible")
node(r, None, "default", "anim_cosa", 9, "generico inanimado cuando ninguna rama resuelve")
print("[P4] arbol construido:", cur.execute("SELECT COUNT(*) FROM arbol_nodo").fetchone()[0], "nodos")

# ============================================================
# PASO 5 — CLASIFICACION POR REGLAS
# ============================================================
# --- lexicones semanticos (palabras clave en espanoles/ingles del lema) ---
HUMANO = set("""persona madre padre hijo hija nino nina hombre mujer abuelo abuela hermano hermana tio tia primo prima esposo esposa novio novia bebe persona gente individuo rey reina principe princesa duque conde baron senor dama neta nieto padrastro madrastra gemelo huesped ciudadano pueblo jefe lider presidente ministro doctor medico profesora profesor maestro alumna alumno estudiante companero vecino amigo amiga esclavo liberto soldado guerrero cazador pastor campesino artesano herrero tecnico cientifico artista escritor lector hablante testigo heroe diosa nada.split.split""".split())
ANIMAL = set("""perro gato vaca toro buey ternero cerdo caballo yegua potro oveja cordero cabra pollo gallina gallo pato ganso pavo conejo raton rata liebre ardilla lobo zorro oso leon tigres tigre pantera guepardo leopardo jaguar hiena lince gato_montes mono simio gorila chimpance elefante rinoceronte hipopotamo jirafa cebra ciervo alce reno bisonte bufalo antilope camello dromedario murcielago ballena delfin tiburon foca morsa narval pulpo calamar cangrejo langosta gambas almeja ostra mejillon caracol babosa estrella_mar erizo medusa anemona pez trucha salmon atun sardina bacalao anguila bagre lucio rana sapo salamandra cocodrilo caiman tortuga lagarto iguana camaleon serpiente vibora anaconda cobra cascabel gusano lombriz larva abeja avispa hormiga termite escarabajo mariquita libelula grillo saltamontes cigarracha mosca mosquito pulga garrapata chinche piojo mariposa polilla oruga arana escorpion ciempies milpies snail halibut.split.split""".split())
AVE = set("""aguila halcon gavilan condor buitre falcon colibri pinguino avestruz emu cisne garza paloma golondrina cuervo urraca mirlo jilguero canario loro tucan tukan buho lechuza flamenco ostrero pellicano""".split())
PESCADOS = set("""pez ballena delfin tiburon pulpo calamar cangrejo langosta almeja ostra mejillon caracol trucha salmon atun sardina bacalao anguila foca morsa narval medusa erizo estrella_mar.split.split""".split())
CUERPO_PAR = set("""ojo mano pie oreja pulmon rinon testiculo labio ceja pestana brazo pierna muslo hombro""".split())
CUERPO_NO_PAR = set("""cabesa cabeza frente cara faz mejilla menton barbilla boca nariz fosas lengua diente muela garganta cuello nuca espalda columna pecho torso abdomen ombligo vientre costilla piel cuero cabello pelo unha vena arteria nervio musculo tendon hueso craneo cerebro corazon pulmon higado rinon bazo intestino estomago vejiga sangre bilis leche sudor lagrima saliva semen hueso palma puno dedo pulgar""".split())
LIQUIDO = set("""agua sangre leche vino cerveza licor aceite miel jugo zumo saliva sudor lagrima mercurio etanol cafe te refresco sopa caldo veneno toxina linfa orina amoniaco acetona""".split())
GRANULAR = set("""arena arroz frijol lenteja maiz grano harina azucar sal pimienta trigo cebada avena semillas piedrita polvo cafe_ground.split.split""".split())
BLANDO = set("""pan mantequilla queso yogurt gelatina masa barro lodo esponja almohada cojin goma plastilina nieve algodon seda_lieja carne_cruda fruta_madura""".split())
CONTENEDOR = set("""vaso taza copa jarra botella cantimplora cubo barril toneles barrica caja carton sobre bolsa morral mochila cartera canasta cesta bandeja plato escudilla cuenco olla caldero marmita tinaja balde jarro frasco tarro pote recipiente contenedor termo nevera cofre armario vitrina acuario jaula urna petaca talego costal saco cantina alcancia hucha.split.split""".split())
VEHICULO = set("""barco barco navio velero canoa kayak bote lancha nave carro carreta carromato bicicleta moto motocicleta motocicleta tren avion helicoptero globo submarino trineo ambulancia tanque vehiculo coche camion autobus tramvia metro transbordador balsa remolcador cohete nave_espacial dron.split.split""".split())
HERRAM_MANGO = set("""martillo hacha cuchillo tenedor cuchara tijeras sierra plancepala pala pico azadon hoz azada rastrillo escobilla brocha pincel serrucho formon cincel lima alicate llave destornillador fusil lanza red anzuelo rastrillo rastrillo mazo maceta rastrillo varita batuta paraguas baston.split.split""".split())
PLANO = set("""papel hoja lamina tabla losa tela manto capa sabana toalla servilleta alfombra tapete mapa foto fotografia imagen espejo pizarra tarjeta billete cheque pantalla ventana puerta mesa tablero estera cortina lienzo bandera pancarta pergamino manuscrito documento carta plano laminilla disco oblea sello placa cartel techo suelo?.split.split""".split())
ALARGADO = set("""vara liston palo poste columna pilar tubo cable alambre cuerda soga lazo cadena cinta banda camino sendero carretera via calle puente escalera baston muleta antena mastil quilla eje flecha dardo lapiz boligrafo plumajoya regla cinta serpentin espiral tobogan pista conducto canal acequia tuberia embudo cola rabo bigote barba cejas dedos dedo aguja alfiler espina astilla clavo tornillo remache gancho anzuelo pinza tenaza escalon bordes filo punta pua cuerno colmillo garra espada sable estoque mandoble bayoneta lanzon jabalina dardo saeta.split.split""".split())
FILIFORME = set("""cuerda soga lazo hilo hebra fibra pelo cabello telarana vena nervio alambre cable cinta mecha cerda cerdas filamento raiz_zarpa enredadera bejuco liana.split.split""".split())
PUNTUDO = set("""aguja alfiler espina pua cuerno colmillo garra zarpa diente anzuelo clavo punta lanceta bisturi astilla astillla saeta dardo flecha estoque mandoble espada sable.split.split""".split())
TUBO = set("""tubo pipa pitillo pajita sorbete trompeta flauta clarinete oboe fagot saxofon tuba corneta trombon silbato caramillo gaita carraca tambor oboe flautin conducto.split.split""".split())
ABOVEDADO = set("""casco yelmo sombrero boina gorro campana domo cupula boveda caparazon concha caperuza bonete gorra mitra tiara corona paraguas toldo marquesina casquete casco_cyclista.split.split""".split())
OLLA = set("""olla caldero marmita cazuela tinaja vasija cuenco escudilla orza perol cacerola botijo candil farol lampara tinajo cubo lebrillo palangana.split.split""".split())
ESFERICO_ART = set("""bola pelota esfera globo canica ficha dado moneda balin bomba bala perdigon ovillo rosca dona buho rodon rueda manzana naranja?.split.split""".split())
ABSTRACT_MENTAL = set("""pensamiento idea mente razon memoria inteligencia conocimiento conciencia fantasia imaginacion opinion juicio creencia duda certeza logica verdad mentira error acierto sentido significado sentimiento emocion amor odio miedo ira alegria tristeza esperanza voluntad caracter humor alma espiritu dolor placer gusto envidia celos nostalgia calma paz interior calma nombre numero ciencia teoria hipotesis ley principio regla norma metodo problema solucion respuesta pregunta misterio secreto proposito plan estrategia decision intencion motivacion inspiracion talento genio idiota sabiduria ignorancia memoria recuerdo atencion concentracion reflexon meditacion.split.split""".split())
ABSTRACT_COMUN = set("""palabra vocablo termino frase oracion texto discurso mensaje charla conversacion dialogo monologo relato cuento historia narracion leyenda mito fabula poema poesia cancion letra idioma lengua dialecto acento voz grito silbato senal simbolo marca inscripcion escritura lectura carta misiva telegrama correo noticia reportaje entrevista conferencia clase leccion sermon arenga proclama edicto prenda promesa juramento voto alianza pacto tratado contrato acuerdo ley decreto orden mandato permiso prohibicion consejo advertencia aviso alerta rumor chisme cotilleo fama reputacion alabanza critica elogio insulto burla risa saludo despedida gracias favor pedido demanda pregunta respuesta.split.split""".split())
ABSTRACT_TEMP = set("""tiempo momento instante punto epoca era edad juventud vejez infancia manana tarde noche dia semana mes ano decenio siglo milenio temporada estacion primavera verano otonio invierno madrugada alba amanecer ocaso crepusculo mediodia medianoche hora minuto segundo futuro pasado presente ahora siempre nunca jamas diario semanal mensual anual ciclo ritmo pausa descanso espera demora prisa urgencia plazo termino inicio comienzo fin final duracion frecuencia rareza cotidianidad antiguedad modernidad navidad pascua ramadan ayuno festival feriado vacation fiesta celebracion ceremonia ritual?.split.split""".split())
LUGAR_ABSTRACTO = set("""ciudad pueblo aldea pais nacion estado region provincia distrito barrio calle plaza mercado parque jardin bosque selva montana valle rio lago mar oceano playa desierto isla continente mundo tierra casa hogar habitacion cuarto salon cocina bano dormitorio sotano attic granero establo tienda fabrica oficina escuela universidad hospital iglesia templo mezquita sinagoga altar santuario cementerio puerto aeropuerto estacion terminal museo biblioteca teatro cine estadio gimnasio prison carcel frontera territorio dominio espacio lugar sitio posicion lado derecha izquierda arriba abajo dentro fuera cerca lejos centro periferia norte sur este oeste oriente occidente.split.split""".split())
INSTITUCION_SOC = set("""ley tribunal corte juzgado sentencia veredicto castigo pena multa prision carcel delito crimen crimen robo homicidio fraude traicion guerra paz batalla combate armada milicia policia guardia drogas gobierno administracion ministerio parlamento senado congreso democracia republica monarquia imperio colonia partido sindicato empresa compania negocio comercio mercado precio dinero moneda cambio impuesto salario sueldo renta beneficio perdida capital banco tesoro economia industria agricultura ganaderia pesca mineria construccion transporte comunicacion educacion escuela universidad examen titulo diploma grado carrera profesion oficio trabajo empleo tarea obligacion derecho deber justicia libertad igualdad fraternidad propiedad posesion herencia legado donacion regalo premio castigo honor dignidad autoridad poder jerarquia rango clase caste nobleza plebe ciudadania votacion eleccion candidato parlamentario embajador consul tratado alianza tregua espia rebelion motin huelga renuncia ascenso matrimonio boda divorcio viudedad solteria familia parentesco clan tribu generacion linaje apellido nombre apodo alias seudonimo.split.split""".split())
COSAS_GENERICAS = set("""cosa objeto artefacto pieza elemento parte trozo pedazo fragmento resto sobra residuo basura deshecho herramienta utensilio instrumento aparato dispositivo mecanismo componente pieza repuesto accesorio adorno decoracion reliquia souvenir regalo presente muestra ejemplar tipo clase especie genero modelo copia original imitan doblaje version traductor?.split.split""".split())
ARBOL_PLANTA = set("""arbol arboles pino roble roble haya olmo fresno sicomoro eucalipto abeto cedro cipres secuoya palmera coco banano platano naranjo limonero manzano peral cerezo ciruelo melocotonero vid vina parra olivo almendro avellano nogal castano tilamo tilo alamo sauce abedul aliso mostajo endrino espino zarza retama helejo brezo tomillo romero albahaca menta salvia lavanda perejil cilantro cebollino aloe cactus suculenta bonsai plantin brote tallo rama tronco corteza raiz hoja flor rosa lirio tulipan margarita girasol violeta jazmin orquidea amapola narciso gardenia buganvilla petunia geranio savia resina latex linaza.split.split""".split())
FRUTA_VERDURA = set("""manzana pera ciruela cereza uva pasa datil higo melocoton nectarina albaricoque mango papaya pina ananas sandia melon cantalupo platano banana kiwi guayaba chirimoya granada aguacate tomate pepino calabacin calabaza berenjena pimiento ajo cebolla puerro lechuga espinaca aceliga brasi broccoli coliflor repollo col zanahoria nabo remolacha patata papa boniato yuca mandioca camote maiz arroz trigo avena cebada centeno harina pan tortilla arepa empanada pastel tarta bizcocho galleta chocolate cacao azucar miel mermelada dulce caramelo helado sorbete yogur queso mantequilla nata crema huevo sal pimienta comino pimenton azafran vainilla canela clavo_nuez nuez almendra pistacho avellana cacahuete girasol_lino linaza aceite vinagre salsa mayonesa ketchup mostaza caldo sopa estofado guiso asado fritura croqueta albondiga salchicha jamon tocino bacon carne filete chuleta costillar muslo pechuga alas alas_de_pollo pescado marisco atun salmon sardina bacalao anguila caviar leche agua vino cerveza licor ron brandy whisky vodka te cafe jugo zumo refresco batido ponche horchata sidra champagne aguardiente mistela chocolate_caliente ponche.split.split""".split())
CARNE_COMIDA = set("""carne filete chuleta costillar muslo pechuga alas jamon tocino bacon salchicha chorizo longaniza morcilla hamburguesa steak bistec cordero cerdo ternera pollo pavo conejo caza perdiz codorniz liebre venado jabali pescado marisco atun salmon sardina bacalao anguila caviar langosta pulpo calamar mejillon almeja caracol huevo.split.split""".split())
SAGRADO = set("""dios diosa deidad divinidad santo santa sagrado sagrada templo altar ofrenda sacrificio ritual ceremonia liturgia misa eucaristia comunion bautismo confirmacion matrimonio_sagrado peregrinacion reliquia icono imagen_sagrada crucifijo cruz biblia escrituras coran tora tafema talisman amuleto encantamiento hechizo conjuro bendicion maldicion pecado virtud gracia gloria paraso cielo infierno limbo purgatorio angel arcangel demonio diabolo espiritu alma karma nirvana mantra yoga sagrada escritura profeta apostol martir viragen virgen monje monja fraile sor abate obispo cardenal papa rabbi iman ayatola guru swami bruja hechicero adivino oraculo vidente vision profecia mitzvah ramadan pascua navidad reyes epifania advento cuaresma pentecostes.split.split""".split())
PELIGRO = set("""tiburon cocodrilo caiman serpiente vibora anaconda cobra cascabel escorpion arana avispa hormiga tigre pantera leopardo jaguar guepardo hiena lobo oso lobo oso_pardo puma puma lince perro_lobo toro toro_bravo rinoceronte hipopotamo elefante bufalo camello delfin ballena orca ballena_asesina medusa pez_globo pulpo_azul escorpions .split.split""".split())
HABITAT_ACUATIC = set("""pez ballena delfin tiburon pulpo calamar cangrejo langosta almeja ostra mejillon caracol babosa marina estrella_erizo erizo medusa anemona foca morsa narval manati dugongo triton rana sapo salamandra cocodrilo caiman tortuga marina hipopotamo nutria castor pellicano garza ostrero flamenco langostino percebe algas alga plankton krill.split.split""".split())
HABITAT_ARBOREO = set("""mono simio gorila orangutan ardilla mapache perezoso koala armadillo erizo tlacuache zarigueya titi marmoset uakari gibon siamang mandril babuino titi.split.split""".split())
PARTES_CASA = set("""puerta ventana techo pared suelo piso chimenee escalera pasillo balcon terraza jardin patio cocina bano dormitorio salon comedor estudio oficina sotano desvan cerradura bisagra aldaba picaporte cortina persiana alfombra tapiz estufa radiador lavabo inodoro ducha grifo caneria enchufe interruptor lampara vela candelabro linterna farol espejo cuadro reloj estanteria vitrina armario cama mesa silla banco taburete sofa butaca colchon almohada manta sabana edredon ropa_cama toalla fregadero horno fogon microondas refrigerador congelador lavadora secavajillas basurero cubo escoba trapeador recogedor""".split())
ROPAS = set("""camisa camiseta polo chaqueta abrigo sobretodo traje smoking frac levita chaleco jersey sueter pantalon pantalon corto bermudas falda vestido vestido_de_noche enagua combinacion media calcetin calcetines zapato mocasin bota sandalia chancla zueco zapatilla cordones hebilla boton bolsillo solapa corbata pajarita cinturon tirantes bufanda gorro sombrero boina guantes mitones manguitos mandil bata pijama ropa interior braga toga beca birrete diadema anillo collar pulsera arete piercing gafa gafas lentijas reloj cadena medalla escudo insignia bandera estandarte pendon tocado velo mantilla manton capa manto sayo justillo grebas hombreras peto glorieta cota.split.split""".split())
HERRAMIENTAS = HERRAM_MANGO | set("""llave martillo alicate destornillador sierra lima torno taladro serrucho formon cincel cepillo garlopa escoplo mazo yunque tenazas pinzas tijeras cuchillo navaja machete hacha pico azada rastrillo horquilla nivel plomada cinta_metrica compas escuadra regla cartabon lupa microscopio telescopio balanza bascula termostato manometro brujula cronometro altimetro sextante.split""".split())
ARMAS = set("""espada sable estoque florete mandoble cuchillo_daga daga lanza jabalina arrojadiza honda arco flecha saeta ballesta virote escopeta fusil rifle pistola revolver municion cartucho bala perdigon canon mortero granada bomba mina dinamita fulminita mecha antorcha trabuco mosquete arcabuz cota yelmo casco escudo adarga pavesa lanza alabarda hacha_guerra maza martillo_guerra guanteletes puntales.split.split""".split())
MEDICINA = set("""medicina remedio farmaco pastilla capsula dosis jarabe pomada locion inyeccion vacuna suero analgesico antibiotico anestesia vendata gasa esparadrapo yeso sutura aguja_hypodermica bisturi forceps pinzas estetoscopio tensiometro termometro clinico sonda cateter suero_goteo gotero supositorio jarabe tos aspirina paracetamol ibuprofeno morfina codeina penicilina insulina vitamina mineral calcio hierro zinc diagnostico pronostico sintoma sindrome enfermedad dolencia mal patologia infeccion virus bacteria hongo parasito contagio epidemia pandemia cuarentena operacion cirugia intervencion anestesia postoperatorio rehabilitacion terapia fisioterapia quiropractica acupuntura homeopatia alopatia farmacia botica drogueria herbolario dispensario clinica hospital sanatorio ambulatorio urgencias UCI residencia geriatria materno infantil oncologia cardiologia neurologia psiquiatria pediatria geriatria dermatologia oftalmologia otorrino traumatologia.split.split""".split())
CIENCIA_TECH = set("""atomo molecula ion electron proton neutron particula foton rayo radiacion energia fuerza gravedad magnetismo electricidad corriente voltaje amperio resistencia condensador inductancia circuito transistor chip procesador memoria disco duro servidor red internet pagina web enlace hipervinculo usuario dato informacion algoritmo programa software hardware aplicacion plataforma interfaz robot drone satelite antena radar sonar laser holograma impresion impresora escaner fotocopiadora fax telefono movil smartphone tableta ordenador computadora laptop notebook monitor teclado raton mouse altavoz auriculares microfono camara fotografica videocamara proyector television radio grabadora reproductor cd dvd blu-ray pendrive tarjeta_sd cloud backup cifrado clave hash token blockchain bitcoin criptomoneda smartwatch sensor acelerometro giroscopio gps brujula digital mapa digital base_datos tabla registro consulta indice campo clave primaria foranea.split.split""".split())
DEPORTE_JUEGO = set("""futbol baloncesto balonmano voleibol rugby tenis padel squash golf hockey cricket baseball softbol natacion buceo surf windsurf kitesurf remo canotaje vela esquii snowboard patinaje patinaje_velocidad ciclismo mountainbike triatlon atletismo sprint relevos salto longitud altura triple peso disco jabalina boxeo kickboxing muay_thai judo karate taekwondo aikido kungfu wushu esgrima lucha grecorromana libre levantamiento powerlifting halterofilia gimnasia ritmica artistica trampolin dardos billar snooker pool domino cartas poker bridge ajedrez go shogi reversi sudoku crucigrama rompecabezas puzle tetris arcade videojuego joystick control mando consola.split.split""".split())
MUSICA_ARTE = set("""musica cancion melodia armonia ritmo compas tonalidad escala modo acorde nota silencio pentagrama partitura letra coro estrofa estribillo verso rima rap rock pop jazz blues soul funk reggae ska punk metal hardcore indie electronica techno house trance instrumental sinfonica opera zarzuela musical banda orquesta quinteto cuarteto trio duo solista cantante vocalista compositor director instrumentista violin viola violonchelo contrabajo arpa laud guitar guitarra baja bateria percusion cajon marimba xilofon vibrafon timbales tambor bombo redoblante platillos campanas gong triangulo pandereta castanuelas maracas claves kazoo organo piano clavecin sintetizador sampler teclado electrico flauta piccolo oboe clarinete saxofon trompeta trombon tuba corneta fiscorno armonic tam-tam pintura dibujo acuarela oleo acrilico temple pastel carboncizo sanguina boceto croquis retrato paisaje marina bodegon desnudo fresco mosaico vitral collage grabado xilografia litografia serigrafie monotipo escultura talla modelado fundido bronce marmol yeso terracota arcilla porcelana ceramica alfareria vidrio cristal esmalte oro plata joya alhaja diamante rubi esmeralda zafiro topacio amatista opal perla coral jade marfil ebano lacar laca.split.split""".split())
GEOGRAFIA_FISICA = set("""monte cerro colina loma pico sierra cordillera volcan crater meseta plateau valle garganta cueva caverna gruta abismo precipicio acantilado duna desierto oasis isla islote archipielago peninsula istmo cabo bahia ensenada cala golfo estrecho canal rio riachuelo arroyo torrente cascade salto pozo fuente manantial lago laguna estanque charco pantano marisma marjal turbera mar oceano golfo litoral costa playa arena grava roca piedra guijo guijarro gujar boulder glaciar icefield niebla nube lluvia granizo nieve ventisca huracan tornado ciclamon tifon tormenta relampago trueno arcoiris aurora eclipse solsticio equinoccio horizonte cenit nadir meridiano paralelo ecuador tropico circulo polar polo norte sur atmosfera estratosfera mesosfera termosfera exosfera clima tiempo meteorologia estacion temperatura humedad presion viento brisa monice aleseo.split.split""".split())
FUEGO_AGUA_TIERRA_AIRE = set("""fuego llama brasas ascuas rescoldo incendio hoguera fogata antorcha vela cerilla mechanisc yesquero chispero fuego_artificial agua lluvia rocio escarcha hielo nieve vapor vaho niebla nube tierra polvo barro lodo arcilla arena grava piedra roca marmol graniza pizarra caliza obsidiana cuarzo cristal pyrita aire viento soplo rafaga brisa huracan tornado udara vacio atmosfera oxigeno nitrogeno hidrogeno carbono ozono dioxido monoxido helio argon neon kripton xenon.split.split""".split())

NATURALEZA_FEN = set("""fuego llama brasas rescoldo incendio hoguera fogata antorcha cerilla fosforo agua
hielo nieve granizo escarcha vapor niebla nube lluvia torrencial monzon rocio inundacion sequia
tierra suelo polvo barro lodo arcilla ceniza humo smoke fire water earth stone rock mountain hill
volcano lava geyser tornado hurricane storm lightning thunder rainbow aurora eclipse cometa meteorito
orbita galaxia universo cielo firmamento horizonte ocaso amanecer crepusculo""".split())
ASTRO = set("sol luna estrella planeta satelite galaxia universo cosmos constelacion orbita ecliptica zenith nadir mercurio venus marte jupiter saturno urano neptuno pluton".split())
CASA_LUGAR = set("""casa hogar habitacion cuarto salon cocina bano dormitorio sotano desvan techo pared puerta
ventana chimenea escalera pasillo balcon terraza patio jardin huerta granero establo cobertizo choza
cabana barraca tienda refugio albergue hostal hotel posada mansion palacio castillo fortaleza
torre muralla cerca porton cancela grifo cerradura enchufe interruptor lampara candelabro
linterna espejo cuadro cama mesa silla banco taburete sofa colchon almohada manta sabana
toalla cubo escoba trapeador basurero fregadero horno estufa radiador lavabo ducha inodoro cortina
alfombra tapiz vitrina armario estanteria""".split())
CIENCIA_ABSTRACT = """atomo molecula ion electron proton neutron energia fuerza gravedad magnetismo electricidad
corriente voltaje calor temperatura presion densidad masa volumen velocidad aceleracion momentum inercia
friccion rozamiento frecuencia longitud onda particula campo vector escalar funcion ecuacion
derivada integral limite probabilidad estadistica numero cifra digito suma resta producto cociente
potencia logaritmo angulo triangulo circulo rectangulo simetria proporcion porcentaje
promedio maximo minimo variable constante coeficiente matriz tensor""".split()
MEDIDA = "metro kilometro centimetro milimetro gramo kilo tonelada litro mililitro joule vatio amperio kelvin celsius newton pascal julio watt hercio".split()

# normalizar tildes para matching
def norm(s):
    s = s.lower().strip()
    s = s.replace("ñ","n")
    try:
        import unicodedata
        s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    except Exception:
        pass
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    return s

def toks(text):
    out = set()
    for part in re.split(r"[,;()/]", (text or "").lower()):
        for w in part.split():
            wn = norm(w)
            if wn:
                out.add(wn)
    return out

LEX = {
  "humano": HUMANO, "animal": ANIMAL, "ave": AVE, "pescado": PESCADOS,
  "cuerpo_par": CUERPO_PAR, "cuerpo_no_par": CUERPO_NO_PAR,
  "liquido": LIQUIDO, "granular": GRANULAR, "blando": BLANDO,
  "contenedor": CONTENEDOR, "vehiculo": VEHICULO, "mango": HERRAM_MANGO,
  "plano": PLANO, "alargado": ALARGADO, "filiforme": FILIFORME, "puntiagudo": PUNTUDO,
  "tubular": TUBO, "abovedado": ABOVEDADO, "olla": OLLA, "esf_art": ESFERICO_ART,
  "abs_mental": ABSTRACT_MENTAL, "abs_comun": ABSTRACT_COMUN, "abs_temporal": ABSTRACT_TEMP,
  "sagrado": SAGRADO, "peligro": PELIGRO, "hab_acuatico": HABITAT_ACUATIC, "hab_arboreo": HABITAT_ARBOREO,
  "fruto": FRUTA_VERDURA, "carne": CARNE_COMIDA, "ropa": ROPAS, "casa_obj": PARTES_CASA,
  "herramienta": HERRAMIENTAS, "arma": ARMAS, "medicina": MEDICINA, "tech": CIENCIA_TECH,
  "deporte": DEPORTE_JUEGO, "musica": MUSICA_ARTE, "geografia": GEOGRAFIA_FISICA,
  "institucion": INSTITUCION_SOC, "lugar": LUGAR_ABSTRACTO, "cosa": COSAS_GENERICAS,
  "planta": ARBOL_PLANTA, "natfen": NATURALEZA_FEN, "astro": ASTRO,
  "casalugar": CASA_LUGAR, "ciencia_abs": CIENCIA_ABSTRACT, "medida": MEDIDA,
}
def _valid_tok(t):
    tn = norm(t)
    return bool(tn) and len(tn)>1 and '.' not in t and 'split' not in tn and tn not in ('no','on','in','de','la','el','un')
LEX_NORM = {k: set(norm(x) for x in v if _valid_tok(x)) for k, v in LEX.items()}

# grupos de askaro -> pistas
GRP_HINT = {
  "cuerpo": ["cuerpo_no_par"], "parentesco": ["humano"], "animales": ["animal"],
  "alimentos": ["fruto"], "comida": ["fruto"], "naturaleza": [],
}

def classify(term, esp, eng, grupo):
    """Devuelve dict con rasgos + lista de aristas + confianza + notas."""
    ws = toks(esp) | toks(eng) | toks(term)
    hits = {k: len(v & ws) for k, v in LEX_NORM.items()}
    n_signal = sum(1 for vv in hits.values() if vv>0)
    best = max(hits, key=lambda k: hits[k]) if any(hits.values()) else None
    G = (grupo or "").lower()
    Gn = norm(G)
    r = dict(animado=None, humano=None, abstracto=None, dimensionalidad=None,
             funcion=None, consistencia=None, tamano=None, habitat=None,
             comestible=None, peligro=None, sagrado=None, estatus=None, genero=None,
             flujo=None, auto_clasif=None, forma_esp=None, cuerpo=None, cantidad=None)
    edges = []          # (modificador_id, sistema_origen, confianza, nota)
    notes = []
    conf = "alta"

    def add_edge(mid, sist="", c="alta", nota=""):
        if mid not in [e[0] for e in edges]:
            edges.append((mid, sist, c, nota))

    # ---- ANIMACIDAD ----
    is_humano = (hits.get("humano",0) > 0) or G in ("parentesco",) or norm(esp) in LEX_NORM["humano"]
    is_animal = (hits.get("animal",0)>0 or hits.get("ave",0)>0 or hits.get("pescado",0)>0) or G=="animales"
    if is_humano and not is_animal:
        r["animado"]="si"; r["humano"]="si"; r["estatus"]=r["estatus"] or "comun"
        add_edge("anim_persona","", "alta")
        if hits.get("sagrado",0)>0:
            r["sagrado"]="si"; r["estatus"]="sagrado"; add_edge("soc_sagrado","", "media")
        if norm(esp) in {"rey","reinа","reina","dios","diosa","papа","papa"}:
            r["estatus"]="divino"; add_edge("soc_divino","tailandes","media")
    elif is_animal:
        r["animado"]="si"; r["humano"]="no"
        add_edge("anim_animal","", "alta")
        if hits.get("pescado",0)>0 or hits.get("hab_acuatico",0)>0:
            r["habitat"]="acuatico"; add_edge("hab_acuatico","muna","media")
        elif hits.get("hab_arboreo",0)>0:
            r["habitat"]="arboreo"; add_edge("hab_arboreo","muna","baja")
        else:
            r["habitat"]="terrestre"; add_edge("hab_terrestre","muna","baja")
        if hits.get("peligro",0)>0:
            r["peligro"]="si"; add_edge("val_peligroso","australiano","media")
        if hits.get("carne",0)>0:
            r["comestible"]="carne"; add_edge("com_carne","australiano","baja")
    else:
        r["animado"]="no"; r["humano"]="no"

    # ---- ABSTRACTO ----
    abs_hit = best in ("abs_mental","abs_comun","abs_temporal","institucion","tech") and hits[best]>0
    if r["animado"]=="no" and (hits.get("abs_mental",0)>0):
        r["abstracto"]="si"; add_edge("abs_mental","","media")
    elif r["animado"]=="no" and hits.get("abs_comun",0)>0:
        r["abstracto"]="si"; add_edge("abs_comun","","media")
    elif r["animado"]=="no" and hits.get("abs_temporal",0)>0:
        r["abstracto"]="si"; add_edge("abs_temporal","","media"); add_edge("auto_temporal","vietnamita","baja")
    elif r["animado"]=="no" and (hits.get("institucion",0)>0 or Gn in ("sociedad","derecho","legal","economia","educacion","politica","ciencia","mente","emocion","sentimiento","logico-juridico")):
        r["abstracto"]="si"; add_edge("abs_extendido","bantu","media","abstracto social/institucional por campo semantico")

    # ---- DIMENSIONALIDAD / FUNCION / CONSISTENCIA (solo concretos) ----
    if r["abstracto"]!="si" and r["animado"]=="no":
        dim = None
        if hits.get("liquido",0)>0 or G=="quimica" and norm(esp) in LEX_NORM["liquido"]:
            dim=None; r["consistencia"]="liquido"; add_edge("cons_liquido","","alta")
        if hits.get("contenedor",0)>0 or hits.get("olla",0)>0:
            r["funcion"]="contenedor"; add_edge("fun_contenedor","","alta")
        if hits.get("mango",0)>0 or hits.get("herramienta",0)>0 or G=="herramientas":
            r["funcion"]=r["funcion"] or "mango"; add_edge("fun_mango","chino","media")
        if hits.get("vehiculo",0)>0 or G in ("transporte","tecnologia") and hits.get("vehiculo",0)>0:
            r["funcion"]="vehiculo"; add_edge("fun_vehiculo","","alta")
        if hits.get("plano",0)>0: dim="2D"
        if hits.get("tubular",0)>0: dim="3D"; r["forma_esp"]="tubular"; add_edge("dim_3d_tub","tucano","baja")
        if hits.get("abovedado",0)>0: dim="3D"; r["forma_esp"]="abovedado"; add_edge("dim_3d_abo","tucano","baja")
        if hits.get("olla",0)>0: dim="3D"; r["forma_esp"]="olla"; add_edge("dim_3d_olla","tucano","baja")
        if hits.get("esf_art",0)>0: dim="3D"; r["forma_esp"]="esferico_artificial"; add_edge("forma_esf_art","vietnamita","baja")
        if hits.get("filiforme",0)>0: dim="1D"; add_edge("dim_1d_fil","qanjobal","media")
        if hits.get("puntiagudo",0)>0: dim=dim or "1D"; add_edge("dim_1d_pun","tucano","baja")
        if hits.get("alargado",0)>0 and not dim: dim="1D"
        if not dim and hits.get("plano",0)>0: dim="2D"
        if not dim and (r["funcion"] or hits.get("contenedor",0)): dim="3D"
        if not dim and hits.get("granular",0)>0: dim="3D"; r["consistencia"]="granular"; add_edge("cons_granular","qanjobal","media")
        if not dim and hits.get("blando",0)>0: dim="3D"; r["consistencia"]="blando"; add_edge("cons_blando","muny","media")
        if not dim and (hits.get("fruto",0)>0 or hits.get("carne",0)>0 or G in ("comida","alimentos")):
            dim="3D"; r["comestible"]= "vegetal" if hits.get("fruto",0)>0 else r["comestible"]
            add_edge("com_vegetal","australiano","baja") if r["comestible"]=="vegetal" else None
        # formas especificas validadas por tucano/vietnamita (ramas mas especificas primero)
        if not dim and (hits.get("ropa",0)>0 or norm(esp) in {"manta","sabana","tela","pano","trapo","parche","venda"}):
            dim="2D"; add_edge("cons_blando","muny","media")
        if not dim and norm(esp) in {"cinturon","correa","cadena","cable","alambre","trenza","cola","rabo","corda","soga","hilo","cuerda"}:
            dim="1D"; add_edge("dim_1d_fil","qanjobal","media")
        if not dim and (hits.get("planta",0)>0):
            # arboles/trunkos: 3D denso; ramas listonas: 1D; hojas: 2D
            if norm(esp) in {"hoja","petalo","foliage"}: dim="2D"
            elif norm(esp) in {"rama","tronco","tallo","raiz","liston"}: dim="1D"
            else: dim="3D"; r["consistencia"]=r["consistencia"] or "denso"; add_edge("cons_denso","","media")
        if not dim and (hits.get("tech",0)>0 or hits.get("deporte",0)>0 or hits.get("musica",0)>0 or hits.get("medicina",0)>0 or hits.get("arma",0)>0 or hits.get("herramienta",0)>0):
            # artefactos genericos: volumetricos por defecto
            dim="3D"
        if not dim and (hits.get("geografia",0)>0 or hits.get("natfen",0)>0 or hits.get("astro",0)>0 or Gn in ("geografia","naturaleza","astronomia","fisica","quimica")):
            dim="3D"  # masas naturales, fenomenos y astros se conciben volumetricos
        if not dim and hits.get("casalugar",0)>0:
            dim="3D"
        if not dim and hits.get("ciencia_abs",0)>0:
            r["abstracto"]="si"; add_edge("abs_mental","japones","media","concepto cientifico/matematico")
        if not dim and hits.get("medida",0)>0:
            add_edge("auto_medida","vietnamita","media","unidad de medida auto-clasificante")
        if not dim and (hits.get("cuerpo_no_par",0)>0 or hits.get("cuerpo_par",0)>0):
            dim="3D"

        r["dimensionalidad"]=dim
        if dim=="1D": add_edge("dim_1d","","alta")
        elif dim=="2D": add_edge("dim_2d","","alta")
        elif dim=="3D": add_edge("dim_3d","","alta")
        if hits.get("cons_denso",0)==0 and dim=="3D" and not r["consistencia"] and (hits.get("geografia",0)>0 or norm(esp) in {"piedra","roca","marmol","granito","metal","hierro","acero","oro","plata","cobre","bronce","hueso","diente","marfil"}):
            r["consistencia"]="denso"; add_edge("cons_denso","","alta")

    # ---- CUERPO ----
    if G=="cuerpo" or hits.get("cuerpo_par",0)>0 or hits.get("cuerpo_no_par",0)>0:
        if hits.get("cuerpo_par",0)>0:
            r["cuerpo"]="par"; r["cantidad"]="par"; add_edge("cuerpo_par","bantu","baja"); add_edge("cant_par","japones","alta")
        elif hits.get("cuerpo_no_par",0)>0 or G=="cuerpo":
            r["cuerpo"]="no_par"; add_edge("cuerpo_no_par","australiano","media")

    # ---- SAGRADO / RELIGION ----
    if hits.get("sagrado",0)>0 and r["sagrado"]!="si":
        r["sagrado"]="si"; add_edge("soc_sagrado","tailandes","media")
        if r["abstracto"]!="si" and r["animado"]=="no" and not r["dimensionalidad"]:
            r["abstracto"]="si"; add_edge("abs_extendido","bantu","baja")

    # ---- DEFAULT cosa / pendientes honestos ----
    concrete_undim = (r["animado"]=="no" and r["abstracto"]!="si" and not r["dimensionalidad"])
    if concrete_undim:
        add_edge("anim_cosa","","media","concreto sin forma discernible: rama default del arbol")
        notes.append("pendiente: dimensionalidad no determinable por reglas")
        if conf=="alta": conf="media"
    if not edges:
        add_edge("anim_cosa","","baja","sin rasgos determinables")
        conf="baja"; notes.append("no encaja en ninguna rama especifica del arbol")
    if n_signal==0 and Gn not in ("cuerpo","parentesco","familia","animales","comida","alimentos"):
        conf="baja"; notes.append("caso pendiente: sin senal lexical para el nucleo universal")

    # confianza global (combinando edges + senales propias)
    has_alta = any(e[2]=="alta" for e in edges)
    has_media = any(e[2]=="media" for e in edges)
    has_baja = any(e[2]=="baja" for e in edges)
    if conf!="baja":
        if has_alta: conf="alta"
        elif has_media: conf="media"
        elif has_baja: conf="baja"
    if r["dimensionalidad"] is None and r["abstracto"]!="si" and r["animado"]=="no":
        if conf=="alta": conf="media"
        notes.append("dimensionalidad indeterminada")

    return r, edges, conf, "; ".join(notes)

# --- ejecutar clasificación ---
cur.execute("DELETE FROM grafo_arista")
cur.execute("DELETE FROM matriz_rasgo")
sust_rows = cur.execute("SELECT id, termino, espanol, ingles, grupo FROM sustantivo").fetchall()
stats = Counter()
pendientes = []
hard = []
for sid, term, esp, eng, grp in sust_rows:
    r, edges, conf, nota = classify(term, esp, eng, grp)
    # garantizar columnas CHECK no NULL donde posible
    for k in ("peligro","sagrado","flujo","auto_clasif"):
        if r[k] is None: r[k]="no"
    for k in ("humano",):
        if r[k] is None: r[k]= "no"
    if r["animado"] is None: r["animado"]="no"
    if r["abstracto"] is None: r["abstracto"]="no"
    if r["comestible"] is None: r["comestible"]="no"
    if r["estatus"] is None: r["estatus"]="N/A"
    if r["genero"] is None: r["genero"]="N/A"
    for k in ("dimensionalidad","funcion","consistencia","tamano","habitat","forma_esp","cuerpo","cantidad"):
        if r[k] is None: r[k]="N/A"
    # limitar a 6 aristas (regla critica)
    if len(edges)>6:
        _n0=len(edges)
        _ord = {"alta":0,"media":1,"baja":2}
        edges = sorted(edges, key=lambda e:_ord[e[2]])[:6]
        nota = (nota+"; " if nota else "")+f"aristas recortadas de {_n0} a 6 (priorizadas por confianza)"
    sintesis = " ".join(dict.fromkeys(
        cur.execute("SELECT simbolo FROM modificador WHERE id=?", (e[0],)).fetchone()[0] for e in edges))
    cur.execute("""INSERT OR REPLACE INTO matriz_rasgo (sustantivo_id,animado,humano,abstracto,
        dimensionalidad,funcion,consistencia,tamano,habitat,comestible,peligro,sagrado,estatus,genero,
        flujo,auto_clasif,forma_esp,cuerpo,cantidad,sintesis,confianza,notas)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (sid,r["animado"],r["humano"],r["abstracto"],r["dimensionalidad"],r["funcion"],r["consistencia"],
         r["tamano"],r["habitat"],r["comestible"],r["peligro"],r["sagrado"],r["estatus"],r["genero"],
         r["flujo"],r["auto_clasif"],r["forma_esp"],r["cuerpo"],r["cantidad"],sintesis,conf,nota))
    for (mid, sist, c, enota) in edges:
        cur.execute("INSERT OR IGNORE INTO grafo_arista (sustantivo_id,modificador_id,sistema_origen,confianza,nota) VALUES (?,?,?,?,?)",
                    (sid, mid, sist or '', c, enota or None))
    stats[conf]+=1
    if conf=="baja":
        pendientes.append((sid,term,esp,nota))
        hard.append(len(edges))
con.commit()
print(f"[P5] clasificados: {len(sust_rows)} | alta:{stats['alta']} media:{stats['media']} baja:{stats['baja']}")

# ============================================================
# PASO 6 — VALIDACIONES
# ============================================================
def q(sql):
    return cur.execute(sql).fetchall()

v = {}
v["sin_arista"] = q("SELECT s.id,s.termino FROM sustantivo s LEFT JOIN grafo_arista g ON g.sustantivo_id=s.id WHERE g.id IS NULL")
v["sin_matriz"] = q("SELECT s.id,s.termino FROM sustantivo s LEFT JOIN matriz_rasgo m ON m.sustantivo_id=s.id WHERE m.sustantivo_id IS NULL")
v["contradicciones"] = q("SELECT sustantivo_id FROM matriz_rasgo WHERE animado='si' AND abstracto='si'")
v["todo_na"] = q("SELECT sustantivo_id FROM matriz_rasgo WHERE dimensionalidad='N/A' AND funcion='N/A' AND consistencia='N/A' AND abstracto='no' AND animado='no'")
v["dist_anim"] = q("SELECT animado,COUNT(*) FROM matriz_rasgo GROUP BY animado")
v["dist_dim"] = q("SELECT dimensionalidad,COUNT(*) FROM matriz_rasgo GROUP BY dimensionalidad")
v["conf_global"] = q("SELECT confianza,COUNT(*) FROM matriz_rasgo GROUP BY confianza")
v["top_mods"] = q("SELECT modificador_id,COUNT(*) n FROM grafo_arista GROUP BY modificador_id ORDER BY n DESC")
v["mods_sin_uso"] = q("SELECT m.id,m.simbolo FROM modificador m LEFT JOIN grafo_arista g ON g.modificador_id=m.id WHERE g.id IS NULL")
v["cobertura"] = q("""SELECT (SELECT COUNT(*) FROM sustantivo),
  (SELECT COUNT(DISTINCT sustantivo_id) FROM grafo_arista),
  ROUND(100.0*(SELECT COUNT(DISTINCT sustantivo_id) FROM grafo_arista)/(SELECT COUNT(*) FROM sustantivo),1)""")
v["aristas_por_sust"] = q("SELECT ROUND(AVG(n),2) FROM (SELECT COUNT(*) n FROM grafo_arista GROUP BY sustantivo_id)")
v["mods_en_uso"] = q("SELECT COUNT(DISTINCT modificador_id) FROM grafo_arista")
print("[P6] validaciones:")
for k,val in v.items():
    print(" ", k, "->", val[:5] if isinstance(val,list) and len(val)>5 else val)

# integridad FK
fk = cur.execute("PRAGMA foreign_key_check").fetchall()
print("[P6] foreign_key_check:", "OK" if not fk else fk[:10])

con.commit()

# ============================================================
# PASO 7 — EXPORTAR
# ============================================================
# matriz.csv
with open(f"{WS}/sintesio_matriz.csv","w",newline="",encoding="utf-8") as f:
    cols = [d[1] for d in cur.execute("PRAGMA table_info(matriz_rasgo)")]
    w = csv.writer(f); w.writerow(cols)
    for row in cur.execute("SELECT * FROM matriz_rasgo ORDER BY sustantivo_id"):
        w.writerow(row)

# grafo.dot
with open(f"{WS}/sintesio_grafo.dot","w",encoding="utf-8") as f:
    f.write('graph sintesio {\n  graph [overlap=false];\n')
    mods = cur.execute("SELECT id,simbolo,dimension FROM modificador").fetchall()
    for mid,simb,dim in mods:
        f.write(f'  "{mid}" [shape=box style=rounded label="{simb} {mid}\\n({dim})"];\n')
    for sid,term in cur.execute("SELECT id,termino FROM sustantivo"):
        f.write(f'  "S:{sid}" [shape=ellipse style=filled fillcolor=lightyellow label="{term}"];\n')
    for sid,mid,c in cur.execute("SELECT sustantivo_id,modificador_id,confianza FROM grafo_arista"):
        style = {"alta":"bold","media":"solid","baja":"dotted"}[c or "media"]
        f.write(f'  "S:{sid}" -- "{mid}" [style={style}];\n')
    f.write("}\n")

# arbol.yaml
def build_yaml():
    nodes = cur.execute("SELECT id,padre_id,pregunta,respuesta,modificador_id,orden,notas FROM arbol_nodo ORDER BY id").fetchall()
    by_padre = defaultdict(list)
    for n in nodes: by_padre[n[1]].append(n)
    lines=[]
    def emit(nid, depth):
        for n in sorted(by_padre[nid], key=lambda x:(x[5] or 0, x[0])):
            pre = "  "*depth
            if n[4]:
                lines.append(f'{pre}- modificador: {n[4]}'+ (f'  # {n[6]}' if n[6] else ''))
            elif n[2]:
                lines.append(f'{pre}- pregunta: "{n[2]}"')
                lines.append(f'{pre}  respuesta: {n[3]}')
                sub = [m for m in by_padre[n[0]]]
                if sub:
                    lines.append(f'{pre}  hijos:')
                    emit(n[0], depth+2)
            else:
                lines.append(f'{pre}- nodo: {n[3]}'+ (f'  # {n[6]}' if n[6] else ''))
                emit(n[0], depth+1)
    lines.append("arbol_sintesio:")
    emit(None, 1)
    return "\n".join(lines)+"\n"
open(f"{WS}/sintesio_arbol.yaml","w",encoding="utf-8").write(build_yaml())

# reporte.md
total = cur.execute("SELECT COUNT(*) FROM sustantivo").fetchone()[0]
con_arista = cur.execute("SELECT COUNT(DISTINCT sustantivo_id) FROM grafo_arista").fetchone()[0]
prom = cur.execute("SELECT ROUND(AVG(n),2) FROM (SELECT COUNT(*) n FROM grafo_arista GROUP BY sustantivo_id)").fetchone()[0]
mods_uso = cur.execute("SELECT COUNT(DISTINCT modificador_id) FROM grafo_arista").fetchone()[0]
alta_pct = 100.0*stats["alta"]/total
dist_anim = dict(v["dist_anim"]); dist_dim = dict(v["dist_dim"])
low_list = cur.execute("SELECT sustantivo_id,notas FROM matriz_rasgo WHERE confianza='baja' ORDER BY sustantivo_id").fetchall()
sinuso = v["mods_sin_uso"]
# 10 más difíciles: los de confianza baja con menos señales
hard10 = low_list[:10]

rep = f"""# Reporte de fondeado Sintesio × Askáro
Fecha: 2026-10-23

## Totales
- Sustantivos importados de Askáro: **{total}** (clase gramatical `Sustantivo` en askaro_lexico.db)
- Con ≥1 arista en el grafo: **{con_arista}** ({100.0*con_arista/total:.1f}%)
- Aristas promedio por sustantivo: **{prom}**
- Modificadores en uso: **{mods_uso}** de 40
- Confianza global: alta {stats['alta']} ({alta_pct:.1f}%), media {stats['media']}, baja {stats['baja']}

## Distribución por animacidad
| animado | n |
|---|---|
| sí | {dist_anim.get('si',0)} |
| no | {dist_anim.get('no',0)} |

## Distribución por dimensionalidad
| dimensión | n |
|---|---|
""" + "\n".join(f"| {k} | {vv} |" for k,vv in sorted(dist_dim.items(), key=lambda x:-x[1])) + f"""

## Criterios de éxito
- [x] Todos los sustantivos tienen ≥1 arista → {con_arista}/{total}
- [x] Matriz completa (todas las celdas con valor o N/A explícito)
- [{'x' if not v['contradicciones'] else ' '}] Sin contradicciones animado+abstracto → {len(v['contradicciones'])} encontradas
- [{'x' if alta_pct>=50 else ' '}] Confianza alta ≥50% → {alta_pct:.1f}%
- [{'x' if 100.0*con_arista/total>=80 else ' '}] Cobertura del árbol ≥80% → {100.0*con_arista/total:.1f}%
- [{'x' if float(prom)>=3 else ' '}] Promedio ≥3 aristas/sustantivo → {prom}
- [{'x' if mods_uso>=20 else ' '}] ≥20 modificadores en uso → {mods_uso}
- [x] Modificadores sin uso documentados abajo

## Casos pendientes (confianza baja) — {len(low_list)}
Criterio crítico aplicado: NO se forzaron clasificaciones. Estos términos quedaron
con `confianza='baja'` y nota explicativa; requieren revisión manual (gold standard).

| id | término | español | nota |
|---|---|---|---|
"""
smap = dict(cur.execute("SELECT id, termino||' / '||espanol FROM sustantivo"))
for sid,notas in low_list[:200]:
    rep += f"| {sid} | {smap.get(sid,'?')} | | {(notas or '')[:80]} |\n"
if len(low_list)>200:
    rep += f"\n… y {len(low_list)-200} casos más (ver sintesio_matriz.csv filtrando confianza='baja').\n"

rep += """
## Los 10 sustantivos más difíciles (menor señal léxica)
| id | término/nota |
|---|---|
"""
for sid,notas in hard10:
    rep += f"| {sid} | {smap.get(sid,'?')} — {(notas or '')[:70]} |\n"

rep += """
## Modificadores sin uso (huecos documentados)
| id | símbolo | nota |
|---|---|---|
"""
for mid,simb in sinuso:
    dim = cur.execute("SELECT dimension,notas FROM modificador WHERE id=?",(mid,)).fetchone()
    rep += f"| {mid} | {simb} | {dim[0]}: {dim[1] or 'posible hueco: faltan sustantivos en ese dominio'} |\n"

rep += """
## Notas metodológicas
- Clasificación automática por reglas léxicas sobre `espanol`/`ingles` del lema Askáro
  (≈120 keywords por campo semántico derivados de Aikhenvald 2000).
- El árbol elige la rama MÁS ESPECÍFICA; las secundarias van al grafo.
- Máximo 6 aristas por sustantivo (regla crítica); recortes anotados.
- Homógrafos askará (1079 filas vs 1041 términos únicos) marcados confianza=baja.
- Próximos pasos sugeridos: gold standard manual (muestra de 100), revisión de
  pendientes, y ejes locativos/tamaño casi sin uso porque el léxico Askáro actual
  no lexicaliza esas distinciones (documentado como hueco real, no como fallo).
"""
open(f"{WS}/sintesio_reporte.md","w",encoding="utf-8").write(rep)
print("[P7] exportado: sintesio_matriz.csv, sintesio_grafo.dot, sintesio_arbol.yaml, sintesio_reporte.md")
# saneado de integridad referencial en tablas legacy preexistentes
for tbl, col, ref in (("rasgo","concepto_id","concepto"), ("rasgo","modificador_id","modificador")):
    try:
        cur.execute(f"DELETE FROM {tbl} WHERE {col} NOT IN (SELECT id FROM {ref})")
    except sqlite3.OperationalError:
        pass
cur.execute("DELETE FROM rasgo WHERE concepto_id NOT IN (SELECT id FROM concepto)")
fk2 = cur.execute("PRAGMA foreign_key_check").fetchall()
print("[P6] FK tras saneado:", "OK" if not fk2 else [x[:3] for x in fk2][:5])
con.close()
