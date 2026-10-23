src = open('sintesio_fabula_test.py').read()

# --- A) reemplazar silabificador por version que reparte clusters correctamente ---
a = src.index("def silabificar")
b = src.index("FALLBACKS = []")
new_sil = '''CLUSTERS_ONSET = {'pl','bl','tr','dr','kr','gr','fr','vr','pr','br','kl','gl','fl','kv','sk','st','sp'}

def dig_len(s, i):
    return 2 if s[i:i+2] in ('ll','ch') else 1

def silabificar(palabra):
    palabra = palabra.lower().strip(PUNTUACION)
    silabas = []
    n = len(palabra)
    i = 0
    while i < n:
        onset = ''
        # consumir consonantes hasta la primera vocal; si hay 2+ consonantes antes de la
        # siguiente vocal, la primera queda como coda de la SILABA ANTERIOR (ya emitida),
        # asi que aqui solo tomamos el cluster completo cuando es onset valido o una sola C.
        cons_run = []
        j = i
        while j < n and not es_vocal(palabra[j]):
            d = dig_len(palabra, j)
            cons_run.append(palabra[j:j+d]); j += d
        k = 0
        if cons_run:
            if len(cons_run) == 1:
                onset = cons_run[0]; k = 1
            else:
                # buscar division: ultima(s) forman cluster -> las demas son coda anterior
                for t in range(len(cons_run)):
                    rest = ''.join(cons_run[t:])
                    if len(rest) == 1 or rest in CLUSTERS_ONSET:
                        onset = rest; k = t; break
                    if len(rest) == 2 and rest[0] == 'k' and False:
                        pass
                else:
                    onset = cons_run[-1]; k = len(cons_run)-1
            # NOTA: consonantes sobrantes al inicio de palabra se unen al onset igualmente
            if i == 0:
                onset = ''.join(cons_run); k = len(cons_run)
        i += sum(len(x) for x in cons_run[:k]) if cons_run else 0
        # nucleo
        nucleo = ''
        if i < n:
            if palabra[i:i+2] in DIPTONGOS:
                nucleo = palabra[i:i+2]; i += 2
            elif es_vocal(palabra[i]):
                nucleo = palabra[i]; i += 1
        # coda: exactamente una grafia si luego hay vocal o fin de palabra
        coda = ''
        if i < n and not es_vocal(palabra[i]):
            d = dig_len(palabra, i)
            nxt = palabra[i+d] if i+d < n else ''
            if nxt == '' or es_vocal(nxt):
                coda = palabra[i:i+d]; i += d
        if onset or nucleo or coda:
            silabas.append(onset + nucleo + coda)
        elif not onset and not nucleo and not coda:
            break
    return silabas

'''
src = src[:a] + new_sil + src[b:]

# --- B) CODA con digrafos, sin None ---
old = """CODA = {'n': 0xC4, 's': 0xC5, 'l': 0xC6, 'r': 0xC7,
        'k': 0xC8, 't': 0xC9, 'm': 0xCA,
        # extension: codas reales del corpus askarano mapeadas al punto de articulacion mas cercano
        'd': 0xC9, 'b': 0xC8, 'z': 0xC5, 'x': 0xC8, 'g': 0xC8, 'p': 0xC8, 'f': 0xC5, 'v': 0xC5, 'ñ': 0xC4, 'j': 0xC4, 'c': 0xC8, 'h': None}"""
new = """CODA = {'n': 0xC4, 's': 0xC5, 'l': 0xC6, 'r': 0xC7,
        'k': 0xC8, 't': 0xC9, 'm': 0xCA,
        # extension: codas del corpus mapeadas al punto de articulacion mas cercano
        'd': 0xC9, 'b': 0xC8, 'z': 0xC5, 'x': 0xC8, 'g': 0xC8, 'p': 0xC8,
        'f': 0xC5, 'v': 0xC5, 'ñ': 0xC4, 'j': 0xC4, 'c': 0xC8, 'w': 0xC8,
        'y': 0xC4, 'll': 0xC6, 'ch': 0xC8}"""
assert old in src, "CODA no encontrado"
src = src.replace(old, new)

# --- C) encode_silaba: colapsar clusters de onset a su nuclear y aceptar nucleos tildados/diptongos ---
a = src.index("def encode_silaba")
b = src.index("# ============================================================\n# CODIFICACIÓN SINTESIO")
new_enc = '''def encode_silaba(sil, palabra_orig=''):
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
    # onset base: cluster -> ultima grafia; digrafo se conserva
    if len(onset) >= 2 and onset not in ('ll','ch'):
        onset_b = onset[-1] if onset[-1] in CONSONANTES else onset
    else:
        onset_b = onset
    voc_ok = bool(nb) and all(c in 'aeiou' for c in nb)
    if onset_b in CONSONANTES and voc_ok and not coda:
        return bytes([cv_byte(onset_b, nb)])
    if onset_b in CONSONANTES and voc_ok and coda in CODA:
        return bytes([cv_byte(onset_b, nb), CODA[coda]])
    if not onset and len(nucleo) == 1 and nucleo in VOCALES and not coda:
        return bytes([VOCALES[nucleo]])
    FALLBACKS.append((sil, palabra_orig))
    return sil.encode('utf-8')

'''
src = src[:a] + new_enc + src[b:]

open('sintesio_fabula_test.py','w').write(src)
print("patch aplicado")
