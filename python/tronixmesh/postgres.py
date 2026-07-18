"""
Postgres wiring (ADR-0003 / ADR-0005) — DSN-ready interface.

Phase B ships SQLite stand-ins. When TRONIX_DATABASE_URL / Vultr DSN is set,
operators can validate connectivity here before cutting over stores.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse


@dataclass(frozen=True)
class DatabaseConfig:
    url: str
    backend: str  # sqlite | postgres

    @property
    def is_postgres(self) -> bool:
        return self.backend == "postgres"


def load_database_config(url: Optional[str] = None) -> DatabaseConfig:
    raw = (url or os.environ.get("TRONIX_DATABASE_URL") or "").strip()
    if not raw or raw.startswith("sqlite"):
        return DatabaseConfig(url=raw or "sqlite:///:memory:", backend="sqlite")
    parsed = urlparse(raw)
    if parsed.scheme in {"postgres", "postgresql"}:
        return DatabaseConfig(url=raw, backend="postgres")
    raise ValueError(f"unsupported database URL scheme: {parsed.scheme!r}")


def ping_postgres(url: Optional[str] = None) -> dict:
    """
    Attempt a simple connectivity check. Requires psycopg if URL is postgres.
    Returns a status dict — never raises for missing optional dependency.
    """
    cfg = load_database_config(url)
    if not cfg.is_postgres:
        return {"ok": True, "backend": "sqlite", "detail": "using sqlite stand-in"}
    try:
        import psycopg  # type: ignore
    except ImportError:
        return {
            "ok": False,
            "backend": "postgres",
            "detail": "psycopg not installed — pip install psycopg[binary]",
        }
    try:
        with psycopg.connect(cfg.url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"ok": True, "backend": "postgres", "detail": "ping ok"}
    except Exception as exc:  # noqa: BLE001 — operator surface
        return {"ok": False, "backend": "postgres", "detail": str(exc)[:300]}
