"""Microservicio de ANALÍTICA: escritura intensiva y procesamiento diferido.

Un hilo en segundo plano consume los eventos de clic de Pub/Sub y los guarda en Firestore.
La API expone las estadísticas agregadas que consume el panel web.
"""
import json
import logging
import os
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .utils import parse_device, parse_ts, summarize

log = logging.getLogger("analytics")
logging.basicConfig(level=logging.INFO)

GCP_PROJECT = os.environ.get("GCP_PROJECT", "acortador-local")
PUBSUB_TOPIC = os.environ.get("PUBSUB_TOPIC", "click-events")
PUBSUB_SUBSCRIPTION = os.environ.get("PUBSUB_SUBSCRIPTION", "click-events-analytics")
AUTO_CREATE = os.environ.get("AUTO_CREATE_RESOURCES", "false").lower() == "true"
MAX_SCAN = int(os.environ.get("MAX_CLICKS_SCAN", "20000"))

_stop = threading.Event()
_worker: threading.Thread | None = None
_db = None
_db_lock = threading.Lock()


def get_db():
    global _db
    with _db_lock:
        if _db is None:
            from google.cloud import firestore

            _db = firestore.Client(project=GCP_PROJECT)
        return _db


def handle_message(message) -> None:
    """Guarda un clic en Firestore. ack = procesado; nack = Pub/Sub lo reintenta."""
    try:
        data = json.loads(message.data.decode("utf-8"))
        ua = data.get("user_agent", "")
        doc = {
            "code": data["code"],
            "ts": parse_ts(data["ts"]),
            "device": parse_device(ua),
            "user_agent": ua,
            "referer": data.get("referer", ""),
            "ip_hash": data.get("ip_hash", ""),
        }
    except (ValueError, KeyError, UnicodeDecodeError):
        log.warning("Mensaje malformado descartado: %r", message.data[:200])
        message.ack()
        return
    try:
        get_db().collection("clicks").add(doc)
        message.ack()
    except Exception:  # noqa: BLE001
        log.exception("Error escribiendo en Firestore; se reintentará")
        message.nack()


def run_subscriber() -> None:
    from google.api_core.exceptions import AlreadyExists
    from google.cloud import pubsub_v1

    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(GCP_PROJECT, PUBSUB_TOPIC)
    sub_path = subscriber.subscription_path(GCP_PROJECT, PUBSUB_SUBSCRIPTION)

    if AUTO_CREATE:
        for attempt in range(30):
            if _stop.is_set():
                return
            try:
                try:
                    publisher.create_topic(name=topic_path)
                except AlreadyExists:
                    pass
                try:
                    subscriber.create_subscription(name=sub_path, topic=topic_path, ack_deadline_seconds=30)
                except AlreadyExists:
                    pass
                break
            except Exception as exc:  # noqa: BLE001  (el emulador puede tardar en arrancar)
                log.warning("Pub/Sub no disponible (%s). Reintento %d/30", exc, attempt + 1)
                _stop.wait(2)

    flow = pubsub_v1.types.FlowControl(max_messages=200)
    while not _stop.is_set():
        future = subscriber.subscribe(sub_path, callback=handle_message, flow_control=flow)
        log.info("Escuchando eventos en %s", sub_path)
        while not _stop.wait(1.0) and not future.done():
            pass
        if not future.done():
            future.cancel()
        try:
            future.result(timeout=10)
        except Exception as exc:  # noqa: BLE001  (cancelación o fallo del stream)
            if not _stop.is_set():
                log.error("Suscripción interrumpida (%s); reintentando", exc)
                _stop.wait(3)
    subscriber.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _worker
    _worker = threading.Thread(target=run_subscriber, name="subscriber", daemon=True)
    _worker.start()
    yield
    _stop.set()


app = FastAPI(
    title="Acortador de URLs - Analítica",
    description="Estadísticas de uso por enlace.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan,
)
Instrumentator(excluded_handlers=["/health", "/metrics"]).instrument(app).expose(
    app, include_in_schema=False
)


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok", "subscriber_alive": bool(_worker and _worker.is_alive())}


@app.get("/api/stats/{code}", tags=["estadísticas"])
def stats(code: str):
    """Total de clics, clics por día, por dispositivo y los más recientes de un enlace."""
    try:
        from google.cloud.firestore_v1.base_query import FieldFilter

        query = get_db().collection("clicks").where(filter=FieldFilter("code", "==", code))
    except ImportError:  # versiones antiguas de la librería
        query = get_db().collection("clicks").where("code", "==", code)
    docs = [d.to_dict() for d in query.limit(MAX_SCAN + 1).stream()]
    truncated = len(docs) > MAX_SCAN
    return summarize(code, docs[:MAX_SCAN], truncated)
