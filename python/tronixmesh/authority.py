"""Phase B minimal authority — bootstrap/static grants (Decision Tokens deferred to Phase C)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class BootstrapGrant:
    grant_id: str
    source_function: str
    dest_function: str
    allow_sensitivity_increase: bool
    expires_at: Optional[datetime] = None

    def is_valid(self, at: Optional[datetime] = None) -> bool:
        now = at or _utc_now()
        if self.expires_at is not None and now >= self.expires_at:
            return False
        return True


class MinimalAuthorityModule:
    """Static grant table for public→confidential without Decision Tokens."""

    def __init__(self) -> None:
        self._grants: Dict[str, BootstrapGrant] = {}

    def add_grant(self, grant: BootstrapGrant) -> None:
        self._grants[grant.grant_id] = grant

    def authorize_handoff(
        self,
        *,
        source_function: str,
        dest_function: str,
        sensitivity_increase: bool,
    ) -> Optional[str]:
        """Return grant_id if authorized, else None."""
        for grant in self._grants.values():
            if not grant.is_valid():
                continue
            if grant.source_function != source_function or grant.dest_function != dest_function:
                continue
            if sensitivity_increase and not grant.allow_sensitivity_increase:
                continue
            return grant.grant_id
        return None
