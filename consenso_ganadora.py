#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RE-CÁLCULO DE `forma_ganadora` / `fuente_ganadora` / `lenguas_consenso`.

Problema que resuelve: el algoritmo de fase 1 (paso4_completo.py, PASO 4)
usaba un sesgo fijo "siempre gana español":
    if es no vacío -> ganadora = es, fuente = 'es'
y solo usaba otra lengua si `es` estaba vacío. Eso contradice la noción de
"ganadora" como forma consensuada: p.ej. en ANCLA, it/pt/ro/ia coinciden en
*ancora* y el propio étimo latino ANCORA lo respalda, pero la tabla guardaba
'ancla' porque era la forma española.

Nuevo criterio (voto ponderado entre las 6 lenguas romances):
  1. Agrupa fr/it/pt/ro/ia/eo por raíz normalizada (sin acentos, sin vocal
     final) — dos formas "cuentan como el mismo voto" si comparten raíz.
  2. El bloque mayoritario gana si tiene >= MIN_VOTOS (3) lenguas.
  3. Empates o desempate dentro del bloque: se elige la forma más cercana al
     étimo latino (columna `latin`), con prioridad ia > eo > it > pt > ro > fr
     (interlingua/esperanto son reflejos casi directos del latín).
  4. Si ningún bloque alcanza 3 votos, gana español (empate a favor de es,
     documentado como tal en la nota).
  5. Se recalcula `lenguas_consenso` = nº de lenguas del bloque ganador.
  6. Nunca se toca la columna `es` ni el resto del esquema; UPDATE dirigido.

Idempotente: vuelve a derivar todo desde las columnas de lenguas.
"""

import collections
import re
import sys
import unicodedata

LEX_DB = sys.argv[1] if len(sys.argv) > 1 else "lexico.db"

try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3

MIN_VOTOS = 3
LANGS = ["fr", "it", "pt", "ro", "ia", "eo"]
# orden de preferencia para desempatar dentro del bloque ganador
PREF = {"ia": 0, "eo": 1, "it": 2, "pt": 3, "ro": 4, "fr": 5}


def strip_acc(s):
    s = unicodedata.normalize("NFD", (s or "").strip().lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def raiz_voto(w):
    """Clave de agrupación de votos: minúsculas, sin acentos, sin vocal
    temática final y sin marcas diacríticas del rumano/eo."""
    k = strip_acc(w)
    k = re.sub(r"[ăâîșțşţ]", lambda m: {"ă": "a", "â": "a", "î": "i",
                                        "ș": "s", "ț": "t", "ş": "s",
                                        "ţ": "t"}[m.group(0)], k)
    k = k.replace("ĉ", "c").replace("ĝ", "g").replace("ŭ", "u")
    # sufijo esperanto -o/-oj tras quitar la vocal final (kamaro~camara)
    if k.endswith("oj"):
        k = k[:-2]
    elif k.endswith("o"):
        k = k[:-1]
    k = k.rstrip("aeiouáéíóúàèìòùâêîôûäëïöü")
    return k


# Excepciones documentadas de agrupación: formas con raíz superficialmente
# divergente que el consenso lingüístico reconoce como equivalente.
ALIAS_VOTO = {
    "ĉielo": "cielo",   # eo < it. cielo
    "reĝino": "regina",  # eo < lat. REGINA
    "persono": "persona",
    "metropolo": "metropole",
    "balanco": "balancia",  # fr balance / ia balancia / pt balança / eo balanco
    "glacio": "glacie",     # hielo: eo glacio ~ ia glacie ~ fr glace
    "gruo": "grue",         # grúa: eo gruo ~ fr grue ~ it gru ~ pt grua
    "fantomo": "fantome",   # fantasma: eo fantomo ~ fr fantôme ~ ro fantomă
    "olivao": "oliva",      # aceituna: eo olivao ~ ia/it oliva ~ fr olive
}


def canon_voto(v):
    k = raiz_voto(v)
    for src, dst in ALIAS_VOTO.items():
        if raiz_voto(src) == k:
            return raiz_voto(dst)
    return k


def similar_a_latin(forma, latin):
    """Cercanía de la forma al étimo latino (V->U, recorte de sufijos)."""
    if not latin or latin == "—":
        return 0
    L = strip_acc(latin).replace("v", "u")
    F = strip_acc(forma).replace("v", "b" if "b" in forma else "v")
    best = 0
    for n in range(len(F), 2, -1):
        if F[:n] in L or L.startswith(F[:n]):
            best = max(best, n)
    return best


def pick_ganadora(row):
    """Devuelve (forma, fuente, n_consenso, detalle_bloque) aplicando el
    nuevo criterio de consenso ponderado."""
    (concepto, es, latin) = row[0], row[1], row[2]
    vals = dict(zip(LANGS, row[3:9]))
    groups = collections.defaultdict(list)
    for lang, v in vals.items():
        if v and v != "—":
            groups[canon_voto(v)].append((lang, v))
    if not groups:
        return es or concepto, "es", 0, "sin datos romances"
    # bloque mayoritario (empate: el que tenga forma más cercana al latín)
    mx = max(len(g) for g in groups.values())
    blocks = [g for g in groups.values() if len(g) == mx]
    if mx < MIN_VOTOS:
        return es or concepto, "es", mx, \
            f"consenso bajo ({mx}<{MIN_VOTOS}); gana es por defecto"
    # elegir la forma representativa del bloque: máxima cercanía al latín,
    # desempate por PREF de lengua
    def key(lv):
        lang, v = lv
        return (-similar_a_latin(v, latin), PREF.get(lang, 9))
    all_forms = []
    for b in blocks:
        all_forms.extend(b)
    lang_w, form_w = sorted(all_forms, key=key)[0]
    n = len(groups[canon_voto(form_w)])
    detalle = ",".join(sorted(l for l, _ in groups[canon_voto(form_w)]))
    # si el bloque ganador coincide con español (raíz igual), fuente sigue es
    if es and es != "—" and canon_voto(es) == canon_voto(form_w):
        return es, "es", n + (0 if "es" in detalle else 1), \
            f"es coincide con el bloque {form_w} ({detalle})"
    return form_w, lang_w, n, f"bloque {form_w} votado por {n} lenguas ({detalle})"


def main():
    con = sqlite3.connect(LEX_DB)
    rows = con.execute(
        "SELECT concepto_es, es, latin, fr, it, pt, ro, ia, eo, "
        "       forma_ganadora, fuente_ganadora, lenguas_consenso "
        "FROM lexico ORDER BY concepto_es").fetchall()

    updates, report = [], []
    for r in rows:
        (concepto, es, latin, fr, it, pt, ro, ia, eo, fg_old, fs_old, lc_old) = r
        forma, fuente, n, detalle = pick_ganadora((concepto, es, latin,
                                                   fr, it, pt, ro, ia, eo))
        if (forma, fuente, n) != (fg_old, fs_old, lc_old):
            updates.append((forma, fuente, n, concepto))
            report.append((concepto, fg_old, fs_old, lc_old,
                           forma, fuente, n, detalle))
    print(f"[consenso] filas={len(rows)} cambios={len(updates)}")
    for c, fo, fs, lo, fn, fus, ln, det in report:
        print(f"  - {c}: '{fo}'({fs},{lo}) -> '{fn}'({fus},{ln})  [{det}]")

    if "--apply" in sys.argv:
        con.executemany(
            "UPDATE lexico SET forma_ganadora=?, fuente_ganadora=?, "
            "lenguas_consenso=? WHERE concepto_es=?", updates)
        con.commit()
        ok = con.execute("PRAGMA integrity_check").fetchone()[0]
        print(f"[consenso] APLICADO ({len(updates)} updates); integrity={ok}")
    else:
        print("[consenso] modo dry-run (usa --apply para escribir)")

    # CSV de auditoría
    with open("recalculo_ganadora.csv", "w", encoding="utf-8", newline="") as fh:
        import csv
        w = csv.writer(fh)
        w.writerow(["concepto_es", "ganadora_antes", "fuente_antes",
                    "consenso_antes", "ganadora_nueva", "fuente_nueva",
                    "consenso_nuevo", "motivo"])
        w.writerows(report)
    print("[consenso] escrito recalculo_ganadora.csv")


if __name__ == "__main__":
    main()
