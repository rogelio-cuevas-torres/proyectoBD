# db.py
import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor


def _get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL no está definida. Configúrala en tu entorno o en Render."
        )
    return url


@contextmanager
def get_conn():
    """
    Abre una conexión a PostgreSQL usando DATABASE_URL.
    Usa RealDictCursor para que cada fila salga como dict (ideal para JSON).
    """
    conn = psycopg2.connect(_get_database_url(), sslmode="require")
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(query: str, params=None):
    """
    Ejecuta un SELECT y regresa una lista de diccionarios.
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            return rows
