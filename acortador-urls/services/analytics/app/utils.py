"""Utilidades puras (sin dependencias externas) del servicio de analítica."""
from collections import Counter
from datetime import datetime, timezone

BOT_WORDS = ("bot", "crawler", "spider", "curl", "wget", "python-requests", "k6", "httpclient")


def parse_device(user_agent: str) -> str:
    """Clasificación simple del agente de usuario: bot, tablet, mobile, desktop o unknown."""
    ua = (user_agent or "").lower()
    if not ua:
        return "unknown"
    if any(word in ua for word in BOT_WORDS):
        return "bot"
    if "ipad" in ua or "tablet" in ua or ("android" in ua and "mobile" not in ua):
        return "tablet"
    if "mobi" in ua or "iphone" in ua or "android" in ua:
        return "mobile"
    return "desktop"


def parse_ts(value) -> datetime:
    """Convierte la marca de tiempo ISO 8601 del evento a datetime con zona UTC."""
    ts = datetime.fromisoformat(value)
    return ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)


def summarize(code: str, clicks: list[dict], truncated: bool = False, recent_n: int = 10) -> dict:
    """Agrega una lista de clics (dicts con ts, device, user_agent) en estadísticas para el panel."""
    by_day = Counter()
    by_device = Counter()
    for c in clicks:
        ts = c["ts"]
        by_day[ts.astimezone(timezone.utc).strftime("%Y-%m-%d")] += 1
        by_device[c.get("device") or "unknown"] += 1
    recent = sorted(clicks, key=lambda c: c["ts"], reverse=True)[:recent_n]
    return {
        "code": code,
        "total": len(clicks),
        "truncated": truncated,
        "by_day": [{"date": d, "clicks": n} for d, n in sorted(by_day.items())],
        "by_device": dict(by_device),
        "recent": [
            {"ts": c["ts"].isoformat(), "device": c.get("device") or "unknown", "user_agent": c.get("user_agent", "")}
            for c in recent
        ],
    }
