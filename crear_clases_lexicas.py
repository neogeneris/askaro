#!/usr/bin/env python3
"""Crea y rellena las tablas `sustantivos` y `adjetivos` en lexico.db a partir de askaro_lexicon.

Clasificaciones:
- sustantivos: animado/inanimado, sexo_biologico (macho/hembra/comun), naturaleza (concreto/abstracto/material)
- adjetivos: tipo (fisico/psicologico/cualidad/deverbal)
- ambas: raiz + vocal_final separadas, origen_seleccion (latin/es/fr/it/pt/ro/ia/eo/neologismo/modelo),
  equivalentes romances + ia/eo/en, cognado si/no, icono UTF-8 UNIQUE (heredado de la fase-1 `lexico`, sin repetirse).

Idempotente: INSERT OR REPLACE. Estado por defecto 'propuesto' (revision humana); 'verificado' para animados.
"""
import sqlite3, unicodedata

DB = 'lexico.db'

def norm(s):
    s = unicodedata.normalize('NFD', (s or '').lower())
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').strip()

def desdiac(s):
    return (s.replace('â','a').replace('ê','e').replace('î','i').replace('ô','o').replace('û','u')
             .replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
             .replace('à','a').replace('è','e').replace('ì','i').replace('ò','o').replace('ù','u')
             .replace('ā','a').replace('ē','e').replace('ī','i').replace('ō','o').replace('ū','u'))

def raiz_vocal(forma):
    if not forma: return ('', '')
    f = forma.strip()
    vowels = 'aeiouáéíóúâêîôûāēīōūə'
    for i in range(len(f)-1, -1, -1):
        if f[i] in vowels:
            return (f[:i], f[i:])
    return (f[:-1], f[-1])

def origen_seleccion(forma, cols, etimo):
    """Determina de qué lengua proviene la forma canónica Askáro."""
    f = norm(forma); base = desdiac(f)
    for col, name in [('es','es'),('fr','fr'),('it','it'),('pt','pt'),('ro','ro'),('ia','ia'),('eo','eo')]:
        v = norm(cols.get(col))
        if v and (v == f or v == base): return name
    lat = norm((etimo or '').split('(')[0].strip())
    if lat and base[:4] and lat.startswith(base[:4]): return 'latin'
    return 'modelo'

# ---- listas semánticas (núcleo verificado manualmente; el resto es heurística propuesto) ----
ANIMADOS = set("""hombre mujer niño niña bebe padre madre hijo hija hermano hermana abuelo abuela primo tio tia sobrino
esposo esposa persona gente rey reina principe princesa duque conde baron presidente alcalde jefe lider medico dentista
profesor maestro alumno estudiante soldado policia ladron asesino amigo vecino huesped invitado esclavo servidor criado
actor cantante bailarin escritor poeta pintor artista musico cocinero panadero carnicero herrero albanil carpintero
sastre zapatero tejedor pastor granjero agricultor cazador pescero minero banquero comerciante mercader juez abogado
secretario monje monja sacerdote rabino iman dios diosa angel demonio fantasma espiritu perro gato vaca toro buey
ternero novilla caballo yegua potro asno mula cerdo cochino puerco cabra ovejo carnero cordero gallina gallo pollo pavo
pato ganso conejo liebre rata raton topo ardilla erizo ciervo venado alce bisonte elefante jirafa rinoceronte hipopotamo
leon tigre lobo zorro oso panda mono simio murcielago ballena delfin tiburon foca morsa pulpo calamar cangrejo langosta
camarao ostra almeja mejillon caracol babosa abeja avispa hormiga mosquito mosca pulga piojo gusano larva arana escorpion
serpiente lagarto cocodrilo tortuga rana sapo trucha salmon atun sardina bacalao pez ave pajaro aguilora halcon buho
cuervo paloma gorrion golondrina codorniz faisán flamenco avestruz pingüino cisne grulla cigueña pichon animal bestia
criatura bacteria virus microbio celula planta arbol pino abeto roble haya olmo fresno arce palmera vid parra manzano
peral naranjo limonero cerezo ciruelo melocotonero higuera almendro avellano nogal castano helecho cactus musgo liquen
seta hongo""".split())

MASC = set("hombre padre hijo hermano abuelo primo tio sobrino esposo rey principe duque conde baron presidente alcalde jefe medico profesor maestro alumno soldado ladron asesino actor escritor poeta pintor musico cocinero herrero carpintero sastre zapatero pastor granjero cazador minero banquero comerciante juez abogado secretario monje sacerdote rabino iman dios angel perro toro buey caballo asno cerdo gallo conejo liebre topo ardilla erizo ciervo alce bisonte elefante leon tigre lobo zorro oso mono murcielago delfin tiburon pulpo cangrejo camarao caracol escorpion gallo".split())
FEM = set("mujer madre hija hermana abuela prima tia sobrina esposa reina princesa duquesa condesa baronesa jefa medica profesora maestra alumna ladrona asesina actora escritora poetisa pintora cocinera pastora granjera cazadora minera banquera jueza abogada monja sacerdotisa imama diosa gata vaca yegua potran novilla cerda oveja gallina pava pata gansa liebre ratona ardilla cierva leona tigra loba zorra osa mona ballena delfina foca langosta ostra almeja tortuga rana sapo paloma golondrina codorniz avestruz cisne perra burra".split())

ABSTRACTOS = set("""amor odio alegria tristeza miedo ira envidia celos verguenza culpa pena dolor placer felicidad esperanza
desesperacion sorpresa curiosidad asombro respeto desprecio admiracion desconfianza fe duda certeza verdad mentira error
acierto justicia injusticia libertad igualdad fraternidad solidaridad bondad maldad mal bien belleza fealdad virtud vicio
valor cobardia prudencia temeridad sabiduria ignorancia inteligencia memoria atencion conciencia pensamiento idea concepto
nocion teoria hipotesis practica experimento axioma teorema ley principio regla norma orden caos poder autoridad soberania
gobierno estado nacion patria pueblo guerra paz conflicto victoria derrota estrategia tactica diplomacia politica derecho
deber obligacion responsabilidad delito crimen pena castigo juicio veredicto sentencia prueba testimonio acusacion defensa
opinion creencia dogma doctrina religion cultura civilizacion arte ciencia tecnologia tecnica habilidad talento genio
creatividad imaginacion fantasia sueno pesadilla vision ilusion apariencia realidad existencia vida muerte nacimiento
vejez juventud madurez salud enfermedad experiencia conocimiento aprendizaje conclusion premisa demostracion debate
discusion conversacion dialogo monologo significado sentido referencia contexto intencion motivacion proposito fin causa
efecto consecuencia resultado exito fracaso logro avance progreso decadencia evolucion revolucion cambio transformacion
estabilidad permanencia posibilidad imposibilidad necesidad contingencia azar suerte destino hado fortuna probabilidad
duda edad epoca era periodo etapa fase turno ocasion cantidad numero clase tipo genero especie categoria grupo serie
coleccion conjunto unidad multiplicidad totalidad parcialidad dualidad brevedad fugacidad eternidad infinitud
matrimonio divorcio viudez solteria virginidad inocencia parentesco alianza amistad enemistad precio costo valor riqueza
pobreza propiedad posesion herencia ganancia perdida beneficio perjuicio interes profesion oficio empleo labor esfuerzo
descanso ocio diversion tradicion costumbre ceremonia ritual rito mito legenda fabula parabola alegoria metafora
ortografia gramatica sintaxis semantica fonetica etimologia derivacion""".split())

MATERIALES = set("""madera palo tronco rama raiz corteza savia hoja flor fruto semilla grano cereal trigo arroz maiz avena
cebada centeno harina pan masa polvo sal azucar miel leche mantequilla yogurt huevo carne hueso piel cuero pluma escama
lana pelo fibra algodon lino seda tela tejido hilo cuerda soga red bolsa caja barril tonele cubo cesto papel carton tabla
liston viga pilar columna arco boveda muro pared techo piso suelo escalera puerta ventana cerradura llave clavo tornillo
cadena alambre cable tubo canal pozo fuente lluvia nieve granizo hielo vapor nube niebla viento aire atmosfera cielo
tierra arena arcilla barro piedra roca grava mineral oro plata cobre hierro acero estano plomo zinc mercurio azufre
carbon diamante rubi esmeralda zafiro jade cristal vidrio espejo lente lampara vela fuego ceniza brasa humo chispa luz
sombra agua aceite grasa cera jabon pintura tinta color pigmento barniz resina caucho plastico goma cemento cal yeso
ladrillo teja mosaico estatua imagen cuadro retrato escultura mascara disfraz uniforme ropa vestido camisa pantalon falda
abrigo capa sombrero gorra guantes bufanda zapatos bota sandalia calcetin medias boton anillo collar pulsera medalla
corona joya tesoro cofre arca baul maleta mochila herramienta martillo hacha sierra tenazas pinzas lima cincel azada pala
pico arado yugo rienda silla mesa banca sofa cama colchon almohada manta sabana cortina alfombra tapiz reloj campana
silbato trompeta tambor arpa lira flauta guitarra piano organo computador maquina motor rueda carro barco nave canoa
puente camino calle carretera plaza parque jardin pradera huerta granja establo tienda mercado almacen fabrica taller
escuela universidad biblioteca museo templo iglesia capilla castillo fortaleza torre muralla palacio habitacion salon
cocina bano sotano""".split())

ADJ_FIS = set("alto bajo largo corto ancho estrecho grueso fino grande pequeno pesado ligero rapido lento fuerte debil duro blando suave rugoso liso caliente frio templado humedo seco claro oscuro brillante opaco rojo azul verde amarillo negro blanco gris rosa cafe violeta naranja dulce amargo salado acido agrio picante sano enfermo viejo nuevo joven bonito feo limpio sucio lleno vacio abierto cerrado cerca lejos hondo superficial gordo flaco ciego sordo mudo zurdo diestro rubio moreno canoso rizado delgado alto bajo ancho angosto pelon lampino".split())
ADJ_PSQ = set("feliz triste alegre contento disgustado enojado furioso tranquilo nervioso ansioso valiente cobarde timido inteligente tonto sabio necio educado grosero generoso avaro prudente honesto fiel traidor leal amable cruel tierno brusco delicado rudo simpatico orgulloso humilde modesto vanidoso celoso envidioso perezoso diligente aplicado descuidado cuidadoso responsable confiable discreto sincero mentiroso optimista pesimista distraido atento cansado hambriento sediento satisfecho aburrido ocupado libre".split())

def clasifica_sust(es, forma):
    e = norm(es)
    anim, sexo = 'inanimado', None
    if e in ANIMADOS:
        anim = 'animado'
        sexo = 'macho' if e in MASC else ('hembra' if e in FEM else 'comun')
    if e in ABSTRACTOS: nat = 'abstracto'
    elif e in MATERIALES: nat = 'material'
    elif anim == 'animado': nat = 'concreto'
    else:
        f = desdiac(norm(forma))
        if any(f.endswith(x) for x in ['cion','tion','dad','tad','ment','anza','encia','ancia','ura','ez','cie','ismo']):
            nat = 'abstracto'
        else:
            nat = 'concreto'
    return anim, sexo, nat

def clasifica_adj(es, forma):
    e = norm(es); f = desdiac(norm(forma))
    if e in ADJ_FIS: return 'fisico'
    if e in ADJ_PSQ: return 'psicologico'
    if any(f.endswith(x) for x in ['ble','nte','roso','ose','ile']): return 'deverbal'
    return 'cualidad'

DDL = """
CREATE TABLE IF NOT EXISTS sustantivos (
  id INTEGER PRIMARY KEY REFERENCES askaro_lexicon(id),
  codigo TEXT UNIQUE,
  forma TEXT, termino_propuesto TEXT,
  es TEXT, en TEXT, fr TEXT, it TEXT, pt TEXT, ro TEXT, ia TEXT, eo TEXT, latin_vulgar TEXT,
  origen_etimologia TEXT,
  origen_seleccion TEXT CHECK(origen_seleccion IN ('latin','es','fr','it','pt','ro','ia','eo','neologismo','modelo')),
  raiz TEXT, vocal_final TEXT,
  animado TEXT CHECK(animado IN ('animado','inanimado')),
  sexo_biologico TEXT CHECK(sexo_biologico IN ('macho','hembra','comun')),
  naturaleza TEXT CHECK(naturaleza IN ('concreto','abstracto','material')),
  icono TEXT UNIQUE,
  cognado TEXT CHECK(cognado IN ('si','no')),
  estado_clasificacion TEXT DEFAULT 'propuesto'
);
CREATE TABLE IF NOT EXISTS adjetivos (
  id INTEGER PRIMARY KEY REFERENCES askaro_lexicon(id),
  codigo TEXT UNIQUE,
  forma TEXT, termino_propuesto TEXT,
  es TEXT, en TEXT, fr TEXT, it TEXT, pt TEXT, ro TEXT, ia TEXT, eo TEXT, latin_vulgar TEXT,
  origen_etimologia TEXT,
  origen_seleccion TEXT,
  raiz TEXT, vocal_final TEXT,
  tipo TEXT CHECK(tipo IN ('fisico','psicologico','cualidad','deverbal')),
  cognado TEXT CHECK(cognado IN ('si','no')),
  estado_clasificacion TEXT DEFAULT 'propuesto'
);
"""

def main():
    con = sqlite3.connect(DB); cur = con.cursor()
    cur.executescript(DDL)
    # mapa emoji fase-1 (unicos por constraint)
    fase1 = {}
    for r in cur.execute("SELECT DISTINCT concepto_es, es, emoji FROM lexico"):
        fase1.setdefault(norm(r[1] or r[0]), r[2])
    usados = set()
    rows = cur.execute("""SELECT id,codigo,forma,termino_propuesto,español,ingles,fr,it,pt,ro,ia,eo,latin_vulgar,origen_etimologia,categoria
                          FROM askaro_lexicon WHERE categoria IN ('Sustantivo','Adjetivo') ORDER BY id""").fetchall()
    ns = na = nic = 0
    for r in rows:
        (sid,cod,forma,prop,es,en,fr,it,pt,ro,ia,eo,lv,etimo,cat) = r
        cols = dict(es=es,en=en,fr=fr,it=it,pt=pt,ro=ro,ia=ia,eo=eo)
        osel = origen_seleccion(forma or prop, cols, etimo)
        rz,vf = raiz_vocal(forma or prop)
        cog = 'si' if any([fr,it,pt,ro,ia,eo]) else 'no'
        if cat == 'Sustantivo':
            anim,sexo,nat = clasifica_sust(es, forma)
            ic = fase1.get(norm(es))
            if ic and ic not in usados: usados.add(ic); nic += 1
            else: ic = None
            est = 'verificado' if anim=='animado' else 'propuesto'
            cur.execute("INSERT OR REPLACE INTO sustantivos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (sid,cod,forma,prop,es,en,fr,it,pt,ro,ia,eo,lv,etimo,osel,rz,vf,anim,sexo,nat,ic,cog,est)); ns += 1
        else:
            tip = clasifica_adj(es, forma)
            cur.execute("INSERT OR REPLACE INTO adjetivos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (sid,cod,forma,prop,es,en,fr,it,pt,ro,ia,eo,lv,etimo,osel,rz,vf,tip,cog,'propuesto')); na += 1
    con.commit()
    print(f"sustantivos={ns} adjetivos={na} iconos_unicos={nic}")
    print("integrity:", cur.execute("PRAGMA integrity_check").fetchone()[0])

if __name__ == '__main__':
    main()
