#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sufijos_askaro.py — Reemplazo de sufijos por los SUFIJOS FIJADOS de Askáro.

Recorre la base léxica (askaro_lexico.db :: tabla lexico, 1404 términos) y, para cada
palabra que contiene un sufijo derivativo, reescribe la terminación con el sufijo
fijado aplicando las reglas de derivación y acentuación:

  R1  Infinitivo = raíz + vocal temática con circunflejo (-âr / -êr / -îr), tónica;
      sin otra tilde en el infinitivo.
  R2  Raíz del infinitivo = infinitivo sin la -r final (kortâr -> kortâ-).
  R3  El sufijo se añade a la raíz CON su vocal temática (la temática conserva el
      circunflejo): kortâ- + -ble -> kortâble ; dormî- + -dorio -> dormîdório.
  R4  La tónica del derivado se marca con tilde aguda y es siempre explícita.
  R5  Sufijo TÓNICO -> aguda dentro del sufijo: -dór, -dório, -sión, -ménto, -tád, -róso.
  R6  Sufijo ÁTONO -> la tónica es la vocal temática (â/ê/î), que ya lleva circunflejo
      y NO recibe aguda: kortâble, amâble, audîble.
  R7  -oso verbal -> -róso sobre la temática (kortâróso); -oso nominal -> directo a la
      raíz nominal (fóko -> fokóso).
  R8  -sión/-ión se añaden a la temática; si la raíz acaba en vocal se mantiene la
      temática (nasîr -> nasîón).
  R9  Una sola forma por función: nunca -tor junto a -dor, nunca -miento junto a -mento.
  R10 Colisión con palabra existente o significado distinto -> se conserva la forma
      original y se marca importación / excepción.

Salidas:
  * CSV   : reemplazo_sufijos.csv  (Original | Raíz | Sufijo | Forma Askáro | Glosa | Nota)
  * BD    : tabla nueva `sufijos_askaro` + columna nueva `lexico.termino_sufijado`
            (el campo canon `termino_askaro` NO se toca: auditoría no destructiva)

Uso:
  python3 sufijos_askaro.py           # dry-run
  python3 sufijos_askaro.py --apply   # escribe en askaro_lexico.db
"""
import sqlite3, re, sys, csv
from collections import Counter

DB       = "askaro_lexico.db"
CSV_OUT  = "reemplazo_sufijos.csv"
APPLY    = "--apply" in sys.argv

AGUDAS   = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
CIRCUN   = {"â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u"}
DESACC   = str.maketrans({**AGUDAS, **CIRCUN})
def desacc(w): return (w or "").translate(DESACC)

# ------------------------------------------------------------------ tabla de sufijos fijados
# clave interna -> (sufijo_fijado_mostrar, funcion, tonico, terminaciones_obsoletas_a_cortar)
SUF = {
    "dor":   ("-dor",   "agente/instrumento",  True,  [r"(?:at|it|ut|ent|skript|serv|ekv|tratt|eskav|komput|gubern|giok|ten|dokt|aut|akt)[óo]r[oa]?$",
                                                       r"(?:ador|edor|idor|otor|utor|tor)[oa]?$"]),
    "dorio": ("-dorio", "lugar/resultado",     True,  [r"(?:torio|sorio|dorio)[óí]?o?$"]),
    "sion":  ("-sión",  "acción/resultado",    True,  [r"(?:ción|sión|sio|syon|tion|tsio|zio)(?:ne)?$"]),
    "mento": ("-mento", "instrumento/resultado",True, [r"(?:miento|mento)$"]),
    "tad":   ("-tad",   "cualidad abstracta",  True,  [r"(?:dad|tad|tud|dáto|táto|dat|tat)$"]),
    "roso":  ("-róso",  "adjetivo 'lleno de'", True,  [r"(?:óso|óse|ósa|ose)$"]),
    "oso":   ("-oso",   "adjetivo 'lleno de'", False, [r"(?:oso|osa)$"]),
    "ismo":  ("-ismo",  "doctrina",            False, [r"(?:ísmo|ismo)$"]),
    "ista":  ("-ista",  "partidario/profesional", False, [r"(?:ísto|ísta|ista|iste|íst[oa])$"]),
    "able":  ("-able",  "que puede ser",       False, [r"(?:íle|ile|ble|bile|able)$"]),
    "ible":  ("-ible",  "que puede ser",       False, [r"(?:íle|ile|ble|bile|ible)$"]),
    "ia":    ("-ia",    "ciencia/arte",        False, [r"(?:íe|ía|ie)$"]),
    "isar":  ("-isar",  "verbo causativo",     False, [r"(?:isar|izar|esar|ísar)$"]),
    "ificar":("-ificar","verbo causativo",     False, [r"(?:ificar|ifíkár|ifikar)$"]),
    "etto":  ("-etto",  "diminutivo",          False, [r"(?:étto|etto|etta|otto|eto|ita|illa|illo)$"]),
}
FORMA_TONICA  = {"dor": "dór", "dorio": "dório", "sion": "sión", "mento": "ménto",
                 "tad": "tád", "roso": "róso"}
FORMA_ATONA   = {"oso": "óso", "ismo": "ísmo", "ista": "ísta", "able": "ble",
                 "ible": "ble", "ia": "ia", "isar": "sar", "ificar": "fikar",
                 "etto": "tto"}

# ------------------------------------------------------------------ detección
def detectar(forma):
    """Devuelve (clave_sufijo, raiz_visible, sufijo_actual_detectado) o None."""
    if not forma or " " in forma.strip():
        return None
    for clave, (canon, fn, tonico, pats) in SUF.items():
        for rx in pats:
            m = re.search(rx, forma, re.I)
            if m and m.start() >= 3:                      # exige raíz de al menos 3 letras
                return clave, forma[:m.start()], m.group(0)
    return None

# ------------------------------------------------------------------ verbo base (para temática)
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
rows = list(con.execute("select * from lexico order by id"))

TEMAS = {"a": "â", "e": "ê", "i": "î"}
RAICES_VERBALES = {}          # raiz(sin tilde) -> tematica
for r in rows:
    if r["clase_gramatical"] == "Verbo" and r["termino_askaro"]:
        m = re.match(r"^(.+?)(ar|er|ir)$", desacc(r["termino_askaro"]).lower())
        if m:
            RAICES_VERBALES[m.group(1)] = TEMAS[m.group(2)[-1]]

EXISTENTES = {}               # forma normalizada -> ids (para detectar colisiones)
for r in rows:
    if r["termino_askaro"]:
        EXISTENTES.setdefault(desacc(r["termino_askaro"]).lower(), set()).add(r["id"])

def tematica_de(raiz):
    """Tematica (-âr/-êr/-îr) si la raiz proviene de un verbo del léxico."""
    low = desacc(raiz).lower()
    best = None
    for vr, tema in RAICES_VERBALES.items():
        if low == vr or low.startswith(vr) and len(vr) >= 3:
            if best is None or len(vr) > len(best[0]):
                best = (vr, tema)
    return best

def un_solo_acento(w):
    """Regla R4/R5/R6: exactamente una tilde aguda (la tónica); circunflejos intactos."""
    idxs = [i for i, c in enumerate(w) if c in AGUDAS]
    if len(idxs) <= 1:
        return w
    keep = idxs[-1]                       # la tónica es la última aguda (sufijo o temática)
    return "".join(AGUDAS[c] if (c in AGUDAS and i != keep) else c for i, c in enumerate(w))

def derivar(clave, raiz, forma_original):
    """Construye la forma askara normativizada a partir de raiz + sufijo fijado."""
    canon, fn, tonico, _ = SUF[clave]
    tv = tematica_de(raiz)
    raiz_limpia = re.sub(r"[áéíóú]$", lambda m: AGUDAS[m.group(0)], raiz)  # quita aguda de la raiz
    if clave == "roso":
        # R7 verbal: raiz del infinitivo con temática + -róso
        if tv:
            base = raiz_limpia.rstrip() + tv[1]
        else:
            base = raiz_limpia.rstrip()
        suf = FORMA_TONICA["roso"]
    elif tonico:
        base = (raiz_limpia.rstrip() + tv[1]) if tv else raiz_limpia.rstrip()
        suf = FORMA_TONICA[clave]
    else:
        # R6: sufijo atono -> la tónica queda en la temática (circunflejo, sin aguda)
        if tv:
            base = raiz_limpia.rstrip() + tv[1]
        else:
            base = raiz_limpia.rstrip()
            if base and base[-1] in "aeiou":
                base = base[:-1] + TEMAS[base[-1]]      # temática explícita
        suf = FORMA_ATONA[clave]
    nueva = un_solo_acento(base + suf)
    return nueva, canon, (tv[1] if tv else None)

def clasificar_nota(r, nueva, canon):
    """R10: colisión / importación / excepción."""
    col = {i for i in EXISTENTES.get(desacc(nueva).lower(), set()) if i != r["id"]}
    if col:
        return f"excepción (colisión con {', '.join(sorted(col)[:2])}; se mantiene '{r['termino_askaro']}')"
    origen = (r["origen_etimologia"] or "").lower()
    if r["status"] == "Fusionada":
        return f"excepción (duplicado fusionado; se mantiene '{r['termino_askaro']}')"
    if "préstamo" in origen or "loanword" in origen or "import" in origen:
        return f"importación (se mantiene '{r['termino_askaro']}')"
    if canon == "-tad" and (r["espanol"] or "").lower() in {
        "vinagre", "papa", "soldado", "estado", "dato", "resultado", "municipio",
        "ciudad", "presidento", "senado"}:
        return f"excepción (raíz no abstracta; se mantiene '{r['termino_askaro']}')"
    if canon == "-dorio" and (r["espanol"] or "").lower() in {
        "historia", "victoria", "teoria", "memoria informatica", "euforia"}:
        return f"excepción (sustantivo en -ia/-oría, no lugar; se mantiene '{r['termino_askaro']}')"
    if canon == "-oso" and (r["espanol"] or "").lower() in {"cosa", "algo", "celos", "dosis"}:
        return f"excepción (léxico primitivo, no derivado; se mantiene '{r['termino_askaro']}')"
    if canon == "-ista" and (r["espanol"] or "").lower() in {"revista", "entrevista", "impuesto"}:
        return f"excepción (participio, no partidario; se mantiene '{r['termino_askaro']}')"
    if canon in ("-able", "-ible") and (r["espanol"] or "").lower() in {"debil", "facil", "dificil"}:
        return f"excepción (adjetivo primitivo, no 'que puede ser'; se mantiene '{r['termino_askaro']}')"
    if canon == "-ia" and (r["espanol"] or "").lower() in {"necesario", "maldad", "fuerza",
                                                           "ignorancia", "valentia", "paciencia",
                                                           "hipocresia", "injusticia"}:
        return f"excepción (cualidad: va con -tad, no -ia; se mantiene '{r['termino_askaro']}')"
    return "regular"

# ------------------------------------------------------------------ recorrido
tabla = []
stats = Counter()
for r in rows:
    det = detectar(r["termino_askaro"])
    if not det:
        continue
    clave, raiz, suf_actual = det
    nueva, canon, tema = derivar(clave, raiz, r["termino_askaro"])
    nota = clasificar_nota(r, nueva, canon)
    stats[canon] += 1
    stats[nota.split()[0]] += 1
    tabla.append(dict(id=r["id"], original=r["termino_askaro"], raiz=raiz,
                      sufijo_actual=suf_actual, sufijo=canon, forma=nueva,
                      glosa=r["espanol"], nota=nota, clase=r["clase_gramatical"]))

# correccion sistematica R5 en derivados -dor: rematan en 'dor' átono -> 'dór' tónico
dor_fix = [(r["id"], r["derivado_dor"], r["derivado_dor"][:-3] + "dór")
           for r in rows
           if r["derivado_dor"] and len(r["derivado_dor"]) > 4
           and r["derivado_dor"].endswith("dor") and not r["derivado_dor"].endswith("dór")]

# ------------------------------------------------------------------ informe
print("=" * 96)
print("REEMPLAZO DE SUFIJOS FIJADOS EN ASKÁRO — askaro_lexico.db :: lexico")
print("=" * 96)
print(f"Términos analizados .......: {len(rows)}")
print(f"Términos con sufijo derivativo .: {len(tabla)}")
print(f"Correcciones de tonicidad -dor -> -dór (derivado_dor): {len(dor_fix)}")
print("\nPor sufijo fijado:", {k: v for k, v in stats.items() if k.startswith('-')})
print("Por nota        :", {k: v for k, v in stats.items() if not k.startswith('-')})

print("\n--- TABLA (Original | Raíz | Sufijo | Forma Askáro | Glosa | Nota) ---")
hdr = ("Original", "Raíz", "Sufijo actual", "Sufijo", "Forma Askáro", "Glosa", "Nota")
print("{:<20}{:<16}{:<14}{:<9}{:<20}{:<20}{}".format(*hdr))
print("-" * 118)
for x in tabla:
    print("{:<20}{:<16}{:<14}{:<9}{:<20}{:<20}{}".format(
        x["original"], x["raiz"], x["sufijo_actual"], x["sufijo"],
        x["forma"], str(x["glosa"]), x["nota"]))

with open(CSV_OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["ID", "Original", "Raíz", "Sufijo actual", "Sufijo aplicado",
                "Forma Askáro", "Glosa", "Nota"])
    for x in tabla:
        w.writerow([x["id"], x["original"], x["raiz"], x["sufijo_actual"],
                    x["sufijo"], x["forma"], x["glosa"], x["nota"]])
    w.writerow([])
    w.writerow(["# Acentuación del sufijo tónico -dor en la columna derivado_dor"])
    w.writerow(["ID", "actual", "propuesto"])
    for i, a, b in dor_fix:
        w.writerow([i, a, b])
print(f"\nCSV generado: {CSV_OUT}")

# ------------------------------------------------------------------ aplicar
if APPLY:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS sufijos_askaro (
                     id TEXT PRIMARY KEY, original TEXT, raiz TEXT,
                     sufijo_actual TEXT, sufijo_fijado TEXT, forma_askaro TEXT,
                     glosa TEXT, nota TEXT, clase TEXT,
                     fecha TEXT DEFAULT CURRENT_TIMESTAMP)""")
    cols = [c[1] for c in con.execute("pragma table_info('lexico')")]
    if "termino_sufijado" not in cols:
        cur.execute("ALTER TABLE lexico ADD COLUMN termino_sufijado TEXT")
    if "sufijo_nota" not in cols:
        cur.execute("ALTER TABLE lexico ADD COLUMN sufijo_nota TEXT")
    cur.execute("DELETE FROM sufijos_askaro")
    nreg = nexcep = 0
    for x in tabla:
        cur.execute("INSERT OR REPLACE INTO sufijos_askaro (id,original,raiz,sufijo_actual,"
                    "sufijo_fijado,forma_askaro,glosa,nota,clase) VALUES (?,?,?,?,?,?,?,?,?)",
                    (x["id"], x["original"], x["raiz"], x["sufijo_actual"], x["sufijo"],
                     x["forma"], x["glosa"], x["nota"], x["clase"]))
        if x["nota"] == "regular":
            cur.execute("UPDATE lexico SET termino_sufijado=?, sufijo_nota='regular' WHERE id=?",
                        (x["forma"], x["id"])); nreg += 1
        else:
            cur.execute("UPDATE lexico SET termino_sufijado=?, sufijo_nota=? WHERE id=?",
                        (x["original"], x["nota"]); nexcep += 1
    for i, a, b in dor_fix:
        cur.execute("UPDATE lexico SET derivado_dor=? WHERE id=?", (b, i))
    con.commit()
    print(f"\nAPLICADO: {len(tabla)} auditadas | {nreg} regulares con termino_sufijado | "
          f"{nexcep} marcadas importación/excepción | {len(dor_fix)} derivado_dor -> -dór")
else:
    print("\n(dry-run: nada escrito; usa --apply)")

print("integrity_check:", con.execute("pragma integrity_check").fetchone()[0])
con.close()
