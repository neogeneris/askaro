src = open('sintesio_fabula_test.py').read()

a = src.index("CLUSTERS_ONSET")
b = src.index("FALLBACKS = []")
new_sil = '''CLUSTERS_ONSET = {'pl','bl','tr','dr','kr','gr','fr','vr','pr','br','kl','gl','fl','kv','sk','st','sp'}

def dig_len(s, i):
    return 2 if s[i:i+2] in ('ll','ch') else 1

def pick_onset(cons_run):
    for t in range(len(cons_run)):
        rest = ''.join(cons_run[t:])
        if len(rest) == 1 or rest in CLUSTERS_ONSET:
            return t, rest
    return len(cons_run)-1, cons_run[-1]

def silabificar(palabra):
    palabra = palabra.lower().strip(PUNTUACION)
    silabas = []
    n = len(palabra)
    i = 0
    while i < n:
        onset = ''
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
        else:
            break
    return silabas

'''
src = src[:a] + new_sil + src[b:]
open('sintesio_fabula_test.py','w').write(src)
print("ok")
