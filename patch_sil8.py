src = open('sintesio_fabula_test.py').read()

# DIPTONGOS: solo formas con tilde (hiato askarano separa vocales sin tilde)
old = """DIPTONGOS = ['ai','au','ei','eu','ou','ui',
    'ái','áu','éi','éu','óu','úi','ài','òu',
    'ia','io','iu','ua','ue','uo',
    'ía','ío','úe','úa','úo','ié']"""
new = """DIPTONGOS = ['ái','áu','éi','éu','óu','úi',
    'ía','ío','úe','úa','úo','ié','àe','òe']"""
assert old in src; src = src.replace(old, new)

# silabificador con guardas anti-bucle
a = src.index("def silabificar")
b = src.index("FALLBACKS = []")
new_sil = '''def silabificar(palabra):
    palabra = palabra.lower().strip(PUNTUACION)
    silabas = []
    n = len(palabra)
    i = 0
    while i < n:
        inicio = i
        onset = ''
        k = 0
        if not es_vocal(palabra[i]):
            cons_run = []
            j = i
            while j < n and not es_vocal(palabra[j]):
                d = dig_len(palabra, j)
                cons_run.append(palabra[j:j+d]); j += d
            if j >= n:                      # resto final consonantico -> coda de la ultima silaba
                leftover = ''.join(cons_run)
                if silabas:
                    silabas[-1] += leftover
                else:
                    silabas.append(leftover)
                break
            if len(cons_run) == 1:
                onset = cons_run[0]; k = 1
            elif not silabas:               # inicio de palabra: cluster completo al onset
                onset = ''.join(cons_run); k = len(cons_run)
            else:
                k, onset = pick_onset(cons_run)
                leftover = ''.join(cons_run[:k])
                if leftover:
                    silabas[-1] += leftover   # coda de la silaba anterior
            i += sum(len(x) for x in cons_run[:k])
        nucleo = ''
        if i < n:
            if palabra[i:i+2] in DIPTONGOS:
                nucleo = palabra[i:i+2]; i += 2
            elif es_vocal(palabra[i]):
                nucleo = palabra[i]; i += 1
        if onset or nucleo:
            silabas.append(onset + nucleo)
        if i <= inicio:                     # guarda anti-bucle
            i = inicio + 1
    return silabas

'''
src = src[:a] + new_sil + src[b:]
open('sintesio_fabula_test.py','w').write(src)
print("ok")
