"""Microservicio de REDIRECCIÓN: lectura intensiva y latencia mínima.

Resuelve el código corto (caché en memoria -> PostgreSQL), responde 301/302 de inmediato
y publica el evento de clic en Pub/Sub DESPUÉS de responder (no retrasa la redirección).
"""
import json
import logging
import os
import threading
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from .utils import CODE_RE, TTLCache, hash_ip

log = logging.getLogger("redirect")
logging.basicConfig(level=logging.INFO)

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+psycopg2://acortador:acortador@localhost:5432/acortador"
)
GCP_PROJECT = os.environ.get("GCP_PROJECT", "acortador-local")
PUBSUB_TOPIC = os.environ.get("PUBSUB_TOPIC", "click-events")
AUTO_CREATE = os.environ.get("AUTO_CREATE_RESOURCES", "false").lower() == "true"
CACHE_TTL = float(os.environ.get("CACHE_TTL_SECONDS", "30"))
IP_SALT = os.environ.get("IP_HASH_SALT", "cambia-esta-sal")

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=10, pool_pre_ping=True)
cache = TTLCache(ttl=CACHE_TTL)

_publisher = None
_topic_path = None


def _init_pubsub() -> None:
    """Crea el cliente de Pub/Sub (y el tema si AUTO_CREATE_RESOURCES=true). Corre en segundo plano."""
    global _publisher, _topic_path
    from google.api_core.exceptions import AlreadyExists
    from google.cloud import pubsub_v1

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GCP_PROJECT, PUBSUB_TOPIC)
    if AUTO_CREATE:
        stop = threading.Event()
        for attempt in range(30):
            try:
                publisher.create_topic(name=topic_path)
                break
            except AlreadyExists:
                break
            except Exception as exc:  # noqa: BLE001  (el emulador puede tardar en arrancar)
                log.warning("Pub/Sub no disponible (%s). Reintento %d/30", exc, attempt + 1)
                stop.wait(2)
    _publisher, _topic_path = publisher, topic_path
    log.info("Publicando eventos en %s", topic_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=_init_pubsub, name="pubsub-init", daemon=True).start()
    yield


app = FastAPI(title="Acortador de URLs - Redirección", docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
Instrumentator(excluded_handlers=["/health", "/metrics"]).instrument(app).expose(
    app, include_in_schema=False
)


def _log_publish_result(future) -> None:
    try:
        future.result()
    except Exception:  # noqa: BLE001
        log.exception("No se pudo publicar el evento de clic")


def publish_click(code: str, user_agent: str, referer: str, ip: str) -> None:
    """Se ejecuta después de enviar la respuesta. Un fallo aquí nunca afecta al visitante."""
    if _publisher is None:
        return
    event = {
        "code": code,
        "ts": datetime.now(timezone.utc).isoformat(),
        "user_agent": user_agent[:300],
        "referer": referer[:300],
        "ip_hash": hash_ip(ip, IP_SALT),
    }
    try:
        future = _publisher.publish(_topic_path, json.dumps(event).encode("utf-8"))
        future.add_done_callback(_log_publish_result)
    except Exception:  # noqa: BLE001
        log.exception("Error al publicar evento de clic")


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/app/", status_code=302)


@app.get("/{code}", include_in_schema=False)
def follow(code: str, request: Request, background: BackgroundTasks):
    if not CODE_RE.match(code):
        raise HTTPException(404, "Enlace no encontrado")

    target = cache.get(code)
    if target is None:
        try:
            with engine.connect() as conn:
                row = conn.execute(
                    text("SELECT url, permanent FROM links WHERE code = :c"), {"c": code}
                ).first()
        except SQLAlchemyError:
            log.exception("Error consultando la base de datos")
            raise HTTPException(503, "Servicio temporalmente no disponible")
        if row is None:
            raise HTTPException(404, "Enlace no encontrado")
        target = (row.url, row.permanent)
        cache.set(code, target)

    url, permanent = target
    ip = (request.headers.get("x-forwarded-for") or (request.client.host if request.client else "")).split(",")[0].strip()
    background.add_task(
        publish_click, code, request.headers.get("user-agent", ""), request.headers.get("referer", ""), ip
    )
    if permanent:
        return RedirectResponse(url, status_code=301)
    return RedirectResponse(url, status_code=302, headers={"Cache-Control": "no-store"})
