#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buscador inverso en el Interlingua-English Dictionary (IED, Guralnik).

Fuente: https://github.com/fuszenecker/InterlinguaEnglishDictionary  (IED/Interlingua-English Dictionary.txt)
El IED es IA->EN; este modulo construye el indice invertido EN->IA.

API:
    idx = build_index("/tmp/IED.txt")          # {english_term_lower: [(ia_form, pos), ...]}
    lookup_ia(idx, "anchor", prefer_nouns=True) -> ("ancora", "n") | None
"""
import re
from collections import defaultdict

HEAD_RE = re.compile(
    r"^(?P<head>\[?[A-Za-z][A-Za-z\-'’ ]*\]?)\s*"
    r"(?:\((?P<xform>[^)]+)\))?\s*"
    r"(?:\[(?P<lang>[A-Z])\])?\s*"
    r"\{(?P<pos>[a-z]+)\}\s*(?P<body>.*)$"
)
SENSE_RE = re.compile(r"\d+\.\s*(?P<defn>.*)$")
GLOSS_SPLIT = re.compile(r"[,;]\s+|\s+-\s+")


def _clean_head(head):
    return head.strip().strip("[]").lower()


def parse_line(line):
    """Return (ia_form, pos, english_words[]) or None."""
    m = HEAD_RE.match(line.rstrip("\n"))
    if not m:
        return None
    head = _clean_head(m.group("head"))
    if not head or len(head) < 2:
        return None
    # skip prefixes/suffixes/cross-refs/combinings
    if head.endswith("-") or head.startswith("-"):
        return None
    pos = m.group("pos")
    if pos in ("prefixo", "suffixo", "prefixo verbal"):
        return None
    body = m.group("body")
    if body.strip().startswith("{see}"):
        return None
    xform = m.group("xform")
    form = xform.split(",")[0].strip() if xform else head
    # collect english glosses from senses + free text
    eng = []
    for sm in SENSE_RE.finditer(body):
        eng.append(sm.group("defn"))
    if not eng:
        # unnumbered definition (e.g. 'abandonamento {n} abandonment')
        eng.append(body)
    words = set()
    for chunk in eng:
        chunk = re.sub(r"`[^']*'", " ", chunk)      # drop IA example phrases
        chunk = re.sub(r"\([^)]*\)", " ", chunk)     # drop parenthetical clarifiers
        chunk = re.sub(r"\[[^\]]*\]", " ", chunk)    # drop domain tags [Naut.]
        chunk = re.sub(r"\{[^)]*\}", " ", chunk)
        for w in GLOSS_SPLIT.split(chunk):
            w = w.strip().strip(".:").lower()
            w = re.sub(r"[’']", "", w)
            if (re.fullmatch(r"[a-z][a-z\- ]*", w) and len(w) >= 3
                    and w not in STOP):
                words.add(w)
    return form, pos, sorted(words)


STOP = {
    "the", "and", "for", "with", "that", "this", "from", "into", "upon",
    "used", "expressing", "referring", "meaning", "indicates", "indicating",
    "also", "compare", "opposite", "kind", "sort", "type", "one", "two",
    "something", "someone", "anything", "some", "such", "other", "others",
    "being", "having", "making", "doing", "about", "related", "pertaining",
    "belonging", "called", "named", "known", "where", "when", "which",
    "those", "these", "very", "more", "most", "like", "as", "than",
    "etc", "often", "usually", "esp", "colloq", "archaic", "obsolete",
    "word", "words", "term", "terms", "sense", "senses", "definition",
    "note", "usage", "examples", "example", "phrase", "phrases",
    "act", "state", "condition", "process", "result", "instance",
    "person", "thing", "place", "things", "persons", "places",
    "to", "of", "in", "on", "at", "by", "or", "not", "but", "all",
    "can", "will", "would", "could", "should", "may", "must", "shall",
}


def build_index(path="/tmp/IED.txt"):
    idx = defaultdict(list)
    n_entries = 0
    with open(path, encoding="latin-1") as fh:
        for line in fh:
            parsed = parse_line(line)
            if not parsed:
                continue
            form, pos, words = parsed
            n_entries += 1
            for w in words:
                idx[w].append((form, pos))
    return idx, n_entries


def lookup_ia(idx, english, prefer_nouns=True):
    """Best-effort IA translation for a single English concept word."""
    key = english.strip().lower()
    cands = idx.get(key)
    if not cands:
        return None
    uniq = {}
    for form, pos in cands:
        uniq.setdefault(form, pos)
    nouns = [(f, p) for f, p in uniq.items() if p == "n"]
    if prefer_nouns and nouns:
        pool = nouns
    else:
        pool = list(uniq.items())
    # prefer shortest, most canonical form
    pool.sort(key=lambda fp: (len(fp[0]), fp[0]))
    return pool[0]


if __name__ == "__main__":
    idx, n = build_index()
    print(f"entradas IA parseadas: {n}, claves EN: {len(idx)}")
    for t in ["anchor", "olive", "avocado", "storehouse", "dawn", "tree"]:
        print(t, "->", lookup_ia(idx, t))
