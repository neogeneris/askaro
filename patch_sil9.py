src = open('sintesio_fabula_test.py').read()

a = src.index("def silabificar")
b = src.index("FALLBACKS = []")
new_sil = '''def silabificar(palabra):
    palabra = palabra.lower().strip(PUNTUACION)
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

'''
src = src[:a] + new_sil + src[b:]
open('sintesio_fabula_test.py','w').write(src)
print("ok")
