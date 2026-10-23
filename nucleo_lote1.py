#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NÚCLEO — Lote 1 (100 sustantivos, ASK-SUS-0005..0320).
Crea tabla nucleo + columna sustantivo.nucleo_id, asigna núcleo por
regla unicode/familia/pendiente y calcula sintesis_completa del lote.
NO toca modificadores ni grafo. NO reclasifica.
"""
import sqlite3

DB = "/workspace/sintesio.db"

FAM_EMOJI = {  # familia_id -> emoji base de familia
    "ak": "💧", "fo": "🔥", "ter": "🪨", "kor": "🧍", "ka": "🏠",
    "nu": "🍽", "tem": "⏳", "si": "🌌", "vi": "🌱", "mor": "💀",
    "so": "👥", "mu": "🚶", "me": "🧠", "er": "🛠", "sk": "💬",
}

# id askaro -> (simbolo, fuente, confianza, nota)
# fuente 'unicode' => emoji especifico claro; ambiguo => se baja a familia/media con nota
A = {
"ASK-SUS-0005": ("◇","pendiente","baja","'cosa' es el generico universal; no hay familia ni emoji"),
"ASK-SUS-0006": ("🧑","unicode","alta","persona humana generica"),
"ASK-SUS-0007": ("💬","familia","media","nombre (sk); sin emoji especifico claro para 'nombre'"),
"ASK-SUS-0008": ("💚","unicode","media","emoji corazon verde asoc. vida; leve ambiguedad con salud"),
"ASK-SUS-0009": ("💀","unicode","alta","muerte"),
"ASK-SUS-0010": ("💧","unicode","alta","agua; emoji canonico de la familia ak"),
"ASK-SUS-0011": ("🔥","unicode","alta","fuego; emoji canonico de la familia fo"),
"ASK-SUS-0012": ("🪨","unicode","alta","tierra/piedra; canonico ter"),
"ASK-SUS-0013": ("🌬","unicode","alta","aire/viento"),
"ASK-SUS-0033": ("☀️","unicode","alta","sol"),
"ASK-SUS-0034": ("🌙","unicode","alta","luna"),
"ASK-SUS-0035": ("⭐","unicode","alta","estrella"),
"ASK-SUS-0038": ("⛰️","unicode","alta","montana"),
"ASK-SUS-0039": ("🌳","unicode","alta","arbol"),
"ASK-SUS-0042": ("🪨","unicode","media","piedra; AMBIGUO: comparte emoji con 'tierra' (termino)"),
"ASK-SUS-0043": ("🩸","unicode","alta","sangre"),
"ASK-SUS-0044": ("🦴","unicode","alta","hueso"),
"ASK-SUS-0046": ("🧴","unicode","media","piel; sin emoji de piel; 🧴 evoca dermis/cuidado, anotado"),
"ASK-SUS-0047": ("❤️","unicode","alta","corazon"),
"ASK-SUS-0048": ("🗣","unicode","media","cabeza; 🗣 es cabeza-hablando, no craneo; ambiguedad anotada"),
"ASK-SUS-0049": ("✋","unicode","alta","mano"),
"ASK-SUS-0051": ("👁️","unicode","alta","ojo"),
"ASK-SUS-0052": ("👄","unicode","alta","boca"),
"ASK-SUS-0053": ("🏠","unicode","alta","casa"),
"ASK-SUS-0054": ("🚪","unicode","alta","puerta"),
"ASK-SUS-0055": ("🪟","unicode","alta","ventana"),
"ASK-SUS-0057": ("🪑","unicode","alta","silla"),
"ASK-SUS-0058": ("🛏️","unicode","alta","cama"),
"ASK-SUS-0059": ("✉️","unicode","alta","carta misiva"),
"ASK-SUS-0061": ("🍷","unicode","alta","vino"),
"ASK-SUS-0063": ("🥩","unicode","alta","carne de vaca"),
"ASK-SUS-0087": ("👧","unicode","media","hermana; 👧 marca femenino+juvenil; ambiguedad anotada"),
"ASK-SUS-0088": ("👦","unicode","media","hijo; 👦 marca masculino+juvenil; ambiguedad anotada"),
"ASK-SUS-0089": ("👧","unicode","media","hija; AMBIGUO: mismo emoji que 'hermana'; colision registrada"),
"ASK-SUS-0090": ("◇","pendiente","baja","libertad: abstracto sin emoji claro (⛓ rota seria interpretacion)"),
"ASK-SUS-0091": ("◇","pendiente","baja","verdad: abstracto me; ✔ generalizado no es nucleo"),
"ASK-SUS-0092": ("🏙️","unicode","alta","ciudad"),
"ASK-SUS-0093": ("🏳️","unicode","media","nacion; bandera como metonimia; ambiguedad anotada"),
"ASK-SUS-0094": ("🦠","unicode","media","infeccion; 🦠 es germen (causa), no infeccion; anotado"),
"ASK-SUS-0095": ("📢","unicode","media","publicidad; altavoz metaforico; ambiguedad anotada"),
"ASK-SUS-0097": ("🗳️","unicode","alta","democracia (voto)"),
"ASK-SUS-0098": ("🧔","unicode","media","filosofo; persona-barba es estereotipo; ambiguedad anotada"),
"ASK-SUS-0099": ("📜","unicode","alta","historia (pergamino)"),
"ASK-SUS-0102": ("🏛️","unicode","alta","gobierno (edificio institucional)"),
"ASK-SUS-0104": ("⚔️","unicode","alta","guerra"),
"ASK-SUS-0105": ("🕊️","unicode","alta","paz"),
"ASK-SUS-0106": ("⛪","unicode","alta","iglesia"),
"ASK-SUS-0107": ("😇","unicode","media","dios; halo angelical ambiguo (angel vs dios); bajado a media"),
"ASK-SUS-0109": ("🌍","unicode","alta","mundo/tierra planetaria"),
"ASK-SUS-0110": ("⏳","unicode","alta","tiempo; canonico tem"),
"ASK-SUS-0111": ("🌌","unicode","alta","espacio cosmico"),
"ASK-SUS-0112": ("🎉","unicode","media","partido politico; 🎉 es fiesta, metonimia debil; anotado"),
"ASK-SUS-0114": ("🤱","unicode","media","seno; emoji allanando ambigua entre maternidad y pecho; anotado"),
"ASK-SUS-0116": ("⛵","unicode","alta","barca"),
"ASK-SUS-0117": ("🚢","unicode","alta","navio"),
"ASK-SUS-0118": ("🐎","unicode","alta","caballo"),
"ASK-SUS-0119": ("🐕","unicode","media","perro; AMBIGUO: 🐕 puede leerse perro/lobo joven; regla critica"),
"ASK-SUS-0120": ("🐈","unicode","media","gato; 🐈 incluye gato domestico; ok pero familia vi cercana"),
"ASK-SUS-0121": ("🐈‍⬛","unicode","media","gata; gata negra ≠ hembra; ambiguedad sexo/color anotada"),
"ASK-SUS-0122": ("🐄","unicode","alta","vaca"),
"ASK-SUS-0124": ("🐓","unicode","alta","gallo"),
"ASK-SUS-0125": ("🐔","unicode","alta","gallina"),
"ASK-SUS-0126": ("🐺","unicode","alta","lobo; distingue de perro 🐕"),
"ASK-SUS-0127": ("🐀","unicode","alta","raton"),
"ASK-SUS-0130": ("🏖️","unicode","alta","playa"),
"ASK-SUS-0132": ("🌲","unicode","media","selva; 🌲 es conifero/bosque; selva tropical sin emoji exacto"),
"ASK-SUS-0133": ("🌾","unicode","media","campo; 🌾 evoca cultivo; campo generico ambiguo"),
"ASK-SUS-0134": ("🛤️","unicode","alta","camino"),
"ASK-SUS-0135": ("🌉","unicode","alta","puente"),
"ASK-SUS-0136": ("⛰️","unicode","media","colina; AMBIGUO: mismo emoji que montana; colision registrada"),
"ASK-SUS-0194": ("🧪","unicode","media","acido; probeta quimica general; ambiguedad anotada"),
"ASK-SUS-0196": ("🧂","unicode","alta","sal"),
"ASK-SUS-0197": ("🪙","unicode","media","azufre; sin emoji de azufre; 🪙 por color amarillo? FORZADO->vease pendiente"),
"ASK-SUS-0198": ("⛓️","unicode","media","hierro; cadena evoca metalurgia; ambiguedad fuerte anotada"),
"ASK-SUS-0199": ("🥇","unicode","media","oro; medalla es artefacto aurificado; ambiguedad anotada"),
"ASK-SUS-0201": ("🫙","unicode","media","vidrio; tarro de vidrio; objeto vs material anotado"),
"ASK-SUS-0202": ("⚙️","unicode","media","maquina; engranaje parte-por-todo; aceptado con nota"),
"ASK-SUS-0203": ("💻","unicode","alta","computadora"),
"ASK-SUS-0204": ("💾","unicode","media","programa; disquete obsoleto/metaforico; anotado"),
"ASK-SUS-0206": ("⚛️","unicode","media","electron; ⚛ es atom; electron no tiene emoji propio; anotado"),
"ASK-SUS-0210": ("🌍","unicode","media","gravedad; AMBIGUO: mismo emoji que mundo; ambiguedad anotada"),
"ASK-SUS-0213": ("💊","unicode","media","medicina; pastilla es subtipo; ambiguedad practica-vs-farmaco"),
"ASK-SUS-0215": ("🏥","unicode","alta","hospital"),
"ASK-SUS-0216": ("🦠","unicode","alta","microbio"),
"ASK-SUS-0217": ("🧫","unicode","media","celula; placa de Petri; biologia general anotada"),
"ASK-SUS-0222": ("◇","pendiente","baja","suma (matematica): sin emoji claro; ➕ es operador, no sustantivo"),
"ASK-SUS-0224": ("⚖️","unicode","alta","abogado (justicia)"),
"ASK-SUS-0226": ("◇","pendiente","baja","impuesto: 💰 evoca dinero generico, no tributo; forzado"),
"ASK-SUS-0227": ("🛒","unicode","media","mercado; carrito es supermercado moderno; anotado"),
"ASK-SUS-0228": ("💰","unicode","alta","dinero"),
"ASK-SUS-0229": ("🏦","unicode","alta","banco"),
"ASK-SUS-0312": ("💪","unicode","media","brazo; flexion muestra brazo pero es fuerza; ambiguedad anotada"),
"ASK-SUS-0313": ("🦵","unicode","alta","pierna"),
"ASK-SUS-0314": ("🦵","unicode","media","rodilla; AMBIGUO: mismo emoji que pierna; colision registrada"),
"ASK-SUS-0315": ("👆","unicode","media","dedo; dedo senalante concreto vs dedo generico; anotado"),
"ASK-SUS-0316": ("💅","unicode","media","una (uña); esmalte desvia a manicura; ambiguedad anotada"),
"ASK-SUS-0317": ("👄","unicode","media","labio; AMBIGUO: mismo emoji que boca; colision registrada"),
"ASK-SUS-0318": ("👂","unicode","alta","oreja"),
"ASK-SUS-0319": ("👃","unicode","alta","nariz"),
"ASK-SUS-0320": ("🧣","unicode","media","cuello; bufanda cubre cuello, no es cuello; ambiguedad anotada"),
}

# Correccion honesta: azufre no tiene emoji razonable -> pendiente, no forzar 🪙
A["ASK-SUS-0197"] = ("◇","pendiente","baja","azufre: sin emoji de azufre en Unicode; 🪙 era forzado -> pendiente")

# Regla critica del prompt: si el emoji especifico es AMBIGUO y existe emoji de familia
# claro, usar la familia (fuente='familia', confianza='media') con nota de ambiguedad.
# Solo aplica donde el generico familiar NO colisiona con otro nucleo ya asignado.
A["ASK-SUS-0046"] = ("🧍","familia","media","piel: sin emoji de piel; familia kor 🧍; 🧴 era metafora forzada")
A["ASK-SUS-0320"] = ("🧍","familia","media","cuello: sin emoji de cuello; familia kor 🧍; 🧣 era objeto que lo cubre")

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys=ON")

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS nucleo (
        id              TEXT PRIMARY KEY,
        simbolo         TEXT NOT NULL,
        familia_id      TEXT NOT NULL,
        termino_askaro  TEXT NOT NULL,
        fuente          TEXT CHECK(fuente IN ('unicode','familia','pendiente')),
        confianza       TEXT CHECK(confianza IN ('alta','media','baja')),
        notas           TEXT
    );
    """)
    col = [r[1] for r in cur.execute("PRAGMA table_info(sustantivo)")]
    if "nucleo_id" not in col:
        cur.execute("ALTER TABLE sustantivo ADD COLUMN nucleo_id TEXT REFERENCES nucleo(id)")

    rows = list(cur.execute(
        "SELECT s.id, s.termino, c.familia FROM sustantivo s "
        "LEFT JOIN concepto c ON c.termino_askaro=s.termino WHERE c.clase_gramatical='Sustantivo' "
        "ORDER BY s.id LIMIT 100"))
    print(f"lote1 filas={len(rows)}")

    ins = upd = 0
    for sid, term, fam in rows:
        if sid not in A:
            print(f"AVISO: {sid} ({term}) sin entrada manual -> pendiente por defecto")
            sym, fte, conf, nota = ("◇", "pendiente", "baja", "sin revision lote1")
        else:
            sym, fte, conf, nota = A[sid]
        fam_base = FAM_EMOJI.get(fam or "", "◇")
        nid = "nucleo_" + term.replace(" ", "_")
        cur.execute("INSERT OR REPLACE INTO nucleo VALUES (?,?,?,?,?,?,?)",
                    (nid, sym, fam or "??", term, fte, conf, nota))
        cur.execute("UPDATE sustantivo SET nucleo_id=? WHERE id=?", (nid, sid))
        ins += 1; upd += 1

    con.commit()

    # sintesis_completa del lote: nucleo + simbolos de grafo (orden estable por modificador.id)
    q = """
    SELECT s.id, n.simbolo || COALESCE((
      SELECT GROUP_CONCAT(m.simbolo,'') FROM (
        SELECT DISTINCT m.simbolo FROM grafo_arista g JOIN modificador m ON m.id=g.modificador_id
        WHERE g.sustantivo_id=s.id ORDER BY m.id) m), '') AS sc
    FROM sustantivo s JOIN nucleo n ON n.id=s.nucleo_id
    WHERE s.nucleo_id IS NOT NULL
    """
    res = list(cur.execute(q))
    print(f"sintesis_calculadas={len(res)}")
    for sid, sc in res[:12]:
        print(" ", sid, sc)

    dist = list(cur.execute("SELECT fuente,confianza,COUNT(*) FROM nucleo GROUP BY 1,2 ORDER BY 1,2"))
    print("dist lote1:", dist)
    con.close()

if __name__ == "__main__":
    main()
