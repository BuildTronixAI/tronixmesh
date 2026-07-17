"""Handoff primitive — channel + authority + envelope + provenance commit."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Optional

from .authority import MinimalAuthorityModule
from .channel import ChannelRuleEngine
from .coordinate import MeshCoordinate
from .envelope import ContextEnvelope
from .flags import FeatureFlags
from .provenance import ProvenanceStore
from .registry import CoordinateRegistry
from .signing import SigningKey


@dataclass(frozen=True)
class HandoffResult:
    ok: bool
    reason: str
    envelope: Optional[ContextEnvelope] = None
    grant_id: Optional[str] = None


class HandoffService:
    def __init__(
        self,
        *,
        registry: CoordinateRegistry,
        channels: ChannelRuleEngine,
        authority: MinimalAuthorityModule,
        provenance: ProvenanceStore,
        flags: Optional[FeatureFlags] = None,
    ) -> None:
        self.registry = registry
        self.channels = channels
        self.authority = authority
        self.provenance = provenance
        self.flags = flags or FeatureFlags.from_env()

    def handoff(
        self,
        *,
        task_id: str,
        source: MeshCoordinate | str,
        destination: MeshCoordinate | str,
        payload: dict[str, Any],
        signing_key: Optional[SigningKey] = None,
        verify_public_key: Optional[bytes] = None,
    ) -> HandoffResult:
        src = source if isinstance(source, MeshCoordinate) else MeshCoordinate.parse(source)
        dst = (
            destination
            if isinstance(destination, MeshCoordinate)
            else MeshCoordinate.parse(destination)
        )

        if self.registry.lookup(dst) is None:
            self.provenance.append(
                task_id=task_id,
                event_type="UNROUTABLE",
                payload={"destination": dst.canonical()},
            )
            return HandoffResult(False, "UNROUTABLE: destination not registered")

        increasing = src.is_sensitivity_increase(dst)
        grant_id = None
        if increasing:
            grant_id = self.authority.authorize_handoff(
                source_function=src.function,
                dest_function=dst.function,
                sensitivity_increase=True,
            )

        decision = self.channels.evaluate(
            src, dst, has_authority=(grant_id is not None) if increasing else True
        )

        if not decision.allowed:
            self.provenance.append(
                task_id=task_id,
                event_type="CHANNEL_DENIED",
                payload={"reason": decision.reason, "source": src.canonical(), "dest": dst.canonical()},
            )
            return HandoffResult(False, decision.reason)

        env = ContextEnvelope(
            envelope_id=str(uuid.uuid4()),
            task_id=task_id,
            source=src,
            destination=dst,
            payload=payload,
            authority_refs=[grant_id] if grant_id else [],
            tags=list(decision.tags_to_add),
            governance_ref="phase-b-bootstrap",
            proof_id=None,
        )

        if signing_key is not None:
            env.sign(signing_key)

        if self.flags.verify_signatures:
            if verify_public_key is None or not env.verify(verify_public_key):
                self.provenance.append(
                    task_id=task_id,
                    event_type="SIGNATURE_INVALID",
                    payload={"envelope_id": env.envelope_id},
                )
                return HandoffResult(False, "envelope signature invalid")

        event = self.provenance.append(
            task_id=task_id,
            event_type="HANDOFF",
            payload={
                "envelope_id": env.envelope_id,
                "source": src.canonical(),
                "destination": dst.canonical(),
                "grant_id": grant_id,
                "tags": env.tags,
                "content_hash": env.signature.content_hash,
            },
        )
        env.provenance_ref = event.entry_hash

        return HandoffResult(True, "ok", envelope=env, grant_id=grant_id)
