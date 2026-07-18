"""Durable task state for resume / quarantine / operator surface."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    QUARANTINED = "quarantined"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class TaskRecord:
    task_id: str
    status: TaskStatus
    step: str
    payload: dict[str, Any]
    error: Optional[str]
    updated_at: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "step": self.step,
            "payload": self.payload,
            "error": self.error,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
        }


class TaskStore:
    """SQLite task ledger (Postgres later per ADR-0003)."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self._path = str(path)
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                step TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                error TEXT,
                updated_at TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def create(self, task_id: str, *, step: str = "start", payload: Optional[dict] = None) -> TaskRecord:
        now = _utc_now()
        rec = TaskRecord(
            task_id=task_id,
            status=TaskStatus.PENDING,
            step=step,
            payload=payload or {},
            error=None,
            updated_at=now,
            created_at=now,
        )
        self._conn.execute(
            """
            INSERT INTO tasks(task_id, status, step, payload_json, error, updated_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rec.task_id,
                rec.status.value,
                rec.step,
                json.dumps(rec.payload, sort_keys=True, separators=(",", ":")),
                rec.error,
                rec.updated_at,
                rec.created_at,
            ),
        )
        self._conn.commit()
        return rec

    def get(self, task_id: str) -> Optional[TaskRecord]:
        row = self._conn.execute(
            "SELECT * FROM tasks WHERE task_id = ?", (task_id,)
        ).fetchone()
        return self._row(row) if row else None

    def update(
        self,
        task_id: str,
        *,
        status: Optional[TaskStatus] = None,
        step: Optional[str] = None,
        payload: Optional[dict[str, Any]] = None,
        error: Optional[str] = None,
        clear_error: bool = False,
    ) -> TaskRecord:
        rec = self.get(task_id)
        if rec is None:
            raise KeyError(f"unknown task: {task_id}")
        new = TaskRecord(
            task_id=rec.task_id,
            status=status or rec.status,
            step=step if step is not None else rec.step,
            payload=payload if payload is not None else rec.payload,
            error=None if clear_error else (error if error is not None else rec.error),
            updated_at=_utc_now(),
            created_at=rec.created_at,
        )
        self._conn.execute(
            """
            UPDATE tasks SET status=?, step=?, payload_json=?, error=?, updated_at=?
            WHERE task_id=?
            """,
            (
                new.status.value,
                new.step,
                json.dumps(new.payload, sort_keys=True, separators=(",", ":")),
                new.error,
                new.updated_at,
                new.task_id,
            ),
        )
        self._conn.commit()
        return new

    def quarantine(self, task_id: str, reason: str) -> TaskRecord:
        return self.update(task_id, status=TaskStatus.QUARANTINED, error=reason)

    def list(self, *, status: Optional[TaskStatus] = None) -> list[TaskRecord]:
        if status is None:
            rows = self._conn.execute("SELECT * FROM tasks ORDER BY created_at").fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY created_at",
                (status.value,),
            ).fetchall()
        return [self._row(r) for r in rows]

    def _row(self, row: sqlite3.Row) -> TaskRecord:
        return TaskRecord(
            task_id=row["task_id"],
            status=TaskStatus(row["status"]),
            step=row["step"],
            payload=json.loads(row["payload_json"]),
            error=row["error"],
            updated_at=row["updated_at"],
            created_at=row["created_at"],
        )
