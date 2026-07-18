"""Telemetry correlation — attach correlation IDs to provenance / operator surfaces."""

from __future__ import annotations

import contextvars
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional


_correlation: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "tronix_correlation_id", default=None
)


def new_correlation_id() -> str:
    return str(uuid.uuid4())


def get_correlation_id() -> Optional[str]:
    return _correlation.get()


def set_correlation_id(correlation_id: str) -> contextvars.Token:
    return _correlation.set(correlation_id)


def reset_correlation_id(token: contextvars.Token) -> None:
    _correlation.reset(token)


@dataclass(frozen=True)
class TelemetryContext:
    correlation_id: str
    task_id: str
    step: Optional[str] = None

    def as_payload(self, **extra: Any) -> dict[str, Any]:
        body = {
            "correlation_id": self.correlation_id,
            "task_id": self.task_id,
            "ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        }
        if self.step:
            body["step"] = self.step
        body.update(extra)
        return body


def enrich_payload(payload: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Merge active correlation_id into a provenance payload."""
    out = dict(payload or {})
    cid = get_correlation_id()
    if cid and "correlation_id" not in out:
        out["correlation_id"] = cid
    return out
