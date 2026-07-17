"""Coordinate registry — populated endpoints and health."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional

from .coordinate import MeshCoordinate


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class AgentEndpoint:
    coordinate: MeshCoordinate
    endpoint: str
    healthy: bool = True
    last_heartbeat: str = field(default_factory=_utc_now)


class CoordinateRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, AgentEndpoint] = {}

    def register(self, coordinate: MeshCoordinate | str, endpoint: str) -> AgentEndpoint:
        coord = (
            coordinate
            if isinstance(coordinate, MeshCoordinate)
            else MeshCoordinate.parse(coordinate)
        )
        record = AgentEndpoint(coordinate=coord, endpoint=endpoint, healthy=True)
        self._agents[coord.canonical()] = record
        return record

    def lookup(self, coordinate: MeshCoordinate | str) -> Optional[AgentEndpoint]:
        key = coordinate.canonical() if isinstance(coordinate, MeshCoordinate) else coordinate
        return self._agents.get(key)

    def heartbeat(self, coordinate: MeshCoordinate | str, *, healthy: bool = True) -> None:
        rec = self.lookup(coordinate)
        if rec is None:
            raise KeyError(f"coordinate not registered: {coordinate}")
        rec.healthy = healthy
        rec.last_heartbeat = _utc_now()

    def populated(self) -> list[AgentEndpoint]:
        return list(self._agents.values())
