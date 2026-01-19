import os
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

app = FastAPI(title="proyectoBD API")

_ENGINE: Engine | None = None


def get_engine() -> Engine:
    """
    Crea (una sola vez) y regresa el Engine de SQLAlchemy.
    Usa psycopg v3 con el driver 'postgresql+psycopg://'.
    """
    global _ENGINE
    if _ENGINE is not None:
        return _ENGINE

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # fallback local (solo para pruebas en tu PC)
        db_url = "postgresql://postgres:postgres@localhost:5432/proyectoBD"

    # Render a veces da postgres:// ... SQLAlchemy prefiere postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    # Forzar el driver psycopg (v3) en SQLAlchemy:
    # postgresql://  -> postgresql+psycopg://
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)

    # En Render normalmente se requiere SSL
    connect_args = {}
    if os.getenv("DATABASE_URL"):
        connect_args = {"sslmode": "require"}

    _ENGINE = create_engine(
        db_url,
        pool_pre_ping=True,
        future=True,
        connect_args=connect_args,
    )
    return _ENGINE


@app.get("/")
def root():
    return {"status": "ok", "message": "API proyectoBD funcionando"}


@app.get("/health")
def health():
    """
    Endpoint simple para verificar que:
    1) la API responde
    2) la base de datos está conectada
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": "not connected", "detail": str(e)}


# =========================================================
# Endpoints para Actividad Complementaria 2 (consultas SELECT)
# =========================================================

@app.get("/clientes")
def listar_clientes():
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT id_cliente, nombre, direccion, telefono
                FROM clientes
                ORDER BY id_cliente
            """)
        ).mappings().all()
    return list(rows)


@app.get("/productos")
def listar_productos():
    """
    Endpoint solicitado en la actividad:
    Ejecuta un SELECT para consultar el contenido de la tabla productos.
    """
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT id_producto, nombre, descripcion, precio, stock, id_categoria
                FROM productos
                ORDER BY id_producto
            """)
        ).mappings().all()
    return list(rows)


@app.get("/ordenes")
def listar_ordenes():
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT id_orden, tipo_orden, id_cliente
                FROM ordenes
                ORDER BY id_orden
            """)
        ).mappings().all()
    return list(rows)
