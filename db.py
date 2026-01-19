# db.py
import os
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row


def _get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL no está definida. Configúrala en Render.")
    return url


@contextmanager
def get_conn():
    """
    Abre una conexión a PostgreSQL usando DATABASE_URL.
    row_factory=dict_row hace que cada fila sea un dict (ideal para JSON).
    """
    conn = psycopg.connect(_get_database_url(), row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(query: str, params=None):
    """
    Ejecuta un SELECT y regresa una lista de diccionarios.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
