import os
from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI(title="proyectoBD API")

def get_engine():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        # fallback local (solo para pruebas en tu PC)
        db_url = "postgresql://postgres:postgres@localhost:5432/proyectoBD"

    # Render a veces da postgres:// ... SQLAlchemy prefiere postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    # Engine (SQLAlchemy 2.x) + reconexión automática
    return create_engine(db_url, pool_pre_ping=True, future=True)

@app.get("/")
def root():
    return {"status": "ok", "message": "API proyectoBD funcionando"}

@app.get("/health")
def health():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": "not connected", "detail": str(e)}

# --- Endpoints mínimos (para la Actividad 2) ---
@app.get("/clientes")
def listar_clientes():
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id_cliente, nombre, direccion, telefono FROM clientes ORDER BY id_cliente")
        ).mappings().all()
    return list(rows)

@app.get("/productos")
def listar_productos():
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT id_producto, nombre, descripcion, precio, stock, id_categoria
            FROM productos ORDER BY id_producto
        """)).mappings().all()
    return list(rows)

@app.get("/ordenes")
def listar_ordenes():
    engine = get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT id_orden, tipo_orden, id_cliente
            FROM ordenes ORDER BY id_orden
        """)).mappings().all()
    return list(rows)

