"""Cell memory — scoped TTL store (Postgres JSONB logical model; SQLite stand-in)."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_iso(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


@dataclass(frozen=True)
class MemoryEntry:
    key: str
    value: dict[str, Any]
    scope_tags: tuple[str, ...]
    expires_at: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
            "scope_tags": list(self.scope_tags),
            "expires_at": self.expires_at,
            "created_at": self.created_at,
        }


class ScopeViolation(PermissionError):
    """Raised when a read/write lacks required scope tags."""


class CellMemoryStore:
    """
    Logical model matches ADR-0005 Postgres JSONB cell memory.

    Local/CI uses SQLite. Production path should point at Postgres with the same
    columns once a Vultr DSN is available.
    """

    def __init__(self, path: str | Path = ":memory:") -> None:
        self._path = str(path)
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cell_memory (
                key TEXT PRIMARY KEY,
                value_json TEXT NOT NULL,
                scope_tags_json TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def put(
        self,
        key: str,
        value: dict[str, Any],
        *,
        scope_tags: Sequence[str],
        ttl_seconds: int,
        writer_scopes: Sequence[str],
    ) -> MemoryEntry:
        tags = tuple(sorted(set(scope_tags)))
        if not tags:
            raise ValueError("scope_tags required")
        if not set(tags).issubset(set(writer_scopes)):
            raise ScopeViolation("writer missing required scope tags")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")

        now = _utc_now()
        entry = MemoryEntry(
            key=key,
            value=value,
            scope_tags=tags,
            expires_at=_iso(now + timedelta(seconds=ttl_seconds)),
            created_at=_iso(now),
        )
        self._conn.execute(
            """
            INSERT INTO cell_memory(key, value_json, scope_tags_json, expires_at, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value_json=excluded.value_json,
                scope_tags_json=excluded.scope_tags_json,
                expires_at=excluded.expires_at,
                created_at=excluded.created_at
            """,
            (
                entry.key,
                json.dumps(entry.value, sort_keys=True, separators=(",", ":")),
                json.dumps(list(entry.scope_tags), separators=(",", ":")),
                entry.expires_at,
                entry.created_at,
            ),
        )
        self._conn.commit()
        return entry

    def get(self, key: str, *, reader_scopes: Sequence[str]) -> Optional[MemoryEntry]:
        self.sweep_expired()
        row = self._conn.execute(
            "SELECT * FROM cell_memory WHERE key = ?", (key,)
        ).fetchone()
        if row is None:
            return None
        entry = self._row_to_entry(row)
        if not set(entry.scope_tags).issubset(set(reader_scopes)):
            raise ScopeViolation("reader missing required scope tags")
        return entry

    def delete(self, key: str, *, writer_scopes: Sequence[str]) -> bool:
        entry = self.get(key, reader_scopes=writer_scopes)
        if entry is None:
            return False
        self._conn.execute("DELETE FROM cell_memory WHERE key = ?", (key,))
        self._conn.commit()
        return True

    def sweep_expired(self, *, now: Optional[datetime] = None) -> int:
        stamp = _iso(now or _utc_now())
        cur = self._conn.execute(
            "DELETE FROM cell_memory WHERE expires_at <= ?", (stamp,)
        )
        self._conn.commit()
        return cur.rowcount

    def keys(self, *, reader_scopes: Sequence[str]) -> list[str]:
        self.sweep_expired()
        out: list[str] = []
        for row in self._conn.execute("SELECT * FROM cell_memory"):
            entry = self._row_to_entry(row)
            if set(entry.scope_tags).issubset(set(reader_scopes)):
                out.append(entry.key)
        return out

    def _row_to_entry(self, row: sqlite3.Row) -> MemoryEntry:
        return MemoryEntry(
            key=row["key"],
            value=json.loads(row["value_json"]),
            scope_tags=tuple(json.loads(row["scope_tags_json"])),
            expires_at=row["expires_at"],
            created_at=row["created_at"],
        )


def scopes_cover(required: Iterable[str], held: Iterable[str]) -> bool:
    return set(required).issubset(set(held))
