src = open('sintesio_fabula_test.py').read()
code = src[:src.index("# ============================================================\n# LA FÁBULA")]
ns = {}
exec(code, ns)
silabificar = ns['silabificar']
tests = ['espérâ','regréso','statâr','recordár','okurrír','supónê','kásodoro','tríbu','álde','—¿vî','vidêr','afirmâ','desisión','konektádo','xaman','radar','síguen','instánte','arkuéroem:']
for w in tests:
    print(w, '->', silabificar(w))
print("FIN OK")
