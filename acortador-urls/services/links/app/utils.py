"""Utilidades puras (sin dependencias externas) del servicio de gestión de enlaces."""
import re
import secrets

BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
ALIAS_RE = re.compile(r"^[A-Za-z0-9_-]{3,32}$")
# Rutas que no pueden usarse como código corto porque ya tienen otro significado.
RESERVED = {"api", "app", "docs", "health", "metrics", "admin", "static"}


def random_code(length: int = 7) -> str:
    """Código aleatorio en Base62 (62^7 ~ 3.5 billones de combinaciones)."""
    return "".join(secrets.choice(BASE62) for _ in range(length))


def is_valid_alias(alias: str) -> bool:
    return bool(ALIAS_RE.match(alias)) and alias.lower() not in RESERVED
