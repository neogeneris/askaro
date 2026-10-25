#!/usr/bin/env python3
"""Ejecuta schema.sql contra lexico.db con executescript().

Motivo: el SQLite embebido del sistema (3.40.1, usado por la CLI y por el
modulo sqlite3 de Python) rechaza erroneamente la concatenacion || dentro
de RAISE(ABORT, ... ) en los cuerpos BEGIN...END de los triggers (bug de
parsing). Se usa pysqlite3-binary (SQLite 3.51.1 >= 3.37, soporta STRICT)
si esta disponible; si no, se cae al sqlite3 del sistema.
"""
import sys
from pathlib import Path

try:
    import pysqlite3 as sqlite3
    fuente = f"pysqlite3 (SQLite {sqlite3.sqlite_version})"
except ImportError:
    import sqlite3
    fuente = f"sqlite3 estandar (SQLite {sqlite3.sqlite_version})"

BASE = Path(__file__).resolve().parent
SCHEMA = BASE / "schema.sql"
DB = BASE / "lexico.db"

def main() -> int:
    print(f"Ejecutando con: {fuente}")
    sql = SCHEMA.read_text(encoding="utf-8")
    conn = sqlite3.connect(str(DB))
    try:
        conn.executescript(sql)
        conn.commit()
        cur = conn.cursor()
        for t in ("table", "index", "trigger", "view"):
            n = cur.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type=? "
                "AND name NOT LIKE 'sqlite_%'", (t,),
            ).fetchone()[0]
            print(f"{t}s: {n}")
        print("emoji_colisiones:", cur.execute("SELECT COUNT(*) FROM emoji_colisiones").fetchone()[0])
        print("lexico:", cur.execute("SELECT COUNT(*) FROM lexico").fetchone()[0])
        print("integrity_check:", cur.execute("PRAGMA integrity_check").fetchone()[0])
    finally:
        conn.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
