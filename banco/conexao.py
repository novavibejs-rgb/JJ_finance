import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PASTA_INSTANCE = BASE_DIR / "instance"
PASTA_INSTANCE.mkdir(parents=True, exist_ok=True)

DB = PASTA_INSTANCE / "financeiro.db"


def conectar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn