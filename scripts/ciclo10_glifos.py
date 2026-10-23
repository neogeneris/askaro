#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ciclo 10: inventario completo de glifos UTF-8 (Unicode 15.x, ~1308 emojis).

Motivacion: el ciclo 9 proceso 25 filas "a ojo" y dejo 76/106. Con horas por delante
el universo de sustantivos codificables en glifos es de cientos, no de decenas.
Este script:
  1) Lee data/glyph_candidates.json (scripts/glyph_inventory.py): emojis pendientes con
     glosa espanol verificada, sin duplicar corpus askaro ni imports existentes.
  2) Aplica las reglas maestro del ciclo 9 (norm_askaro + tilde penultima).
  3) Inserta como auto-glifo/propuesta con su glifo registrado.
Reversible: DELETE FROM imports WHERE variantes LIKE 'ciclo10:%';
            DELETE FROM imports_forma WHERE import_id NOT IN (SELECT id FROM imports);

Filtro de calidad (ampliado del ciclo 9):
  a) solo una palabra por glifo (los sintagmas no pegan en la morfologia askara);
  b) cada glosa espanol debe COINCIDIR con el nombre Unicode oficial del codepoint
     (tabla CHECK: es -> tokens obligatorios del nombre EN). Esto evita errores tipo
     ⚖->balanza (realmente 'scales'), 🪔->lampara ('diya lamp') que un mapeo ciego produce.
Reversible: DELETE FROM imports WHERE variantes LIKE 'ciclo10:%';
            DELETE FROM imports_forma WHERE import_id NOT IN (SELECT id FROM imports);
"""
import sqlite3, json, re, os, sys, unicodedata

DB = "sintesio.db"
CANDS = "data/glyph_candidates.json"

# es -> tokens que DEBEN aparecer en el nombre Unicode oficial del codepoint
CHECK = {
 'manzana':['apple'],'pera':['pear'],'naranja':['orange'],'limon':['lemon'],'platano':['banana'],
 'sandia':['watermelon'],'fresa':['strawberry'],'uva':['grape'],'cereza':['cherri'],'melocoton':['peach'],
 ' pina':['pineapple'],'mango':['mango'],'kiwi':['kiwi'],'coco':['coconut'],'melon':['melon'],
 'mandarina':['tangerine'],'aguacate':['avocado'],'tomate':['tomato'],'zanahoria':['carrot'],
 'patata':['potato'],'maiz':['corn'],'ajo':['garlic'],'cebolla':['onion'],'brocoli':['broccoli'],
 'lechuga':['leafy'],'pimiento':['pepper'],'pepino':['cucumber'],'aceituna':['olive'],'berenjena':['eggplant'],
 'castana':['chestnut'],'seta':['mushroom'],'bellota':['acorn'],'espiga':['ear of grain'],
 'pan':['bread'],'croissant':['croissant'],'pizza':['pizza'],'queso':['cheese'],'huevo':['egg'],
 'bacon':['bacon'],'hamburguesa':['hamburger'],'taco':['taco'],'burrito':['burrito'],'tamal':['tamale'],
 'sushi':['sushi'],'pastel':['cake'],'cumpleanos':['birthday'],'tarta':['pie'],'chocolate':['chocolate'],
 'caramelo':['candy'],'piruleta':['lollipop'],'miel':['honey pot'],'biberon':['baby bottle'],
 'te':['hot beverage'],'copa':['wine glass'],'coctel':['cocktail'],'cuchara':['spoon'],
 'cuchillo':['knife'],'palillos':['chopstick'],'olla':['pot of food'],'ensalada':['salad'],
 'palomitas':['popcorn'],'arroz':['cooked rice'],'fideos':['steaming bowl'],'espagueti':['spaghetti'],
 'tempura':['fried shrimp'],'jabali':['boar'],'cerdo':['pig'],'vaca':['cow'],'buey':['ox'],
 'bufalo':['buffalo'],'cabra':['goat'],'oveja':['sheep'],'carnero':['ram'],'caballo':['horse'],
 'poni':['pony'],'burro':['donkey'],'mula':['mule'],'camello':['camel'],'llama':['llama'],
 'alpaca':['alpaca'],'jirafa':['giraffe'],'elefante':['elephant'],'rinoceronte':['rhinoceros'],
 'mamut':['mammoth'],'hipopotamo':['hippopotamus'],'leon':['lion'],'leopardo':['leopard'],
 'tigre':['tiger'],'oso':['bear'],'panda':['panda'],'koala':['koala'],'perezoso':['sloth'],
 'nutria':['otter'],'zorro':['fox'],'lobo':['wolf'],'mapache':['raccoon'],
 'perro':['dog'],'caniche':['poodle'],'gato':['cat'],'conejo':['rabbit'],'ardilla':['chipmunk'],
 'erizo':['hedgehog'],'murcielago':['bat'],'raton':['mouse'],'rata':['rat'],'mono':['monkey'],
 'gorila':['gorilla'],'orangutan':['orangutan'],'sapo':['toad'],'rana':['frog'],'tortuga':['turtle'],
 'cocodrilo':['crocodile'],'lagarto':['lizard'],'serpiente':['snake'],'ballena':['whale'],
 'delfin':['dolphin'],'foca':['seal'],'morsa':['walrus'],'coral':['coral'],'caracol':['snail'],
 'mariposa':['butterfly'],'polilla':['moth'],'abeja':['bee'],'mosca':['fly'],'mosquito':['mosquito'],
 'grillo':['cricket'],'cucaracha':['cockroach'],'escarabajo':['beetle'],'hormiga':['ant'],
 'arana':['spider'],'escorpion':['scorpion'],'gusano':['worm'],'microbio':['microbe'],
 'pajaro':['bird'],'pinguino':['penguin'],'colibri':['hummingbird'],'buho':['owl'],'loro':['parrot'],
 'flamingo':['flamingo'],'cisne':['swan'],'paloma':['dove'],
 'aguila':['eagle'],'pato':['duck'],'gallo':['rooster'],'pollo':['chicken'],'avestruz':['ostrich'],
 'polluelo':['hatching chick'],'pluma':['feather'],'nido':['nest'],'telarana':['web'],
 'rosa':['rose'],'hibisco':['hibiscus'],'girasol':['sunflower'],'tulipan':['tulip'],'orquidea':['orchid'],
 'loto':['lotus'],'sakura':['blossom'],'ramo':['bouquet'],'arbol':['deciduous tree'],'pino':['pine tree'],
 'abeto':['evergreen tree'],'palmera':['palm tree'],'cactus':['cactus'],'bambu':['bamboo'],
 'helecho':['fern'],'hierba':['herb'],'trebol':['shamrock'],'hoja':['fallen leaf'],'arce':['maple leaf'],
 'semilla':['seedling'],'maceta':['potted plant'],'flor':['white flower'],
 'luna':['crescent moon'],'arco':['rainbow'],'rayo':['lightning'],
 'volcan':['volcano'],'ola':['water wave'],'hielo':['ice'],'fuego':['fire'],
 'gota':['droplet'],'niebla':['fog'],'ciclon':['cyclone'],'copo':['snowflake'],'amanecer':['sunrise'],
 'atardecer':['sunset'],'montana':['mountain'],'isla':['desert island'],'desierto':['desert'],
 'playa':['beach'],'puente':['bridge'],'edificio':['classical building'],'casa':['house building'],
 'fabrica':['factory'],'tienda':['convenience store'],'hotel':['hotel'],'iglesia':['church'],
 'mezquita':['mosque'],'sinagoga':['synagogue'],'fuente':['fountain'],'choza':['hut'],
 'estatua':['statue'],'escudo':['shield'],'espada':['dagger'],'cohete':['rocket'],
 'satelite':['satellite'],'avion':['airplane'],'avioneta':['small airplane'],
 'helicoptero':['helicopter'],'bicicleta':['bicycle'],'motocicleta':['motorcycle'],'patinete':['kick scooter'],
 'autobus':['bus'],'coche':['automobile'],'taxi':['taxi'],'ambulancia':['ambulance'],'camion':['delivery truck'],
 'tractor':['tractor'],'tren':['train'],'tranvia':['tram'],'metro':['metro'],'estacion':['station'],
 'barco':['ship'],'velero':['sailboat'],'canoa':['canoe'],'ferry':['ferry'],'bote':['rowboat'],
 'rueda':['wheel'],'ancla':['anchor'],'brujula':['compass'],'movil':['mobile phone'],
 'telefono':['telephone'],'ordenador':['desktop computer'],'impresora':['printer'],
 'televisor':['television'],'radio':['radio'],'camara':['camera'],'linterna':['flashlight'],'vela':['candle'],
 'lapiz':['pencil'],'boligrafo':['pen'],'pincel':['paintbrush'],'tijeras':['scissors'],'candado':['lock'],
 'llave':['key'],'martillo':['hammer'],'hacha':['axe'],'sierra':['saw'],'destornillador':['screwdriver'],
 'engranaje':['gear'],'probeta':['test tube'],'termometro':['thermometer'],
 'guantes':['gloves'],'estetoscopio':['stethoscope'],'pastilla':['pill'],'lupa':['magnifying glass'],
 'microscopio':['microscope'],'microfono':['microphone'],'auriculares':['headphone'],
 'guitarra':['guitar'],'violín':['violin'],'saxofón':['saxophone'],
 'trompeta':['trumpet'],'tuba':['tuba'],'pandereta':['tambourine'],'maracas':['maraca'],'tambor':['drum'],
 'banjo':['banjo'],'accordion':['accordion'],'campana':['bell'],
 'silbato':['whistle'],'libro':['book'],'cuaderno':['notebook'],'pergamino':['scroll'],'periodico':['newspaper'],
 'ticket':['ticket'],'cometa':['kite'],'pinata':['pinata'],'medalla':['medal'],
 'trofeo':['trophy'],'futbol':['soccer ball'],'beisbol':['baseball'],'baloncesto':['basketball'],
 'voleibol':['volleyball'],'tenis':['tennis'],'rugby':['rugby football'],'billar':['pool 8 ball'],
 'frisbee':['flying disc'],'boliche':['bowling'],'boxeo':['boxing glove'],'porteria':['goal net'],
 'golf':['flag in hole'],'patin':['ice skate'],'esqui':['ski'],'trineo':['sled'],'curling':['curling stone'],
 'casco':['helmet'],'varita':['magic wand'],'dado':['game die'],
 'rompecabezas':['jigsaw'],'nota musical':['musical note'],'partitura':['musical score'],
 'calabaza':['gourd'],'fantasma':['ghost'],'robot':['robot'],
 'extraterrestre':['alien'],'zombi':['zombie'],'genio':['genie'],'hada':['fairy'],'princesa':['princess'],
 'reina':['queen'],'angel':['baby angel'],'sirena':['mermaid'],'niña':['girl'],'bebé':['baby'],
 'sombrero':['hat'],'corona':['crown'],'camisa':['shirt'],'vestido':['dress'],'kimono':['kimono'],
 'sari':['sari'],'biquini':['bikini'],'calcetín':['socks'],'guante':['glove'],'bufanda':['scarf'],
 'abrigo':['coat'],'vaqueros':['jeans'],'bolso':['handbag'],'monedero':['purse'],'mochila':['backpack'],
 'corbata':['necktie'],'anillo':['ring'],'gema':['gem stone'],'billete':['banknote'],
 'tarjeta':['credit card'],'regla':['straight ruler'],'chincheta':['pushpin'],
 'portapapeles':['clipboard'],'carpeta':['file folder'],'calendario':['calendar'],
 'sobre':['envelope'],'megafono':['megaphone'],'enchufe':['electric plug'],'pila':['battery'],
 'bombilla':['light bulb'],'extintor':['fire extinguisher'],'escalera':['ladder'],
 'mapamundi':['world map'],'telescopio':['telescope'],'petri':['petri dish'],'dna':['dna'],
 'cadena':['chains'],'disquete':['floppy disk'],'escaner':['scanner'],'videoconsola':['joystick'],
}

def norm_askaro(es):
    w = es.lower()
    w = w.replace("qu", "k").replace("ch", "c")          # ch -> c (africada)
    w = re.sub(r"[cz]", "s", w)                          # c suave, z, s -> s
    w = w.replace("c", "k")                              # c restante (fuerte) -> k
    w = re.sub(r"^h", "", w)                             # h inicial muda -> elision
    w = w.replace("x", "ks")
    return w

def tilde_penult(w):
    vowels = "aeiouáéíóúâêî"
    vs = [i for i, ch in enumerate(w) if ch in vowels]
    if len(vs) < 2:
        return w, None
    if any(ch in "áéíóúâêî" for ch in w):
        return w, "preexistente"
    idx = vs[-2]
    acc = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}
    return w[:idx] + acc[w[idx]] + w[idx+1:], "penultima"

FEM_BIOL = {"nutria","gata","perra","vaca","yegua","burra","ovelha","oveja","cabra","cabra",
            "cerda","leona","zorra","loba","osa","gallina","rana","mosca","abeja","araña",
            "hormiga","caracol","libélula","luciérnaga","mariquita","mariposa","langosta",
            "gamba","foca ballena","ballena","delfin","tortuga","lagarta","serpiente",
            "araña","escorpión","niña","mujer","reina","princesa","hada","sirena","vaca"}

def main():
    if not os.path.exists(CANDS):
        print(f"Falta {CANDS}; ejecutar primero scripts/glyph_inventory.py"); sys.exit(1)
    cands = json.load(open(CANDS))
    con = sqlite3.connect(DB); cur = con.cursor()

    existing_es = {r[0] for r in cur.execute("SELECT concepto_espanol FROM imports")}
    lex_roots = {r[0] for r in cur.execute("SELECT termino_norm FROM sustantivo")}
    used_glyphs = set()
    for (g,) in cur.execute("SELECT glifo FROM imports WHERE glifo IS NOT NULL AND glifo!=''"):
        used_glyphs.update(g)

    added, skipped = [], []
    for cp, glyph, es in cands:
        esl = es.lower().strip()
        if " " in esl or "-" in esl:
            skipped.append((esl, "sintagma (no es una palabra)")); continue
        toks = CHECK.get(esl)
        if toks is None:
            skipped.append((esl, "glosa no listada en CHECK")); continue
        try: nm = unicodedata.name(chr(cp)).lower()
        except ValueError: nm = ''
        if not all(t in nm for t in toks):
            skipped.append((esl, f"glosa no coincide con Unicode ({nm})")); continue
        if glyph in used_glyphs:
            skipped.append((esl, "glifo ya asignado")); continue
        if esl in existing_es:
            skipped.append((esl, "ya en imports")); continue
        base = norm_askaro(esl)
        forma_tonica, modo = tilde_penult(base)
        if forma_tonica in lex_roots or base in lex_roots:
            skipped.append((esl, f"colision raiz corpus ({base})")); continue
        genero = "femenino_biol" if esl in FEM_BIOL else "neutro"
        des = "-a" if genero == "femenino_biol" else "-o"
        maxid = cur.execute("SELECT MAX(id) FROM imports").fetchone()[0] or 0
        nid = maxid + 1
        crit = "cognado_universal" if esl in ("manzana","naranja","tomate","banana","platano",
                "zanahoria","cebolla","ajo","sal","aceite","vinagre","limon","azucar","cafe") \
               else "reconstruccion_latina"
        cur.execute("""INSERT INTO imports (id, concepto_espanol, es, palabra_sugerida, tipo_sugerencia,
                     estado, clase_gramatical, askaro_forma_norm, criterio_seleccion, etimologia, variantes, glifo)
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (nid, esl, esl, forma_tonica, "auto-glifo", "propuesta", "sustantivo", forma_tonica,
             crit, f"glifo U+{cp:04X} {glyph}", f"ciclo10:{glyph}", glyph))
        cur.execute("INSERT INTO imports_forma (import_id, forma, desinencia, genero, forma_tonica, silaba_tonica) VALUES (?,?,?,?,?,?)",
            (nid, base, des, genero, forma_tonica, modo))
        used_glyphs.add(glyph); existing_es.add(esl)
        added.append((nid, esl, base, forma_tonica, glyph))

    con.commit()
    tot = cur.execute("SELECT COUNT(*) FROM imports").fetchone()[0]
    ngl = cur.execute("SELECT COUNT(*) FROM imports WHERE glifo IS NOT NULL AND glifo!=''").fetchone()[0]
    npend = cur.execute("SELECT COUNT(*) FROM imports WHERE glifo IS NULL OR glifo=''").fetchone()[0]
    print(f"AÑADIDOS: {len(added)}  OMITIDOS: {len(skipped)}")
    for nid, e, b, ft, g in added[:20]:
        print(f"  #{nid} {e:14s} -> {b:14s} tonica={ft:14s} {g}")
    print("  ...")
    for nid, e, b, ft, g in added[-10:]:
        print(f"  #{nid} {e:14s} -> {b:14s} tonica={ft:14s} {g}")
    print("OMITIDOS:")
    for e, r in skipped:
        print(f"  {e}: {r}")
    print(f"TOTAL imports: {tot} | con glifo: {ngl} | sin glifo (léxico): {npend}")
    con.close()

if __name__ == "__main__":
    main()
