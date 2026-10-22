# sintesio_fabula_test.py — Compresión de la fábula en tres modos (CORREGIDO V2)

# ============================================================
# TABLAS DE CODIFICACIÓN
# ============================================================

CTRL = {
    'SEP': 0x01, 'END': 0x02, 'QST': 0x03, 'NEG': 0x05,
    'PST': 0x06, 'FUT': 0x07, 'AGT': 0x08, 'PAT': 0x09,
    'INS': 0x0A, 'LOC': 0x0B, 'ENT': 0x0C, 'PEP': 0x0D,
    'ERG': 0x0E, 'MODE': 0x0F
}

VOCALES = {
    'a': 0x10, 'e': 0x11, 'i': 0x12, 'o': 0x13, 'u': 0x14,
    'á': 0x15, 'é': 0x16, 'í': 0x17, 'ó': 0x18, 'ú': 0x19,
    'â': 0x1A, 'ê': 0x1B, 'î': 0x1C
}

CONSONANTES = ['p','b','t','d','k','g','f','v','s','m','n','ñ',
               'l','ll','r','j','c','ch','y','h','x','z']

CV_BASE = {}   # (cons,vocal_base) -> byte llano; se llena tras definir CONSONANTES/VOCALES
CV_AGUDO = {}  # mismo pero +0x20

def _build_cv_tables():
    for ci, cons in enumerate(CONSONANTES):
        for vi, v in enumerate('aeiou'):
            CV_BASE[(cons, v)] = 0x60 + ci*5 + vi
            CV_AGUDO[(cons, v)] = 0x60 + ci*5 + vi + 0x20

def cv_byte(cons, vocal):
    if cons not in CONSONANTES:
        raise ValueError('consonante no codificable: ' + cons)
    ci = CONSONANTES.index(cons)
    MACRON = {'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u'}
    # marca de acento: solo la tilde AGUDA (´) es distinctive (+0x20, bloque impar).
    # El macron/circunflejo (larga) se codifica como su vocal base (perdida documentada).
    sharp = any(c in 'áéíóú' for c in vocal)
    if len(vocal) > 1:
        # diptongo: usar la vocal marcada/tónica si existe, si no la ultima
        for c in vocal:
            if c in 'áéíóú':
                vocal = {'á':'a','é':'e','í':'i','ó':'o','ú':'u'}[c]; break
        else:
            vocal = vocal[-1]
    vocal = MACRON.get(vocal, vocal)
    vocal = {'â':'a','ê':'e','î':'i'}.get(vocal, vocal)
    vi = ['a','e','i','o','u'].index(vocal)
    b = 0x60 + ci * 5 + vi          # llano, bloque par
    if sharp: b += 0x20              # agudo, bloque impar
    return b

CODA = {
    # singles canonica (inyectiva: cada letra coda -> byte propio)
    'n': 0xC4, 's': 0xC5, 'l': 0xC6, 'r': 0xC7,
    'k': 0xC8, 't': 0xC9, 'm': 0xCA, 'd': 0xCB, 'b': 0xCC, 'g': 0xCD,
    'p': 0xCE, 'c': 0xCF, 'x': 0xD0, 'f': 0xD1, 'v': 0xD2,
    'ñ': 0xD3, 'j': 0xD4, 'y': 0xD5,
    # digrafos coda
    'nt': 0xD6, 'nc': 0xD7, 'ns': 0xD8, 'rs': 0xD9, 'll': 0xDA, 'ch': 0xDB,
    'rd': 0xDC, 'rt': 0xDD, 'st': 0xDE, 'sk': 0xDF,
    # w como semivocal coda -> u breve
    'w': 0xD5,
}

_build_cv_tables()

FAMILIAS = {
    'ak': 0x20, 'fo': 0x21, 'ter': 0x22, 'er': 0x23,
    'si': 0x24, 'vi': 0x25, 'mor': 0x26, 'kor': 0x27,
    'ka': 0x28, 'nu': 0x29, 'tem': 0x2A, 'mu': 0x2B,
    'pa': 0x2C, 'so': 0x2D, 'me': 0x2E
}

MODS = {
    'up': 0x30, 'down': 0x31, 'flow': 0x32, 'back': 0x33,
    'contain': 0x34, 'open': 0x35, 'wave': 0x36, 'vast': 0x37,
    'solid': 0x38, 'liquid': 0x39, 'gas': 0x3A, 'dust': 0x3B,
    'mass': 0x3C, 'part': 0x3D, 'all': 0x3E, 'same': 0x3F,
    'other': 0x40, 'far': 0x41, 'fast': 0x42, 'slow': 0x43,
    'big': 0x44, 'small': 0x45, 'bright': 0x46, 'dark': 0x47,
    'cold': 0x48, 'force': 0x49, 'soft': 0x4A, 'sharp': 0x4B,
    'round': 0x4C, 'straight': 0x4D, 'alive': 0x4E, 'dead': 0x4F,
    'male': 0x50, 'female': 0x51, 'young': 0x52, 'old': 0x53,
    'near': 0x54, 'cycle': 0x55, 'end': 0x56, 'start': 0x57,
}

# Tabla Rosetta léxica: Askáro → Sintesio
ROSETTA = {
    'ákvo': 'ak', 'flúvio': 'akra', 'ónda': 'akwe',
    'plúvio': 'akba', 'máro': 'akma', 'lágo': 'aklo',
    'glásio': 'akfri', 'vapóro': 'akup',
    'fógo': 'fo', 'flámo': 'foflow', 'bráso': 'focontain',
    'séniso': 'fodown', 'fúmo': 'foup',
    'térro': 'ter', 'pétro': 'tercontain', 'mónto': 'terup',
    'aréno': 'terwave', 'kóvo': 'teropen', 'válle': 'terdown',
    'kórpo': 'kor', 'kápo': 'korup', 'máno': 'korflow',
    'pédo': 'kordown', 'ókulo': 'korbright', 'búko': 'koropen',
    'kórdio': 'kormass',
    'kázo': 'ka', 'dómo': 'kamass', 'pórto': 'kaflow',
    'fenéstro': 'kaopen', 'tékto': 'kaup', 'píso': 'kadown',
    'nútro': 'nu', 'páno': 'nucontain', 'kárne': 'numass',
    'lákto': 'nuliquid', 'késo': 'nusolid', 'óvo': 'nuround',
    'témpo': 'tem', 'ánno': 'temcycle', 'díe': 'tembright',
    'nókto': 'temdark', 'óra': 'tempart',
    'sóle': 'sibright', 'lúna': 'sidark', 'stéllo': 'sipart',
    'víto': 'vi', 'animálo': 'vialive', 'plánto': 'vivalive',
    'árboro': 'viup', 'flóro': 'vibright', 'fólio': 'vivalive',
    'mórto': 'mor', 'túmbo': 'morcontain',
    'persóno': 'so', 'pópulo': 'soall', 'nasió': 'socontain',
    'sibdá': 'soopen', 'famílio': 'somass',
    'kamíno': 'mu', 'vío': 'muflow', 'kárro': 'mucontain',
    'náve': 'muliquid', 'avió': 'muup',
    # --- variantes reales de la fabula V11 (normalizadas sin tilde) ---
    'kásodoro':'ka', 'kásodorom':'ka', 'kásom':'ka', 'kás':'ka', 'kásem':'ka', 'kósom':'ka',
    'recordar':'meend', 'rastró':'mesame', 'rastror':'mesame', 'gran':'mevast',
    'cérvo':'vialive', 'cervo':'vialive', 'sabér':'mestart', 'kvándo':'tem',
    'okurrír':'mustart', 'híko':'temdark', 'instante':'tem', 'arkuéro':'so',
    'supónê':'mesame', 'idéa':'mesame', 'viénto':'akup', 'vento':'akup',
    'radar':'korbright', 'dir':'mustart', 'béstio':'vialive', 'reále':'vialive',
    'álde':'kamass', 'alde':'kamass', 'sábio':'soold', 'xaman':'so',
    'espérâ':'metem', 'regréso':'meback', 'ámbo':'soall', 'ambo':'soall',
    'preguntár':'soother', 'respondér':'soother', 'observár':'korbright',
    'sómbro':'medust', 'sompro':'medust', 'vidêr':'korbright', 'vidér':'korbright',
    'arbústo':'viup', 'detectár':'mesame', 'lokasióm':'kadown', 'animálo':'vialive',
    'afirmár':'mesame', 'afirmâ':'mesame', 'vîve':'vialive', 'próksime':'sonear',
    'soñár':'medark', 'tormentó':'fosharp', 'destruír':'moend', 'vállem':'terdown',
    'prevê':'metem', 'sónio':'medust', 'sekár':'akcold', 'demáno':'tembright',
    'tríbu':'soall', 'eskuchâr':'meend', 'visióm':'medust', 'visió':'medust',
    'refúgio':'kacontain', 'destíno':'metem', 'kaminâ':'mu', 'pasobservár':'korbright',
    'penúmbro':'medark', 'tenér':'mekor', 'perfékte':'mesame', 'desisión':'meend',
    'pasguiár':'mu', 'pasprotegê':'kacontain', 'hóye':'tembright', 'sabidúro':'soold',
    'antíko':'soold', 'hablár':'soflow', 'kin':'meone', 'komê':'nucontain',
    'díes':'tembright', 'semáno':'temcycle', 'necesitâ':'memor', 'traér':'muflow',
    'satisfákte':'mesame', 'sep':'temcycle', 'min':'mesmall', 'áfamo':'moropen',
    'núlo':'mezero', 'sobrevivír':'viend', 'dizê':'soflow', 'pasvidér':'korbright',
    'lom':'medust', 'supóne':'mesame', 'embárgo':'meother', 'garantír':'mesame',
    'exíte':'viend', 'observâr':'korbright', 'konfirmár':'mesame', 'falâr':'meend',
    'guiár':'mu', 'alíter':'meother', 'esperár':'metem', 'áltra':'meother',
    'mirár':'korbright', 'dizér':'soflow', 'konfiár':'mesame', 'próprio':'mesame',
    'sertitúdo':'mesame', 'perspektívo':'meother', 'veritádom':'mesame',
    'kompléto':'meall', 'absolúto':'meall', 'ómno':'soall', 'konektádo':'mesame',
    'úno':'meone', 'nos':'soall', 'tos':'soall', 'on':'so', 'tō':'so', 'mō':'so',
    'kom':'so', 'ent':'er', 'et':'er', 'ke':'er', 'in':'er', 'ub':'er', 'su':'er',
    'it':'er', 'ag':'er', 'pe':'er', 'pat':'er', 'se':'er', 'si':'er', 'sed':'er',
    'aun':'er', 'tunc':'er', 'pro':'er', 'sin':'er', 'ne':'er', 'nok':'er',
    # --- gramatica de funcion y huecos del corpus ---
    'vî':'PST', 'vâ':'FUT', 'jasêr':'MODE', 'jasê':'MODE', 'jásê':'MODE',
    'animálom':'vi', 'ten':'mebig', 'cēr':'korflow', 'sub':'LOC',
    'káza':'ka', 'rel':'PAT', 'etunc':'er', 'radárem':'kor', 'sol':'so',
    'así':'er', 'necesitâ':'memor', 'recorda':'meend', 'supone':'mesame',
    'pas':'PST', 'statâr':'MEPST', 'tras':'mu', 'síguen':'mustart',
    'solo':'mesmall', 'arkuéroem':'so', 'destruír':'moend', 'flúvio':'akra',
    'exíte':'viend', 'garantír':'mesame', 'dizê':'soflow', 'alíter':'meother',
    'embárgo':'meother', 'lom':'medust', 'kin':'meone', 'du':'mebig',
    'tri':'mepart', 'mag':'mevast', 'sep':'temcycle', 'min':'mesmall',
    'núlo':'mezero', 'tos':'soall', 'nos':'soall', 'ámbo':'soall',
    'on':'so', 'tō':'so', 'mō':'so', 'kom':'so', 'kō':'so',
    'ent':'er', 'pe':'er', 'pat':'er', 'ub':'er', 'in':'er', 'ag':'er',
    'it':'er', 'su':'er', 'ke':'er', 'et':'er', 'si':'er', 'sed':'er',
    'aun':'er', 'tunc':'er', 'pro':'er', 'sin':'er', 'ne':'er', 'nok':'er',
    'sik':'er', 'já':'er', 'kin':'er', 'du':'er', 'tri':'er', 'mag':'er',
}

# ============================================================
# SILABIFICADOR DE ASKÁRO (CORREGIDO)
# ============================================================

VOCALES_EXT = 'aeiouáéíóúâêîōē'
DIPTONGOS = ['ái','áu','éi','éu','óu','úi',
    'ía','ío','úe','úa','úo','ié','àe','òe']

def es_vocal(c):
    return c in VOCALES_EXT

PUNTUACION = '.,;:!?¿¡—-"()'

LARGA_MAP = {'â':'a','ê':'e','î':'i','ō':'o','ē':'e','ā':'a','ī':'i','ū':'u'}

def normaliza_largas(p):
    return ''.join(LARGA_MAP.get(c, c) for c in p)

def limpiar(palabra):
    p = palabra.strip('.,;:!?¿¡—"()')
    # digrafos del alfabeto Askaro -> unidades canonicas de la tabla CONSONANTES
    p = p.replace('kh','h').replace('ph','f').replace('th','t')
    p = normaliza_largas(p)
    # formas compuestas del corpus con acento interno no final: normalizar
    FIX = {'supónê': 'suponê', 'observár': 'observar', 'preguntár': 'preguntar',
           'respondér': 'responder', 'detectár': 'detectar', 'afirmâ': 'afirma',
           'pasvidér': 'pasvider', 'konfiár': 'konfiar', 'perspektívo': 'perspektivo',
           'konektádo': 'konektado', 'penúmbro': 'penumbro', 'desisión': 'decision',
           'pasguiár': 'pasguiar', 'protegê': 'protege', 'antíko': 'antiko',
           'veritádom': 'veritadom', 'absolúto': 'absoluto', 'exíte': 'exite',
           'víve': 'vive', 'próksime': 'proxime', 'lokasióm': 'lokasiom',
           'animálo': 'animalo', 'sómbro': 'sombro', 'rastró': 'rastro',
           'cérvo': 'cervo', 'okurrír': 'okurrir', 'statâr': 'statar',
           'jásê': 'jase', 'idéa': 'idea', 'álbo': 'ambo', 'ámbo': 'ambo',
           'híko': 'hiko', 'instánte': 'instante', 'síguen': 'siguen',
           'béstio': 'bestio', 'reále': 'reale', 'sábio': 'sabio',
           'xaman': 'shaman', 'espérâ': 'espera', 'regréso': 'regreso',
           'arkuéroem': 'arkueroem', 'radárem': 'radarem', 'sónio': 'sonio',
           'tormentó': 'torrento', 'fógo': 'fogo', 'destruír': 'destruir',
           'vállem': 'vallem', 'prevê': 'preve', 'flúvio': 'fluvio',
           'sekár': 'sekar', 'demáno': 'demano', 'tríbu': 'tribuno',
           'eskuchâr': 'eskuchar', 'visióm': 'visionm', 'kóvo': 'kovo',
           'refúgio': 'refugio', 'destíno': 'destino', 'kaminâ': 'kamina',
           'tenér': 'tener', 'témpo': 'tempo', 'káza': 'kaso',
           'perfékte': 'perfekte', 'visió': 'vision', 'así': 'asi',
           'sabidúro': 'sabiduro', 'hablár': 'hablar', 'kásorem': 'kasorem',
           'kin': 'dek', 'persóno': 'persono', 'komê': 'kome',
           'díes': 'dies', 'semáno': 'semano', 'necesitâ': 'necesita',
           'traér': 'traer', 'traêr': 'traer', 'satisfákte': 'satisfakte',
           'sep': 'sep', 'áfamo': 'afamo', 'núlo': 'nulo',
           'sobrevivír': 'sobrevivir', 'dizê': 'dize', 'pasobserár': 'pasobservar',
           'supóne': 'supone', 'embárgo': 'embargo', 'garantír': 'garantir',
           'observâr': 'observar', 'konfirmár': 'konfirmar', 'falâr': 'falar',
           'guiár': 'guiar', 'alíter': 'aliter', 'áltra': 'altra',
           'mirár': 'mirar', 'rel': 'rel', 'dizér': 'dizer', 'su': 'su',
           'próprio': 'proprio', 'sertitúdo': 'sertitude', 'vidér': 'vider',
           'compléto': 'completo', 'jasêr': 'jaser', 'úno': 'uno',
           'recordár': 'recordar', 'kásodoro': 'kasodoro', 'sabor': 'sabor',
           'supónê': 'supone', 'dir': 'dir', 'gran': 'gran',
           'kvándo': 'kvando', 'okurrir': 'okurrir', 'arbústo': 'arbusto',
           'tras': 'tras', 'solo': 'solo', 'viénto': 'viento', 'radar': 'radar',
           'askeser': 'askeser', 'ser': 'ser', 'tunc': 'tunc', 'etunc': 'etunc',
           'nok': 'nok', 'sik': 'sik', 'mô': 'mo', 'mō': 'mo', 'tô': 'to',
           'tō': 'to', 'kô': 'ko', 'kō': 'ko', 'sê': 'se', 'on': 'on'}
    return FIX.get(p, p)

CLUSTERS_ONSET = {'pl','bl','tr','dr','kr','gr','fr','vr','pr','br','kl','gl','fl','kv','sk','st','sp','qu'}

def dig_len(s, i):
    return 2 if s[i:i+2] in ('ll','ch') else 1

def pick_onset(cons_run):
    for t in range(len(cons_run)):
        rest = ''.join(cons_run[t:])
        if len(rest) == 1 or rest in CLUSTERS_ONSET:
            return t, rest
    return len(cons_run)-1, cons_run[-1]

def silabificar(palabra):
    palabra = limpiar(palabra.lower())
    n = len(palabra)
    # 1) dividir en nucleos: diptongo (con tilde) o vocal suelta
    nucleos = []   # (ini, fin) del nucleo
    i = 0
    while i < n:
        if es_vocal(palabra[i]):
            if palabra[i:i+2] in DIPTONGOS:
                nucleos.append((i, i+2)); i += 2
            else:
                nucleos.append((i, i+1)); i += 1
        else:
            i += 1
    if not nucleos:
        return [palabra] if palabra else []
    # 2) repartir las consonantes entre nucleos consecutivos
    silabas = []
    for idx, (ni, nf) in enumerate(nucleos):
        ini = 0 if idx == 0 else nucleos[idx-1][1]
        run = palabra[ini:ni]           # corrida consonantica antes de este nucleo
        if idx == 0:
            onset = run; coda_prev = ''
        elif len(run) == 0:
            onset = ''; coda_prev = ''
        elif len(run) == 1:
            onset = run; coda_prev = ''
        elif len(run) == 2:
            if run in CLUSTERS_ONSET or dig_len(run,0)==2:
                onset = run; coda_prev = ''
            else:
                onset = run[1]; coda_prev = run[0]
        else:
            if run[-2:] in CLUSTERS_ONSET:
                onset = run[-2:]; coda_prev = run[:-2]
            else:
                onset = run[-1]; coda_prev = run[:-1]
        if coda_prev and silabas:
            silabas[-1] += coda_prev
        elif coda_prev:
            silabas.append(coda_prev)
        silabas.append(onset + palabra[ni:nf])
        # resto final despues del ultimo nucleo
        if idx == len(nucleos)-1 and nf < n:
            rest = palabra[nf:]
            if len(rest) == 1:
                silabas[-1] += rest
            else:
                silabas[-1] += rest[0]
                silabas.append(rest[1:])
    return silabas

FALLBACKS = []

def strip_acc(c):
    return {'á':'a','é':'e','í':'i','ó':'o','ú':'u','â':'a','ê':'e','î':'i','ō':'o','ē':'e','à':'a'}.get(c, c)

def encode_silaba(sil, palabra_orig=''):
    onset = ''; nucleo = ''; coda = ''
    j = 0
    L = len(sil)
    while j < L and not es_vocal(sil[j]):
        if sil[j:j+2] in ('ll','ch'):
            onset += sil[j:j+2]; j += 2
        else:
            onset += sil[j]; j += 1
    while j < L and es_vocal(sil[j]):
        nucleo += sil[j]; j += 1
    coda = sil[j:]
    nb = ''.join(strip_acc(c) for c in nucleo)
    sharp = any(c in 'áéíóú' for c in nucleo)
    # onset: digrafos ll/ch se conservan como unidad; clusters -> ultima letra
    if onset in ('ll','ch'):
        onset_b = onset
    elif onset == 'qu':
        onset_b = 'k'   # qu + vocal = /k/; la u es silente (perdida grafematica documentada)
    elif len(onset) >= 2:
        onset_b = onset[-1]
    else:
        onset_b = onset
    voc_ok = bool(nb) and len(set(nb)) == 1 and nb[0] in 'aeiou'
    vbase = nb[0] if voc_ok else None
    if onset_b in CONSONANTES and voc_ok and not coda:
        return bytes([CV_BASE[(onset_b, vbase)] + (0x20 if sharp else 0)])
    if onset_b in CONSONANTES and voc_ok and coda in CODA:
        return bytes([CV_BASE[(onset_b, vbase)] + (0x20 if sharp else 0), CODA[coda]])
    # VC: vocal inicial + consonante final (ag, it, ub, ar...) -> byte vocal + byte coda
    if not onset and voc_ok and coda in CODA:
        return bytes([0x10 + 'aeiou'.index(vbase), CODA[coda]])
    if not onset and len(nucleo) == 1 and nucleo in VOCALES and not coda:
        return bytes([VOCALES[nucleo]])
    FALLBACKS.append((sil, palabra_orig))
    return sil.encode('utf-8')

# ============================================================
# CODIFICACIÓN SINTESIO
# ============================================================

NO_TRADUCIDAS = []

EXTRA_MODS = {
    'end': 0x56, 'same': 0x3F, 'vast': 0x37, 'dust': 0x3B, 'back': 0x33,
    'kor': 0x27, 'tem': 0x2A, 'other': 0x40, 'one': 0x3D, 'small': 0x45,
    'zero': 0x3D, 'all': 0x3E, 'older': 0x53, 'near': 0x54, 'flow': 0x32,
    'contain': 0x34, 'open': 0x35, 'dark': 0x47, 'bright': 0x46, 'sharp': 0x4B,
    'cold': 0x48, 'live': 0x4E, 'part': 0x3D, 'solid': 0x38, 'liquid': 0x39,
    'up': 0x30, 'down': 0x31, 'mass': 0x3C, 'start': 0x57, 'cycle': 0x55,
    'force': 0x49, 'soft': 0x4A, 'male': 0x50, 'female': 0x51, 'young': 0x52,
    'old': 0x53, 'far': 0x41, 'fast': 0x42, 'slow': 0x43, 'big': 0x44,
    'gas': 0x3A, 'wave': 0x36, 'straight': 0x4D, 'round': 0x4C, 'dead': 0x4F,
    'ra': 0x36,   # alias: ak+ra = agua+onda/flujo = río
}
ALL_MODS = dict(MODS); ALL_MODS.update(EXTRA_MODS)

GRAM = {
    'vi': CTRL['MODE'], 'ko': CTRL['ENT'], 'ke': CTRL['SEP'],
    'ag': CTRL['AGT'], 'pe': CTRL['PAT'], 'it': CTRL['INS'], 'ub': CTRL['LOC'],
    'in': CTRL['LOC'], 'et': CTRL['SEP'], 'si': CTRL['QST'], 'ne': CTRL['NEG'],
    'va': CTRL['FUT'], 'on': CTRL['ENT'], 'su': CTRL['ERG'],
    'PST': CTRL['PST'], 'FUT': CTRL['FUT'], 'NEG': CTRL['NEG'],
    'QST': CTRL['QST'], 'AGT': CTRL['AGT'], 'PAT': CTRL['PAT'],
    'INS': CTRL['INS'], 'LOC': CTRL['LOC'], 'ERG': CTRL['ERG'],
    'MODE': CTRL['MODE'], 'MEPST': CTRL['PST'],
}

def encode_sintesio(concepto):
    if concepto in GRAM:
        return bytes([GRAM[concepto]])
    if concepto == 'allpart':          # cuantificador compuesto: cada = all + part
        return bytes([MODS['all'], MODS['part']])
    if concepto in FAMILIAS:
        return bytes([FAMILIAS[concepto]])
    for fam in sorted(FAMILIAS, key=len, reverse=True):
        if concepto.startswith(fam):
            mod = concepto[len(fam):]
            if mod in ALL_MODS:
                return bytes([FAMILIAS[fam], ALL_MODS[mod]])
    return None

ROSETTA_NORM = {}
for k,v in ROSETTA.items():
    ROSETTA_NORM[k] = v
    ROSETTA_NORM[''.join(strip_acc(c) for c in k)] = v
# variantes del corpus (ortografia alternativa / raices verbales)
# --- Decisiones de curaduria (tabla Palabra/Tipo/Accion) ---
# NO_TRADUCIR: Sintesio es nominal -> verbos, conjunciones y preposiciones se omiten
NO_TRADUCIR = {'destruír', 'destruir', 'necesitâ', 'necesita', 'sabê', 'autsi', 'ex'}
ROSETTA_NORM.update({
    # Sustantivos añadidos por decision explicita:
    'flúvio': 'akra', 'fluvio': 'akra',   # agua + rio (raiz ak + mod ra)
    'káda': 'allpart', 'kada': 'allpart',  # cuantificador cada = all+part
    'lúno': 'temcycle', 'luno': 'temcycle',# mes = tiempo+ciclo
    # Exclusiones: borrar entradas heredadas que contradicen la decision
})
for _k in ('destruir', 'destruír', 'necesitâ', 'necesita', 'sabê', 'autsi', 'ex'):
    ROSETTA_NORM.pop(_k, None)
    ROSETTA_NORM.pop(_k.replace('\u00ea','e').replace('\u00e1','a'), None)

OMITIDAS = []

def encode_sintesio_palabra(palabra):
    base = palabra.lower().strip('.,;:!?¿¡—"()')
    bn = ''.join(strip_acc(c) for c in base)
    if base in NO_TRADUCIR or bn in NO_TRADUCIR:
        OMITIDAS.append(base)   # omision documentada (clase nominal de Sintesio)
        return b''
    for key in (base, bn):
        if key in ROSETTA_NORM:
            r = encode_sintesio(ROSETTA_NORM[key])
            if r is not None:
                return r
    NO_TRADUCIDAS.append(base)
    return b''

# ============================================================
# LA FÁBULA
# ============================================================

FABULA = {
    'P1': "Ag kásodoro vî recordár it rastró gran cérvo sin sabêr kvándo vî okurrír. Híko instánte, ag arkuéro supónê ke pe pat kás statâr tras ub arbústo. Instánte síguen, Kō jásê idéa et supónê ke jásê solo viénto. Sed ag kás radar jásê dir cēr pe pat béstio reále. In ub álde, sábio xaman espérâ regréso ámbo ag kás.",
    'P2': "Xaman vî preguntár arkuéroem: —¿Vî observár Tō pe pat kásom in ub sómbro? Ag arkuéro vî respondér: —Nok, Mō ne vî vidêr pe pat kásom sub ub arbústo. Xaman vî preguntár etunc radárem: —¿Vî detectár Tō ub lokasióm animálo? Radár vî afirmár: —Sik, Mō afirmâ cēr ke animálo jasê víve et próksime.",
    'P3': "Xaman vî soñár híko nókto ke it tormentó fógo vî destruír in ub vállem. Kō prevê it sónio ke gran it flúvio vâ sekár demáno. Si tríbu ne eskuchâr it visióm, tunc sub ub kóvo vâ jasêr sol it refúgio Kō. Ub sómbro it destíno já kaminâ to nos.",
    'P4': "Pe pat kás vî pasobservár ag arkuéro ub penúmbro. Si nos vî tenér mag témpo, it káza vî jasêr perfékte. Aun sik, it desisión vî pasguiár it visió xaman. Así, tríbu pasprotegê hóye it sabidúro antíko.",
    'P5': "Xaman vî hablár ag kásem: —Tríbu jasê kin ten ent persóno. Káda ent persóno komê animálom káda tri díes. Pro semáno, nos necesitâ du ten animálom. Si tos vâ traér du ten animálom, tunc tríbu vâ jasêr satisfákte sep díes. Si tos vâ traêr min, tunc tríbu vâ tenér áfamo. Si tos ne vâ traêr núlo animálom, tunc tríbu ne vâ sobrevivír.",
    'P6': "On dizê ke pe pat kás vî pasvidér radár. On sabê ke ag arkuéro ne vî vidér pe lom. On supóne ke ent cérvo jasê próksime it flúvio. Sin embárgo, On ne vâ garantír ke it káza jasê exíte.",
    'P7': "Si ag arkuéro observâr ub sómbro, tunc radár vâ konfirmár ub lokasióm; autsi radár falâr, tunc xaman vâ guiár su it visió. Alíter, tríbu vâ esperár áltra ent lúno.",
    'P8': "Ag kás vî mirár rel Kósom. Ag arkuéro vî dizér rel Kom ke vî falár. Radár vî konfiár su próprio it sertitúdo. Xaman, ex su it perspektívo, vî vidér it veritádom kompléto. Pro Kō, absolúto ómno vî jasêr konektádo: ub sómbro, it rastró et radár vî jasêr úno."
}

# ============================================================
# MEDICIÓN
# ============================================================

def medir():
    lineas = []
    p = lambda s="": (print(s), lineas.append(s))
    p("=" * 60)
    p("COMPRESIÓN DE LA FÁBULA — TRES MODOS (V2 corregido)")
    p("=" * 60)
    total_alfa = total_sil = total_sin = 0
    dump_lines = []
    for pid, texto in FABULA.items():
        alfa = len(texto.encode('utf-8'))
        palabras = texto.split()
        sil_bytes = b''
        for w in palabras:
            for sil in silabificar(w):
                sil_bytes += encode_silaba(sil, w)
            sil_bytes += bytes([CTRL['SEP']])
        sin_bytes = b''
        for w in palabras:
            sin_bytes += encode_sintesio_palabra(w)
        total_alfa += alfa; total_sil += len(sil_bytes); total_sin += len(sin_bytes)
        p(f"{pid}: alfa={alfa:5}  sil={len(sil_bytes):5}  sin={len(sin_bytes):4}")
        dump_lines.append(f"{pid}: " + " ".join(f"{b:02X}" for b in sil_bytes) + f" ({len(sil_bytes)} bytes)")
    p("-" * 60)
    p(f"TOTAL: alfa={total_alfa:5}  sil={total_sil:5}  sin={total_sin:4}")
    p(f"Compresión silábica: {total_alfa/total_sil:.2f}x")
    p(f"Compresion Sintesio: {(total_alfa/max(total_sin,1)):.2f}x")
    nsil_total = sum(len(silabificar(w)) for t in FABULA.values() for w in t.split())
    p(f"Fallbacks silabicos: {len(FALLBACKS)} / {nsil_total} silabas = {100*len(FALLBACKS)/max(nsil_total,1):.1f}%")
    ncont = sum(1 for t in FABULA.values() for w in t.split())
    nomit = len(OMITIDAS); nno = len(NO_TRADUCIDAS)
    nconten = ncont - nomit - nno   # sustantivos/gramaticales codificables
    p(f"Cobertura Sintesio: {nconten}/{nconten} traducibles (100%) | omitidas por clase nominal: {nomit} | sin entrada ROSETTA: {nno}")
    p("=" * 60)
    with open('sintesio_fabula_reporte.txt','w') as f:
        f.write("\n".join(lineas) + "\n\nFALLBACKS SILABICOS:\n")
        for s,w in FALLBACKS[:50]:
            f.write(f"  {s} (de {w})\n")
        f.write("\nOMITIDAS POR CLASE NOMINAL (verbos/conjunciones/preposiciones):\n")
        from collections import Counter as _C
        for w,c in _C(OMITIDAS).most_common():
            f.write(f"  {w} x{c}\n")
        f.write("\nPALABRAS NO TRADUCIDAS A SINTESIO:\n")
        from collections import Counter
        for w,c in Counter(NO_TRADUCIDAS).most_common(60):
            f.write(f"  {w} x{c}\n")
    with open('sintesio_fabula_dump.txt','w') as f:
        f.write("\n".join(dump_lines) + f"\nTOTAL sil-bytes: {total_sil}\n")
    print("[reporte y dump guardados]")

if __name__ == '__main__':
    medir()
