src = open('sintesio_fabula_test.py').read()

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
    prev_silaba = None   # indice de la ultima silaba emitida
    while i < n:
        # --- recolectar corrida de consonantes antes de la siguiente vocal ---
        cons_run = []
        j = i
        while j < n and not es_vocal(palabra[j]):
            d = dig_len(palabra, j)
            cons_run.append(palabra[j:j+d]); j += d
        # --- decidir onset (el resto va a la coda de la silaba anterior) ---
        onset = ''
        if cons_run:
            if j >= n:                      # sin vocal despues -> todo al onset (resto final)
                onset = ''.join(cons_run); k = len(cons_run)
            elif len(cons_run) == 1:
                onset = cons_run[0]; k = 1
            elif prev_silaba is None:       # inicio de palabra: cluster completo al onset
                onset = ''.join(cons_run); k = len(cons_run)
            else:
                # buscar el mayor sufijo que sea onset valido (cluster o C suelta)
                for t in range(len(cons_run)):
                    rest = ''.join(cons_run[t:])
                    if rest in CLUSTERS_ONSET or len(rest) == 1:
                        onset = rest; k = t; break
                else:
                    onset = cons_run[-1]; k = len(cons_run)-1
            # consonantes NO consumidas -> coda de la silaba anterior
            leftover = ''.join(cons_run[:k])
            if leftover and prev_silaba is not None:
                silabas[prev_silaba] += leftover
            i += sum(len(x) for x in cons_run[:k])
        else:
            k = 0
        # --- nucleo ---
        nucleo = ''
        if i < n:
            if palabra[i:i+2] in DIPTONGOS:
                nucleo = palabra[i:i+2]; i += 2
            elif es_vocal(palabra[i]):
                nucleo = palabra[i]; i += 1
        if onset or nucleo:
            silabas.append(onset + nucleo)
            prev_silaba = len(silabas) - 1
        else:
            break
    return silabas

'''
src = src[:a] + new_sil + src[b:]
open('sintesio_fabula_test.py','w').write(src)
print("silabificador reescrito")
