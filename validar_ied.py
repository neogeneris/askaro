#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador IED (Interlingua-English Dictionary, Guralnik).

Fuente: https://github.com/fuszenecker/InterlinguaEnglishDictionary/blob/master/IED/Interlingua-English%20Dictionary.txt

Construye el conjunto de headwords del IED y lo usa como diccionario autoritativo
para validar/corregir la columna `interlingua` de askaro_lexico.db.

Uso:
    python3 validar_ied.py            # dry-run: informa OK / NO / corregibles
    python3 validar_ied.py --apply    # escribe correcciones en la BD
"""
import re
import sys
import sqlite3
import unicodedata
from collections import defaultdict

IED_PATH = "/tmp/IED.txt"
DB_PATH = "askaro_lexico.db"


def strip_acc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                   if unicodedata.category(c) != "Mn").strip()


HEAD_RE = re.compile(r"^(?P<head>[^\s{][^{]*)\{(?P<pos>[a-z]+)\}")


def clean_head(raw):
    """Normaliza un headword del IED a su forma canónica.

    El txt tiene casos raros: 'facer [fac-/fact-;-fic-/-fect-] {v}',
    "ille' {pron}", '[G]' lang tags, variantes '(bú-)'. Se limpian todos.
    """
    h = raw.strip().strip("[]").lower()
    h = re.sub(r"\[[^\]]*\]", "", h)          # quita [tags] completos
    h = re.sub(r"\[[^\]]*$", "", h)           # quita [tag sin cerrar
    h = h.replace("'", "").replace("`", "")   # apóstrofos de variantes (ille')
    h = re.sub(r"[^a-záéíóúàèìòùâêîôûäëïöü' -]", " ", h)
    base = h.split("(")[0].strip()
    base = re.sub(r"\s+", " ", base).strip()
    return base


def build_ied(path=IED_PATH):
    """Devuelve (dict normalizado->canonical, indice por prefijo de 2 letras)."""
    exact = {}
    first2 = defaultdict(set)
    with open(path, encoding="latin-1") as fh:
        for line in fh:
            m = HEAD_RE.match(line)
            if not m:
                continue
            base = clean_head(m.group("head"))
            pos = m.group("pos")
            if len(base) < 2 or base.startswith("-") or base.endswith("-"):
                continue
            if " " in base:
                continue
            if pos in ("prefixo", "suffixo", "prefixo verbal"):
                continue
            for key in {base, strip_acc(base)}:
                if key not in exact:
                    exact[key] = (base, pos)
                first2[key[:2]].add(key)
    return exact, {k: sorted(v) for k, v in first2.items()}


def levenshtein(a, b):
    if abs(len(a) - len(b)) > 2:
        return 99
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def validate_form(word, exact, first2, max_dist=1):
    """Busca `word` en el IED; devuelve ((canonical,pos), dist) o None.

    El candidato difusivo se filtra por prefijo de 2 letras para no
    recorrer los ~25k headwords con Levenshtein en cada consulta.
    """
    w = strip_acc(word)
    if w in exact:
        return exact[w], 0
    if len(w) < 2:
        return None
    best = None
    seen = set()
    for key in first2.get(w[:2], ()):
        if key in seen:
            continue
        seen.add(key)
        d = levenshtein(w, key)
        if d <= max_dist and (best is None or d < best[1]):
            best = (exact[key], d)
    return best


def main(apply_changes=False):
    exact, first2 = build_ied()
    print(f"headwords IED cargados: {len(exact)}")

    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT id, espanol, interlingua FROM lexico "
        "WHERE COALESCE(interlingua,'')<>''").fetchall()

    ok = fixes = unknown = 0
    fix_list = []
    unk_list = []
    for rid, es, ia in rows:
        f = strip_acc(re.sub(r"\[[^\]]*\]", "", ia)).split("(")[0].split(",")[0].strip()
        r = validate_form(f, exact, first2)
        if r and r[1] == 0:
            ok += 1
        elif r and r[1] == 1:
            fixes += 1
            fix_list.append((rid, es, ia, r[0][0]))
        else:
            unknown += 1
            unk_list.append((rid, es, ia))

    print(f"total validadas: {len(rows)}")
    print(f"  OK exactas:            {ok}")
    print(f"  corregibles (dist=1):  {fixes}")
    print(f"  no encontradas:        {unknown}")
    print("\nEjemplos de correccion:")
    for x in fix_list[:15]:
        print(f"  {x[1]}: '{x[2]}' -> '{x[3]}'")
    print("\nEjemplos no encontrados (revisar):")
    for x in unk_list[:20]:
        print(f"  {x[1]}: '{x[2]}'")

    if apply_changes:
        con.execute("BEGIN")
        for rid, es, old, new in fix_list:
            con.execute("UPDATE lexico SET interlingua=? WHERE id=?", (new, rid))
        con.commit()
        print(f"\nAPLICADAS {fixes} correcciones.")
    con.close()


if __name__ == "__main__":
    main("--apply" in sys.argv)
