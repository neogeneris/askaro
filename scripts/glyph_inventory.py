#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventario real de emojis Unicode 15.x vs glifos ya procesados.
Salida: /workspace/data/glyph_candidates.json + resumen por dominio."""
import sqlite3, unicodedata, json, re, os

RANGES=[(0x231A,0x231B),(0x23E9,0x23FA),(0x24C2,0x24C2),(0x25AA,0x25AB),(0x25B6,0x25B6),(0x25C0,0x25C0),
(0x25FB,0x25FE),(0x2601,0x2604),(0x260E,0x260E),(0x2611,0x2611),(0x2614,0x2615),(0x2618,0x2618),(0x261D,0x261D),
(0x2620,0x2620),(0x2622,0x2623),(0x2625,0x2625),(0x2627,0x2627),(0x262A,0x262A),(0x262E,0x262F),(0x2638,0x263A),
(0x2640,0x2640),(0x2642,0x2642),(0x2648,0x2653),(0x265F,0x2660),(0x2663,0x2663),(0x2665,0x2666),(0x2668,0x2668),
(0x267B,0x267B),(0x267E,0x267F),(0x2692,0x2697),(0x2699,0x2699),(0x269B,0x269C),(0x26A0,0x26A0),(0x26A7,0x26A7),
(0x26AA,0x26AB),(0x26B0,0x26B1),(0x26BD,0x26BE),(0x26C4,0x26C5),(0x26C8,0x26C8),(0x26CE,0x26CE),(0x26CF,0x26CF),
(0x26D1,0x26D1),(0x26D3,0x26D4),(0x26E9,0x26EA),(0x26F0,0x26F5),(0x26F7,0x26FA),(0x26FD,0x26FD),(0x2702,0x2702),
(0x2705,0x2705),(0x2708,0x2709),(0x270C,0x270D),(0x270F,0x270F),(0x2712,0x2712),(0x2714,0x2714),(0x2716,0x2716),
(0x271D,0x271D),(0x2721,0x2721),(0x2728,0x2728),(0x2733,0x2734),(0x2744,0x2744),(0x2747,0x2747),(0x274C,0x274C),
(0x274E,0x274E),(0x2753,0x2755),(0x2757,0x2757),(0x2763,0x2764),(0x2795,0x2797),(0x27A1,0x27A1),(0x27B0,0x27B0),
(0x27BF,0x27BF),(0x2B1B,0x2B1C),(0x2B50,0x2B50),(0x2B55,0x2B55),(0x1F004,0x1F004),(0x1F0CF,0x1F0CF),
(0x1F170,0x1F171),(0x1F17E,0x1F17F),(0x1F18E,0x1F18E),(0x1F191,0x1F19A),(0x1F201,0x1F202),(0x1F21A,0x1F21A),
(0x1F22F,0x1F22F),(0x1F232,0x1F23A),(0x1F250,0x1F251),(0x1F300,0x1F321),(0x1F324,0x1F393),(0x1F396,0x1F397),
(0x1F399,0x1F3DB),(0x1F3DE,0x1F3FE),(0x1F400,0x1F4FC),(0x1F4FF,0x1F53D),(0x1F549,0x1F54E),(0x1F550,0x1F567),
(0x1F56F,0x1F570),(0x1F573,0x1F57A),(0x1F587,0x1F587),(0x1F58A,0x1F58D),(0x1F590,0x1F590),(0x1F595,0x1F596),
(0x1F5A4,0x1F5A4),(0x1F5FB,0x1F64F),(0x1F680,0x1F6C5),(0x1F6CB,0x1F6D2),(0x1F6D5,0x1F6D7),(0x1F6DC,0x1F6DF),
(0x1F6EB,0x1F6EC),(0x1F6F4,0x1F6FC),(0x1F7F0,0x1F7F0),(0x1F90C,0x1F93A),(0x1F93C,0x1F945),(0x1F947,0x1F9FF),
(0x1FA70,0x1FA74),(0x1FA78,0x1FA7C),(0x1FA80,0x1FA86),(0x1FA88,0x1FA8F),(0x1FA90,0x1FAAC),(0x1FAB0,0x1FABA),
(0x1FAC0,0x1FAC5),(0x1FACC,0x1FACC),(0x1FACE,0x1FADB),(0x1FAE0,0x1FAE7),(0x1FAE9,0x1FAE9),(0x1FAF0,0x1FAF6)]

def emoji_names():
    out=[]
    for lo,hi in RANGES:
        for cp in range(lo,hi+1):
            try: out.append((cp,unicodedata.name(chr(cp))))
            except ValueError: pass
    return out

SKIP=['FACE','SMILING','GRINNING','ANGRY','TEAR','THUMB','CLAP','HANDSHAKE','KISS','ARROW','BUTTON',
'SHAPE','SQUARE','CIRCLE','TRIANGLE','DIAMOND','HEART DECORATION','KEYCAP','INPUT','REGIONAL','FLAG','MAP',
'MOON SYMBOL','EXCLAMATION','QUESTION','HEART','COIN','CARD','CHESS','MAHJONG','BACK','END','SOON','TOP',
'ON','OFF','UP','DOWN','NO ENTRY','PROHIBITED','WARNING']

EN_ES={
 'watch':'reloj','spaghetti':'espagueti','rugby football':'rugby','label':'etiqueta',
 'lady beetle':'mariquita','womans hat':'sombrero','older man':'anciano',
 'personal computer':'computadora','scroll':'pergamino','hole':'agujero','high-speed train':'tren bala',
 'door':'puerta','avocado':'aguacate','sari':'sari','swan':'cisne','onion':'cebolla',
 'stethoscope':'estetoscopio','hourglass with flowing sand':'reloj de arena','ladder':'escalera',
 'hook':'gancho','ring buoy':'boya','candle':'vela','running shirt':'camiseta',
 'adhesive bandage':'tirita','firecracker':'petardo','gas cylinder':'bombona','wing':'ala',
 'musical note':'nota musical','microphone':'micrófono','headphone':'auricular','radio':'radio',
 'television':'televisor','camera':'cámara','battery':'pila','electric plug':'enchufe',
 'floppy disk':'disquete','desktop computer':'ordenador','printer':'impresora','scanner':'escáner',
 'calendar':'calendario','file folder':'carpeta','clipboard':'portapapeles','pushpin':'chincheta',
 'paperclip':'clip','straight ruler':'regla','triangular ruler':'escuadra','pen':'bolígrafo',
 'fountain pen':'pluma','paintbrush':'pincel','crayon':'crayón','books':'libro','open book':'libro',
 'green book':'cuaderno','notebook':'cuaderno','ledger':'registro','page with curl':'hoja',
 'newspaper':'periódico','bookmark tabs':'marcapáginas','moneybag':'zurrón','yen banknote':'billete',
 'credit card':'tarjeta','gem stone':'gema','ring':'anillo','necktie':'corbata','shirt':'camisa',
 'jeans':'vaqueros','kimono':'kimono','handbag':'bolso','purse':'monedero','backpack':'mochila',
 'socks':'calcetín','glove':'guante','scarf':'bufanda','coat':'abrigo','dress':'vestido',
 'bikini':'biquini','lab coat':'bata','campus':'campus','school':'escuela',
 'department store':'grandes almacenes','factory':'fábrica','japanese castle':'castillo',
 'tokyo tower':'torre','statue of liberty':'estatua','church':'iglesia','mosque':'mezquita',
 'synagogue':'sinagoga','kaaba':'kaaba','fountain':'fuente','tent':'tienda','hut':'choza',
 'house':'casa','desert island':'isla','national park':'parque','stadium':'estadio',
 'classical building':'edificio','derelict house':'casa abandonada','post office':'correos',
 'hospital':'hospital','bank':'banco','hotel':'hotel','convenience store':'tienda','pharmacy':'farmacia',
 'atm':'cajero','police car':'coche patrulla','ambulance':'ambulancia','fire engine':'camión bomberos',
 'taxi':'taxi','automobile':'coche','sport utility vehicle':'todoterreno','delivery truck':'camión',
 'articulated lorry':'tráiler','tractor':'tractor','racing car':'coche carreras','motorcycle':'motocicleta',
 'motor scooter':'patinete','bicycle':'bicicleta','kick scooter':'patinete','bus':'autobús',
 'trolleybus':'trolebús','minibus':'minibús','train':'tren','railway car':'vagón','bullet train':'tren bala',
 'light rail':'tranvía','station':'estación','tram':'tranvía','monorail':'monorraíl','maglev':'maglev',
 'airplane':'avión','small airplane':'avioneta','seat':'asiento','canoe':'canoa','speedboat':'lancha',
 'passenger ship':'crucero','ferry':'ferry','ship':'barco','rowboat':'bote','wheel':'rueda',
 'helicopter':'helicóptero','mountain railway':'funicular','railway track':'vía','metro':'metro',
 'nail polish':'esmalte','eye':'ojo','tongue':'lengua','mouth':'boca','baby':'bebé','girl':'niña',
 'baby angel':'ángel','santa claus':'papá noel','princess':'princesa','queen':'reina','fairy':'hada',
 'mermaid':'sirena','elf':'elfo','genie':'genio','zombie':'zombi','ghost':'fantasma',
 'alien':'extraterrestre','robot':'robot','jack-o-lantern':'calabaza','christmas tree':'abeto',
 'fireworks':'fuegos artificiales','sparkler':'bengala','red envelope':'sobre rojo','ribbon':'cinta',
 'wrapped gift':'regalo','teddy bear':'oso peluche','balloon':'globo','confetti ball':'confeti',
 'wind chime':'campanilla','ticket':'entrada','military medal':'medalla','trophy':'trofeo',
 'sports medal':'medalla','1st place medal':'oro','2nd place medal':'plata','3rd place medal':'bronce',
 'soccer ball':'futbol','baseball':'beisbol','softball':'softbol','basketball':'baloncesto',
 'volleyball':'voleibol','american football':'futbol americano','tennis':'tenis','flying disc':'frisbee',
 'bowling':'boliche','cricket game':'críquet','field hockey':'hockey','ice hockey':'hockey hielo',
 'lacrosse':'lacrosse','ping pong':'pingpong','badminton':'bádminton','boxing glove':'boxeo',
 'goal net':'portería','flag in hole':'golf','ice skate':'patín','fishing pole':'caña',
 'diving mask':'mascara buceo','snorkel':'tubo','skis':'esquí','sled':'trineo','curling stone':'curling',
 'direct hit':'diana','pool 8 ball':'billar','video game':'videojuego','slot machine':'tragaperras',
 'game die':'dado','puzzle piece':'rompecabezas','rubiks cube':'cubo rubik','chess pawn':'peón',
 'droplet':'gota','water wave':'ola','sandstorm':'tormenta arena','fog':'niebla','cyclone':'ciclón',
 'snowflake':'copo','hot springs':'aguas termales','thermometer':'termómetro','sunrise':'amanecer',
 'sunset':'atardecer','carousel horse':'carrusel','ferris wheel':'noria','roller coaster':'montaña rusa',
 'barber pole':'poste barbero','circus tent':'carpa circo','performing arts':'artes escénicas',
 'frame picture':'cuadro','artist palette':'paleta','spotlight':'foco','studio microphone':'micrófono',
 'control knobs':'perillas','musical keyboard':'teclado','musical score':'partitura',
 'saxophone':'saxofón','guitar':'guitarra','accordion':'acordeón','violin':'violín',
 'harpsichord':'clavicordio','banjo':'banjo','drum':'tambor','maracas':'maracas','blowfish':'pez globo',
 'shark':'tiburón','octopus':'pulpo','shell':'concha','crab':'cangrejo','shrimp':'gamba','squid':'calamar',
 'coral':'coral','snail':'caracol','butterfly':'mariposa','bug':'bicho','ant':'hormiga','honeybee':'abeja',
 'beetle':'escarabajo','cricket':'grillo','cockroach':'cucaracha','spider':'araña','scorpion':'escorpion',
 'mosquito':'mosquito','fly':'mosca','worm':'gusano','microbe':'microbio','frog':'rana',
 'crocodile':'cocodrilo','turtle':'tortuga','lizard':'lagarto','snake':'serpiente','sauropod':'saurio',
 'whale':'ballena','dolphin':'delfin','seal':'foca','tropical fish':'pez tropical','lobster':'bogavante',
 'goat':'cabra','ram':'carnero','sheep':'oveja','horse':'caballo','pony':'poni','donkey':'burro','mule':'mula',
 'cow':'vaca','ox':'buey','water buffalo':'búfalo','pig':'cerdo','boar':'jabalí','camel':'camello',
 'two-hump camel':'bactriano','llama':'llama','alpaca':'alpaca','giraffe':'jirafa','elephant':'elefante',
 'rhinoceros':'rinoceronte','mammoth':'mamut','hippopotamus':'hipopótamo','mouse':'ratón','rat':'rata',
 'hamster':'hámster','rabbit':'conejo','fox':'zorro','bear':'oso','panda':'panda','polar bear':'oso polar',
 'koala':'koala','sloth':'perezoso','otter':'nutria','skunk':'mofeta','tiger':'tigre','lion':'leon',
 'leopard':'leopardo','cat':'gato','dog':'perro','poodle':'caniche','wolf':'lobo','raccoon':'mapache',
 'monkey':'mono','gorilla':'gorila','orangutan':'orangutan','moose':'alce','deer':'ciervo',
 'chipmunk':'ardilla','penguin':'pinguino','dove':'paloma','eagle':'aguila','duck':'pato','owl':'buho',
 'peacock':'pavo real','parrot':'loro','flamingo':'flamenco','pelican':'pelicano','black bird':'cuervo',
 'turkey':'pavo','chicken':'gallina','rooster':'gallo','hatching chick':'polluelo','feather':'pluma',
 'nest':'nido','apple':'manzana','green apple':'manzana verde','pear':'pera','tangerine':'mandarina',
 'lemon':'limon','banana':'platano','watermelon':'sandia','strawberry':'fresa','blueberry':'arandano',
 'grapes':'uva','melon':'melon','cherries':'cereza','peach':'melocoton','mango':'mango',
 'pineapple':'piña','coconut':'coco','kiwi fruit':'kiwi','tomato':'tomate','olive':'aceituna',
 'eggplant':'berenjena','potato':'patata','carrot':'zanahoria','corn':'maiz','bell pepper':'pimiento',
 'cucumber':'pepino','leafy green':'lechuga','broccoli':'brocoli','garlic':'ajo','peanuts':'cacahuete',
 'bread':'pan','croissant':'croissant','baguette bread':'baguette','pretzel':'pretzel','bagel':'bagel',
 'pancakes':'tortitas','waffle':'galleta','cheese':'queso','meat on bone':'costilla','poultry leg':'muslo',
 'bacon':'tocino','hamburger':'hamburguesa','french fries':'patatas fritas','pizza':'pizza','hot dog':'perrito',
 'sandwich':'bocadillo','taco':'taco','burrito':'burrito','tamale':'tamal','egg':'huevo',
 'pot of food':'olla','fondue':'fondue','bowl with spoon':'cuenco','green salad':'ensalada',
 'popcorn':'palomitas','cooked rice':'arroz','steaming bowl':'fideos','sushi':'sushi','fried shrimp':'tempura',
 'ice cream':'helado','cake':'pastel','birthday cake':'cumpleaños','cupcake':'magdalena','pie':'tarta',
 'chocolate bar':'chocolate','candy':'caramelo','lollipop':'piruleta','custard':'natilla','honey pot':'miel',
 'baby bottle':'biberon','hot beverage':'té','teapot':'tetera','wine glass':'copa','cocktail glass':'coctel',
 'cup with straw':'refresco','chopsticks':'palillos','fork and knife':'cubierto','spoon':'cuchara',
 'kitchen knife':'cuchillo','amphora':'ánfora','compass':'brújula','brick':'ladrillo','wood':'madera',
 'charcoal':'carbón','crystal ball':'bola de cristal','magic wand':'varita','nazar amulet':'amuleto',
 'talisman':'talismán','yo-yo':'yo-yo','kite':'cometa','pinata':'piñata','nested dolls':'matrioska',
 'limitless':'infinito','rose':'rosa','hibiscus':'hibisco','sunflower':'girasol','tulip':'tulipan',
 'seedling':'semilla','potted plant':'maceta','evergreen tree':'abeto','deciduous tree':'árbol',
 'palm tree':'palmera','cactus':'cactus','sheaf of rice':'espigas','herb':'hierba','shamrock':'trébol',
 'four leaf clover':'trébol','pine tree':'pino','bouquet':'ramo','cherry blossom':'sakura','lotus':'loto',
 'maple leaf':'arce','fallen leaf':'hoja seca','mushroom':'seta','chestnut':'castaña','acorn':'bellota',
 'ear of grain':'espiga','sprout':'brote','bamboo':'bambú','red paper lantern':'farolillo',
}

def clean(nm):
    t=nm.split(';')[-1].strip().lower()
    t=re.sub(r'\bsymbol\b|\bsign\b|\bbutton\b|\bface\b','',t).strip()
    t=re.sub(r'\bwith.*$','',t).strip()
    return t

def main():
    con=sqlite3.connect('sintesio.db'); cur=con.cursor()
    cur.execute("SELECT espanol_norm FROM sustantivo"); corpus={r[0] for r in cur.fetchall()}
    cur.execute("SELECT concepto_espanol FROM imports WHERE estado!='rechazada'")
    pend={r[0].lower().strip() for r in cur.fetchall()}
    used=set()
    cur.execute("SELECT glifo FROM imports WHERE glifo IS NOT NULL AND glifo!=''")
    for (g,) in cur.fetchall(): used.update(g)
    assigned=emoji_names()
    cands=[]; seen=set()
    for cp,nm in assigned:
        ch=chr(cp)
        if ch in used: continue
        if any(k in nm.upper() for k in SKIP): continue
        t=clean(nm)
        es=None
        for key,val in EN_ES.items():
            if key==t or (len(key)>4 and key in t) or (len(t)>4 and t in key):
                es=val; break
        if not es: continue
        esl=es.lower()
        if esl in corpus or esl in pend or esl in seen: continue
        seen.add(esl); cands.append((cp,ch,es))
    os.makedirs('data',exist_ok=True)
    json.dump(cands,open('data/glyph_candidates.json','w'),ensure_ascii=False)
    print(f"Emojis totales Unicode 15.x: {len(assigned)}")
    print(f"Glifos ya procesados: {len(used & {chr(cp) for cp,_ in assigned})}")
    print(f"Candidatos NUEVOS sin duplicar corpus/imports: {len(cands)}")
    for cp,ch,es in cands[:40]:
        print(f"  {ch} U+{cp:04X} {es}")
    print("  ...")
    for cp,ch,es in cands[-15:]:
        print(f"  {ch} U+{cp:04X} {es}")

if __name__=='__main__': main()
