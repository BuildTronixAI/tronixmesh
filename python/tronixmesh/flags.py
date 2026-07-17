"""Feature flags — schema is proof-native; behavior is flagged (ADR-0001 / plan §1.2)."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class FeatureFlags:
    """Runtime behavior toggles. Schema fields exist regardless of these flags."""

    verify_signatures: bool = False
    mesh_resolver_hot_path: bool = False
    distributed_enforcement: bool = False

    @classmethod
    def from_env(cls) -> FeatureFlags:
        return cls(
            verify_signatures=_env_bool("TRONIX_VERIFY_SIGNATURES", False),
            mesh_resolver_hot_path=_env_bool("TRONIX_MESH_RESOLVER", False),
            distributed_enforcement=_env_bool("TRONIX_DISTRIBUTED_ENFORCEMENT", False),
        )
