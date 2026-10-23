import re, unicodedata

VOWELS = 'aeiouáéíóúâêîôûà'

def askarizar(palabra):
    """Aplica las reglas ortográficas de Askâro:
    - c suave (ante e/i), z, s -> s ; c fuerte -> k
    - ch -> c ; qu -> k ; gu -> g ; g siempre fuerte
    - h -> x (suena como j española)  [según ciclo 9: j->x]
    - ll, ñ, rr se conservan; y -> i
    - f inicial -> f; v -> v
    - tildes explícitas en palabras con >=2 vocales (regla del usuario)
    """
    w = palabra.lower().strip()
    # ch -> c (sonido africado propio de la c askâra)
    w = w.replace('ch','c')
    # qu -> k, gu+e/i -> g
    w = re.sub(r'qu','k',w)
    w = re.sub(r'g([ei])',r'g\1',w)  # g siempre fuerte: mantener g
    # c: suave ante e,i -> s ; fuerte -> k
    out=[]
    for i,chr_ in enumerate(w):
        if chr_=='c':
            nxt = w[i+1] if i+1<len(w) else ''
            out.append('s' if nxt in 'ei' else 'k')
        elif chr_=='z':
            out.append('s')
        elif chr_=='h':
            out.append('x')   # h suena como j española -> escrita x? 
        elif chr_=='v' :
            out.append('v')
        elif chr_=='y':
            out.append('i')
        elif chr_=='j':
            out.append('x')   # j francesa
        else:
            out.append(chr_)
    w=''.join(out)
    return w

def vocal_count(w):
    return sum(1 for c in w if c in VOWELS)

def tilde_pos(w):
    """Regla del usuario: tilde explícita si >=2 vocales.
    Palabras esdrújulas/llanas: marcar la vocal tónica por posición desde el final.
    Heurística: contar secuencias vocálicas; tónica = penúltima vocal si termina en
    vocal/n/s, antepenúltima si consonante final o acento etimológico conocido."""
    idx=[i for i,c in enumerate(w) if c in VOWELS]
    if len(idx)<2: return None,None
    last=w[-1]
    tonica = idx[-2] if last in VOWELS+'nsxz' else idx[-3] if len(idx)>=3 else idx[-2]
    return tonica, ''.join(w[tonica]+'́' if False else '')  # placeholder
