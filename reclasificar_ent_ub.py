# -*- coding: utf-8 -*-
"""
Reclasificador ontológico Askáro-A  [ENT] / [UB]
=================================================
Compilador-taxonomista para la arquitectura dual simplificada:

  MACROGRUPOS
    ENT (entes)      -> objeto_concreto | material | abstracto | rol_entidad
    UB  (locativos)  -> ubicacion | ruta_direccion | coordenada_temporal
                        (el tiempo se trata unificado bajo la misma coordenada, cf. tabla `roles`: ub = matriz espacio+tiempo)

  CRITERIO BIOLÓGICO SEXUADO (adentro de ENT)
    - Se ELIMINA la distinción teórica animado/inanimado.
    - macho / rol general  -> sufijo temático -o  (o -or/-oro agente)  => ba (masculino)
    - hembra               -> sufijo temático -a                       => fa (femenino)
    - neutro / inanimado    -> terminación obligatoria -o               => entes no sexuados
    - roles comunes (ambos sexos posibles) => rol_general (-o/-or), subsumido en ba
    - pacientes (p.ej. 'empleado', 'víctima', 'acusado') => pat, con morfología -o/-a

  ADAPTACIÓN MORFOLÓGICA A LA NORMA Askáro-A
    - Toda palabra con >=2 vocales lleva tilde gráfica EXPLÍCITA en la tónica
      (reglas españolas; hiatus a/e/o + i/u átonos -> golpe en la vocal cerrada).
    - Femeninos biológicos terminan en -a; todo lo demás termina en -o (o -or/-oro).
    - Los sustantivos UB conservan su desinencia léxica (-o/-a); el marcador
      categorial es el prefijo lok-/ub-, no la terminación.

Salidas: reclasificacion_ent_ub.csv  +  UPDATE en lexico.db (tabla sustantivos, columnas nuevas macrogrupo/tipo_interno/sexo_morfologia)
"""
import sqlite3, csv, re, unicodedata

VOC = set('aeiouáéíóúàèìòùäëïöü')
VOC_BASE = {'á':'a','é':'e','í':'i','ó':'o','ú':'u','à':'a','è':'e','ì':'i','ò':'o','ù':'u','ä':'a','ë':'e','ï':'i','ö':'o','ü':'u'}

def strip_acc(s): return ''.join(VOC_BASE.get(c, c) for c in s)

def count_voc(s):
    return sum(1 for c in s if c in VOC or c in 'áéíóúàèìòùäëïöü')

def stressed_form(word):
    """Devuelve la forma askara con tilde explícita en la tónica (reglas españolas)."""
    w = word.strip().lower()
    # separar parte multi-palabra (compuestos tipo 'sega a máno'): acentuar solo la última palabra léxica
    parts = w.split()
    if len(parts) > 1:
        return ' '.join(stressed_single(p) if count_voc(p) >= 2 else p for p in parts)
    return stressed_single(w)

def stressed_single(w):
    base = strip_acc(w)
    n = len(base)
    # localizar índice de la vocal final y penúltima
    vidx = [i for i, c in enumerate(base) if c in 'aeiou']
    if not vidx:
        return w
    last = vidx[-1]
    # regla española sobre la terminación
    if base.endswith(('o', 'a', 'e')) or re.search(r'[aeiou]s$', base) or re.search(r'[aeiou]n$', base):
        pos = vidx[-2] if len(vidx) >= 2 else None            # llana: tónica = penúltima vocal
    else:
        pos = last                                            # aguda: tónica = última vocal
        # hiatus: si la última vocal es cerrada (i,u) preceded por abierta -> golpe en la cerrada
        if pos > 0 and base[pos] in 'iu':
            prev = base[pos-1]
            if prev in 'aeo':
                pos = pos  # ya es la cerrada (última vocal) -> correcto
    if pos is None:
        return w
    # ¿ya existe una tilde en otra vocal? respetar marcas existentes del lémame
    if any(base[i] == c and w[i] != c for i, c in enumerate(base) if False):
        pass
    if any(ord(w[i]) in range(0xE0, 0xFB) or w[i] in 'áéíóú' for i in range(len(w))):
        # ya hay acento gráfico: conservar (forma canónica preexistente)
        return w
    TILDE = {'a':'á','e':'é','i':'í','o':'ó','u':'ú'}
    ch = base[pos]
    if ch in TILDE:
        out = list(w)
        out[pos] = TILDE[ch]
        return ''.join(out)
    return w

# ---------------- LÉXICOS DE CLASIFICACIÓN ----------------
TIEMPO = {  # coordenadas temporales puras (tem)
 'tiempo','hora','minuto','segundo','dia','ano','anio','semana','mes (unidad de tiempo)',
 'madrugada','manana','mediodia','tarde','atardecer','medianoche','momento','instante',
 'siglo','decada','milenio','eternidad','pasado','presente','futuro',
 'lunes','martes','miercoles','jueves','viernes','sabado','domingo',
 'primavera','verano','otono','invierno','temporada','calendario','edad','epoca','era',
 'ciclo','juventud','vejez','duracion','frecuencia','kelvin','celsius','voltio','amperio','vatio','ohmio','metro','byte','segundo (unidad si)'
}
# Nota: unidades SI de longitud/masa/tiempo son coordenadas métricas, PERO
# kelvin/celsius/voltio... no son marcos espaciotemporales: van a ENT abstracto.
UNIDADES_SI = {'kelvin','celsius','voltio','amperio','vatio','ohmio','metro','byte','segundo (unidad si)','numero','cifra'}

RUTA_DIR = {  # rutas / direcciones / vectores (lok-ruta)
 'camino','via','calle','ruta','sendero','autopista','carretera','ferrocarril','tranvia',
 'norte','sur','este','oeste','noreste','noroeste','sureste','suroeste','direccion',
 'latitud','longitud','altitud','ecuador','hemisferio','orbita','lado','retirada','peregrinacion'
}

UBICACION = {  # ubicaciones estáticas / recintos / topónimos genéricos (lok-recinto)
 'lugar','casa','ciudad','aldea','barrio','vecindario','pueblo','capital','provincia','region',
 'distrito','municipio','comarca','pais','patria','nacion','estado','imperio','reino','colonia',
 'territorio','metropoli','continente','frontera','mundo','universo','cosmos','naturaleza',
 'playa','isla','selva','bosque','campo','valle','colina','montana','volcan','cordillera',
 'pradera','llanura','meseta','peninsula','golfo','bahia','estrecho (accidente geo.)','canal',
 'archipielago','arrecife','acantilado','prado','desierto','lago','oceano','mar','rio',
 'iglesia','mezquita','sinagoga','templo','altar','hospital','escuela','universidad','clase',
 'biblioteca','archivo','museo','mercado','banco','plaza','teatro','cine','estadio','gimnasio',
 'puerto','aeropuerto','estacion','carcel','tribunal','palacio','castillo','torre','muro','puente',
 'cocina','dormitorio','sala','jardin','parque','oficina','fabrica','tienda','hotel','restaurante',
 'laboratorio','taller','almacen','granja','huerto','habitacion','piso','techo','pared','porta','ventana',
 'espacio','espacio (fis.)','spatío'
}

GEO_NATURAL = UBICACION  # las ubicaciones naturales también son lok

# Roles de entidad (agentes/pacientes humanos u ocupaciones)
ROL_ENTIDAD = {
 'madre','padre','hermano','hermana','hijo','hija','abuelo','abuela','nieto','nieta','tio','tia',
 'primo','prima','sobrino','sobrina','suegro','suegra','yerno','nuera','cunado','cunada',
 'bisabuelo','tatarabuelo','bisnieto','familia','persona','gente','pueblo (gente)','ciudadano',
 'doctor','medico','enfermero','cirujano','farmaceutico','maestro','profesor','estudiante','alumno',
 'ingeniero','abogado','juez','fiscal','defensor','acusado','policia','soldado','capitan','general (grado)',
 'coronel','teniente','sargento','cabo','rey','reina','presidente','ministro','gobernador','alcalde',
 'sacerdote','monje','monja','obispo','papa (sumo pontifice)','filosofo','autor','actor','artista',
 'escritor','poeta','jugador','entrenador','campeon','atleta','periodista','reportero','testigo',
 'victima','culpable','inocente','cazador','empleado','trabajador','servidor','robot','dios','ser humano','hombre','mujer','nino','nia',
 'remitente','destinatario','usuario','cliente','empresa','equipo','tropa','ejercito','sociedad','grupo','multitud','populacho'
}

ANIMAL_SEXO = {  # sexo biológico explícito conocido (macho/hembra) — resto: comun
 'macho': {'padre','hermano','hijo','abuelo','nieto','tio','primo','sobrino','cunado','bisabuelo','tatarabuelo','bisnieto',
   'gallo','toro','perro','gato','caballo','lobo','leon','tigre','oso','zorro','ciervo','conejo','elefante','jabali','venado',
   'escorpion','pulpo','tiburon','delfin','caracol','erizo','sacerdote','monje','obispo','papa (sumo pontifice)','rey',
   'presidente','ministro','gobernador','alcalde','juez','fiscal','doctor','maestro','profesor','ingeniero','abogado',
   'soldado','capitan','general (grado)','coronel','teniente','sargento','cabo','actor','autor','poeta','escritor',
   'artistacomun','jugador','entrenador','campeon','atleta','periodista','reportero','testigo','cazador','dios','hombre','novio','marido'},
 'hembra': {'madre','hermana','hija','abuela','nieta','tia','prima','sobrina','suegra','cunada','vaca','gallina','gata',
   'rana','tortuga','ballena','abeja','avestruz','cisne','foca','ostra','langosta','morsa','monja','reina','nuera','yernocomun',
   'mujer','niña','victima','novia','esposa'},
}

MATERIAL = {
 'madera','hierro','plata metal ag','plata','cobre','oro','azufre','sulfuro','sulfuro (material)','carbon','petroleo','gas','acido',
 'arena','barro','polvo','hielo','nieve','lluvia','niebla','luz','sombra','viento','nube','cielo','sangre','carne','piel','hueso',
 'hoja','flor','vidrio','papel','tela','algodon','lana','seda','cuero','caucho','plastico','cement','hormigon','ladrillo','ceramica',
 'jabon','aceite','mantequilla','azucar','miel','sal','grano','trigo','maiz','avena','cebada','centeno','pan','leche','agua','fuego',
 'olla','sarten','cuchillo','cuchara','tenedor','plato','taza','vaso','botella','copa','jarra','cuchillo de cocina','sierra de mano',
 'silla','mesa','cama','lampara','espejo','alfombra','cortina','colchon','almohada','sabana','manta','cojin','cuadro','florero','canasto',
 'ropa','camisa','pantalon','zapato','sombrero','abrigo','bolsa','calcetin','guante','bufanda','cinturon','corbata','gorra','botas',
 'sandalia','zapatilla','chaqueta','sueter','falda','vestido','blusa','pantalon corto','ropa interior','sosten','pijama','bata','delantal',
 'panuelo','gafas','sombrilla','paraguas','joya','anillo','collar','pulsera','martillo','sierra','taladro','destornillador','alicate',
 'llave inglesa','tornillo','clavo','tuerca','arandela','cincel','lima','lijadora','hacha','pico','pala','rastrillo','azada','machete',
 'tijeras','aguja','alfiler','imperdible','boton','cierre','cuerda','cadena','alambre','tubo','plomada','instrumento','motor','rueda',
 'maquina','computadora','telefono','radio','television','pantalla','teclado','cable','antena','bateria','chip','procesador','terminal',
 'avion','bicicleta','moto','autobus','camion','tren','coche','helicoptero','submarino','yate','velero','canoa','balsa','patinete',
 'monopatin','trineo','carreta','carruaje','tractor','excavadora','ambulancia','coche policial','coche bomberos','avioneta','globo aerostatico',
 'piano','guitarra','violin','tambor','flauta','violonchelo','contrabajo','clarinete','oboe','fagot','trompeta','trombon','tuba','saxofon',
 'timbal','xilofono','arpa','organo','acordeon','armonica','arma','escudo','espada','lanza','reloj','cronometro','foto','camara','pelicula',
 'libro','lapiz','carta','paquete','sello','sobre (objeto)','telegrama','estatua','retrato','pintura','escultura','medalla','trofeo','balon',
 'notamusical','sensor','impreso','billete','moneda','barca','navio','ave','pez','pescado','pollo','carne de vaca','huevo','queso','vino',
 'cerveza','jugo','sopa','ensalada','pasta','pizza','chocolate','cafe','te','arroz','tomate','papa','cebolla','ajo','zanahoria','lechuga',
 'naranja','manzana','platano','uva','limon','nuez','sandia','melon','fresa','frambuesa','arandano','cereza','ciruela','durazno','higo',
 'granada','pine','mango','papaya','lenteja','garbanzo','frijol','soja','almendra','avellana','cacahuete','pistacho','castana','arroz blanco',
 'arroz integral','microbio','celula','bacteria','virus','vitamina','proteina','antibiotico','analgesico','anestesia','remedio','medicina',
 'vacuna','formon','llave','estante','bandeja','caja','cesta','saco','bidon','escalera','andamio','grua','torno',' soldadura','yunque'
}

# ---------------- FUNCIONES DE CLASIFICACIÓN ----------------
def es_ubicacion(es):
    e = es.lower().strip()
    if e in UBICACION: return True
    sufijos_loc = ('ville','city') 
    return False

def clasificar(codigo, forma, es, naturaleza, sexo_db):
    e = es.lower().strip()
    f = forma.strip()

    # --- Macrogrupo ---
    if e in TIEMPO or e.startswith(('lunes','martes','miercoles','jueves','viernes','sabado','domingo')):
        macro, interno = 'UB', 'coordenada_temporal (tem)'
    elif e in RUTA_DIR:
        macro, interno = 'UB', 'ruta_direccion'
    elif es_ubicacion(e):
        macro, interno = 'UB', 'ubicacion_recinto'
    else:
        macro = 'ENT'
        if e in ROL_ENTIDAD:
            interno = 'rol_entidad'
        elif naturaleza == 'abstracto' or e in UNIDADES_SI:
            interno = 'abstracto'
        elif naturaleza == 'material' or e in MATERIAL:
            interno = 'material'
        else:
            interno = 'objeto_concreto'

    # --- Tipificación biológica/morfológica (solo aplica morfología sexual a ENT vivos) ---
    if macro == 'UB':
        bio = 'neutro_inanimado(-o)' if not f.endswith('a') else 'forma_femenina_lexica(-a)'
        rol = 'lok' if interno != 'coordenada_temporal (tem)' else 'tem'
        return macro, interno, bio, rol, f

    # ENT: determinar sexo biológico
    if e in ANIMAL_SEXO['hembra'] or (sexo_db == 'hembra'):
        sexo = 'hembra'
    elif e in ANIMAL_SEXO['macho'] or (sexo_db == 'macho'):
        sexo = 'macho'
    elif sexo_db == 'comun' or e in ROL_ENTIDAD:
        sexo = 'comun_rol_general'
    else:
        sexo = 'neutro'

    if interno == 'objeto_concreto' and e in {'arbol','planta','flora','microbio','celula','bacteria','virus'} :
        sexo = 'neutro'  # criterio biológico sexuado NO aplica a flora/microbios: sin sexo explícito -> -o

    # Morfología: hembra -> -a ; macho/rol general -> -o/-or ; neutro -> -o
    stem = f[:-1] if f and f[-1] in 'ao' else f
    if sexo == 'hembra':
        forma_adaptada = stem + 'a'
        bio = 'fa(-a)'
        rol = 'ba/fa' if interno == 'rol_entidad' else 'fa'
    elif sexo == 'macho':
        forma_adaptada = stem + 'o'
        bio = 'ba(-o/-or)'
        rol = 'ag' if interno == 'rol_entidad' else 'ba'
    elif sexo == 'comun_rol_general':
        forma_adaptada = stem + 'o'
        bio = 'rol_general(-o/-or)'
        rol = 'ag' if interno == 'rol_entidad' else 'ba'
    else:
        forma_adaptada = stem + 'o'
        bio = 'neutro_inanimado(-o)'
        rol = 'ent'
    # pacientes típicos
    if e in {'victima','acusado','empleado','paciente'}:
        rol = 'pat'
    forma_adaptada = stressed_form(forma_adaptada)
    return macro, interno, bio, rol, forma_adaptada

con = sqlite3.connect('lexico.db')
cur = con.cursor()
rows = cur.execute('SELECT codigo, forma, es, naturaleza, sexo_biologico FROM sustantivos').fetchall()

out = []
for codigo, forma, es, naturaleza, sexo_db in rows:
    macro, interno, bio, rol, fa = clasificar(codigo, forma, es, naturaleza, sexo_db)
    out.append((codigo, forma, fa, es, macro, interno, bio, rol))

with open('reclasificacion_ent_ub.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['codigo','forma_original','forma_askaro_A','concepto_es','macrogrupo','tipo_interno','morfologia_biolgica','rol_sintactico'])
    w.writerows(out)

# resumen
from collections import Counter
cm = Counter(o[4] for o in out)
ci = Counter((o[4], o[5]) for o in out)
cb = Counter(o[6] for o in out)
print('MACROGRUPO:', dict(cm))
for k, v in sorted(ci.items()): print(' ', k, v)
print('MORFOLOGÍA:', dict(cb))

# ---- Escribir en la BD (columnas nuevas para acceso O(1)) ----
cur.executescript("""
ALTER TABLE sustantivos ADD COLUMN macrogrupo TEXT;
ALTER TABLE sustantivos ADD COLUMN tipo_interno TEXT;
ALTER TABLE sustantivos ADD COLUMN morfologia_sexo TEXT;
ALTER TABLE sustantivos ADD COLUMN rol_sintactico TEXT;
""") if not any(r[1]=='macrogrupo' for r in cur.execute('PRAGMA table_info(sustantivos)')) else None
cur.executemany('UPDATE sustantivos SET macrogrupo=?, tipo_interno=?, morfologia_sexo=?, rol_sintactico=? WHERE codigo=?',
                [(o[4], o[5], o[6], o[7], o[0]) for o in out])
con.commit()
print('BD actualizada: sustantivos.macrogrupo/tipo_interno/morfologia_sexo/rol_sintactico')
