"""Utilidades puras (sin dependencias externas) del servicio de redirección."""
import hashlib
import re
import threading
import time

CODE_RE = re.compile(r"^[A-Za-z0-9_-]{3,32}$")


class TTLCache:
    """Caché en memoria con tiempo de vida. Evita consultar la base en cada redirección."""

    def __init__(self, ttl: float = 30.0, max_items: int = 10_000, clock=time.monotonic):
        self.ttl = ttl
        self.max_items = max_items
        self._clock = clock
        self._data: dict = {}
        self._lock = threading.Lock()

    def get(self, key):
        with self._lock:
            item = self._data.get(key)
            if item is None:
                return None
            value, expires = item
            if expires <= self._clock():
                del self._data[key]
                return None
            return value

    def set(self, key, value) -> None:
        with self._lock:
            if len(self._data) >= self.max_items and key not in self._data:
                self._data.clear()  # estrategia simple: vaciar cuando se llena
            self._data[key] = (value, self._clock() + self.ttl)


def hash_ip(ip: str, salt: str) -> str:
    """No guardamos la IP real, solo un hash corto (privacidad)."""
    return hashlib.sha256(f"{salt}{ip}".encode()).hexdigest()[:16]
