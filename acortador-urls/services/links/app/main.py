"""Microservicio de GESTIÓN DE ENLACES: API REST (CRUD) documentada con OpenAPI/Swagger.

Además sirve el panel web (carpeta static/) en /app/.
"""
import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

from .utils import is_valid_alias, random_code

log = logging.getLogger("links")
logging.basicConfig(level=logging.INFO)

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg2://acortador:acortador@localhost:5432/acortador"
)
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080").rstrip("/")
MAX_URL_LENGTH = 2048

engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=5, pool_pre_ping=True)

DDL = """
CREATE TABLE IF NOT EXISTS links (
    code        VARCHAR(32)  PRIMARY KEY,
    url         TEXT         NOT NULL,
    permanent   BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
)
"""
COLUMNS = "code, url, permanent, created_at, updated_at"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # La base puede tardar unos segundos en estar lista: reintentamos.
    for attempt in range(30):
        try:
            with engine.begin() as conn:
                conn.execute(text(DDL))
            log.info("Tabla 'links' lista")
            break
        except Exception as exc:  # noqa: BLE001
            log.warning("Base de datos no disponible (%s). Reintento %d/30", exc, attempt + 1)
            time.sleep(2)
    yield


app = FastAPI(
    title="Acortador de URLs - Gestión de enlaces",
    description="API REST para crear, consultar, actualizar y eliminar enlaces cortos.",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url=None,
    lifespan=lifespan,
)
Instrumentator(excluded_handlers=["/health", "/metrics"]).instrument(app).expose(
    app, include_in_schema=False
)


class LinkCreate(BaseModel):
    url: HttpUrl = Field(description="URL original (http o https)")
    alias: str | None = Field(
        default=None,
        description="Código personalizado (3-32 caracteres: letras, números, _ o -). Si se omite se genera uno aleatorio.",
    )
    permanent: bool = Field(
        default=False,
        description="True usa HTTP 301 (el navegador lo cachea y los clics repetidos no se cuentan). False usa 302.",
    )


class LinkUpdate(BaseModel):
    url: HttpUrl | None = None
    permanent: bool | None = None


class LinkOut(BaseModel):
    code: str
    short_url: str
    url: str
    permanent: bool
    created_at: datetime
    updated_at: datetime


def _out(row) -> LinkOut:
    m = row._mapping
    return LinkOut(
        code=m["code"],
        short_url=f"{BASE_URL}/{m['code']}",
        url=m["url"],
        permanent=m["permanent"],
        created_at=m["created_at"],
        updated_at=m["updated_at"],
    )


def _check_url(url: str) -> str:
    if len(url) > MAX_URL_LENGTH:
        raise HTTPException(422, f"La URL excede {MAX_URL_LENGTH} caracteres")
    if url.startswith(BASE_URL):
        raise HTTPException(422, "No se puede acortar un enlace de este mismo servicio")
    return url


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


@app.post("/api/links", response_model=LinkOut, status_code=201, tags=["enlaces"], summary="Crear enlace")
def create_link(body: LinkCreate):
    url = _check_url(str(body.url))
    if body.alias is not None:
        if not is_valid_alias(body.alias):
            raise HTTPException(422, "Alias inválido: use 3-32 caracteres (letras, números, _ o -) y no una palabra reservada")
        candidates = [body.alias]
    else:
        candidates = [random_code() for _ in range(5)]

    for code in candidates:
        try:
            with engine.begin() as conn:
                row = conn.execute(
                    text(f"INSERT INTO links (code, url, permanent) VALUES (:c, :u, :p) RETURNING {COLUMNS}"),
                    {"c": code, "u": url, "p": body.permanent},
                ).one()
            return _out(row)
        except IntegrityError:
            if body.alias is not None:
                raise HTTPException(409, "El alias ya está en uso")
    raise HTTPException(500, "No se pudo generar un código único; intente de nuevo")


@app.get("/api/links", response_model=list[LinkOut], tags=["enlaces"], summary="Listar enlaces")
def list_links(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
    with engine.connect() as conn:
        rows = conn.execute(
            text(f"SELECT {COLUMNS} FROM links ORDER BY created_at DESC LIMIT :l OFFSET :o"),
            {"l": limit, "o": offset},
        ).all()
    return [_out(r) for r in rows]


@app.get("/api/links/{code}", response_model=LinkOut, tags=["enlaces"], summary="Consultar enlace")
def get_link(code: str):
    with engine.connect() as conn:
        row = conn.execute(text(f"SELECT {COLUMNS} FROM links WHERE code = :c"), {"c": code}).first()
    if row is None:
        raise HTTPException(404, "Enlace no encontrado")
    return _out(row)


@app.patch("/api/links/{code}", response_model=LinkOut, tags=["enlaces"], summary="Actualizar enlace")
def update_link(code: str, body: LinkUpdate):
    fields = {}
    if body.url is not None:
        fields["url"] = _check_url(str(body.url))
    if body.permanent is not None:
        fields["permanent"] = body.permanent
    if not fields:
        raise HTTPException(422, "Indique al menos un campo a actualizar (url o permanent)")
    sets = ", ".join(f"{k} = :{k}" for k in fields)  # las claves son fijas, no vienen del usuario
    with engine.begin() as conn:
        row = conn.execute(
            text(f"UPDATE links SET {sets}, updated_at = now() WHERE code = :code RETURNING {COLUMNS}"),
            {**fields, "code": code},
        ).first()
    if row is None:
        raise HTTPException(404, "Enlace no encontrado")
    return _out(row)


@app.delete("/api/links/{code}", status_code=204, tags=["enlaces"], summary="Eliminar enlace")
def delete_link(code: str):
    with engine.begin() as conn:
        result = conn.execute(text("DELETE FROM links WHERE code = :c"), {"c": code})
    if result.rowcount == 0:
        raise HTTPException(404, "Enlace no encontrado")


# Panel web (debe montarse al final para no tapar las rutas de la API)
app.mount("/app", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="panel")
