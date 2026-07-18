"""Append-only hash-chained provenance store (in-memory Phase B primitive)."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

from .telemetry import enrich_payload


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class ProvenanceEvent:
    seq: int
    task_id: str
    event_type: str
    payload: dict[str, Any]
    prev_hash: str
    entry_hash: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "seq": self.seq,
            "task_id": self.task_id,
            "event_type": self.event_type,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "entry_hash": self.entry_hash,
            "created_at": self.created_at,
        }


def _hash_entry(prev_hash: str, body: dict[str, Any]) -> str:
    material = json.dumps(
        {"prev_hash": prev_hash, **body},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


class ProvenanceStore:
    """
    Append-only ledger. SQLite backend for durable pilot; ":memory:" for tests.

    Application must not UPDATE/DELETE ledger rows (enforced by API; DB role in prod).
    """

    GENESIS = "0" * 64

    def __init__(self, path: str | Path = ":memory:") -> None:
        self._path = str(path)
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS provenance (
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                prev_hash TEXT NOT NULL,
                entry_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def tip_hash(self) -> str:
        row = self._conn.execute(
            "SELECT entry_hash FROM provenance ORDER BY seq DESC LIMIT 1"
        ).fetchone()
        return row["entry_hash"] if row else self.GENESIS

    def append(
        self,
        *,
        task_id: str,
        event_type: str,
        payload: Optional[dict[str, Any]] = None,
    ) -> ProvenanceEvent:
        prev = self.tip_hash()
        created_at = _utc_now()
        enriched = enrich_payload(payload)
        body = {
            "task_id": task_id,
            "event_type": event_type,
            "payload": enriched,
            "created_at": created_at,
        }
        entry_hash = _hash_entry(prev, body)
        cur = self._conn.execute(
            """
            INSERT INTO provenance (task_id, event_type, payload_json, prev_hash, entry_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                event_type,
                json.dumps(enriched, sort_keys=True),
                prev,
                entry_hash,
                created_at,
            ),
        )
        self._conn.commit()
        return ProvenanceEvent(
            seq=int(cur.lastrowid),
            task_id=task_id,
            event_type=event_type,
            payload=enriched,
            prev_hash=prev,
            entry_hash=entry_hash,
            created_at=created_at,
        )

    def events_for_task(self, task_id: str) -> list[ProvenanceEvent]:
        rows = self._conn.execute(
            "SELECT * FROM provenance WHERE task_id = ? ORDER BY seq ASC",
            (task_id,),
        ).fetchall()
        return [self._row_to_event(r) for r in rows]

    def all_events(self) -> list[ProvenanceEvent]:
        rows = self._conn.execute("SELECT * FROM provenance ORDER BY seq ASC").fetchall()
        return [self._row_to_event(r) for r in rows]

    def verify_chain(self, events: Optional[Iterable[ProvenanceEvent]] = None) -> bool:
        prev = self.GENESIS
        for event in events if events is not None else self.all_events():
            if event.prev_hash != prev:
                return False
            body = {
                "task_id": event.task_id,
                "event_type": event.event_type,
                "payload": event.payload,
                "created_at": event.created_at,
            }
            if _hash_entry(prev, body) != event.entry_hash:
                return False
            prev = event.entry_hash
        return True

    @staticmethod
    def _row_to_event(row: sqlite3.Row) -> ProvenanceEvent:
        return ProvenanceEvent(
            seq=int(row["seq"]),
            task_id=row["task_id"],
            event_type=row["event_type"],
            payload=json.loads(row["payload_json"]),
            prev_hash=row["prev_hash"],
            entry_hash=row["entry_hash"],
            created_at=row["created_at"],
        )
