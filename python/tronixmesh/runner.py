"""Idempotent step runner with retries and failure-injection hooks."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable, Optional

from .faults import FaultInjector
from .handoff import HandoffResult, HandoffService
from .memory import CellMemoryStore
from .provenance import ProvenanceStore
from .router import RouteDecision, RulesRouter
from .signing import SigningKey


@dataclass(frozen=True)
class StepResult:
    ok: bool
    reason: str
    attempts: int
    idempotency_key: str
    route: Optional[RouteDecision] = None
    handoff: Optional[HandoffResult] = None
    replayed: bool = False


def _idem_key(task_id: str, step_name: str, payload: dict[str, Any]) -> str:
    material = json.dumps(
        {"task_id": task_id, "step": step_name, "payload": payload},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


class IdempotentStepRunner:
    """
    Runs one routed handoff step with:
      - idempotency via cell memory (F5/F9)
      - transient retries (F1)
      - routing escalate / unroutable (F2/F3)
      - optional fault injection
    """

    def __init__(
        self,
        *,
        router: RulesRouter,
        handoff: HandoffService,
        memory: CellMemoryStore,
        provenance: ProvenanceStore,
        max_retries: int = 2,
        faults: Optional[FaultInjector] = None,
        memory_scopes: tuple[str, ...] = ("task", "engineering"),
    ) -> None:
        self.router = router
        self.handoff = handoff
        self.memory = memory
        self.provenance = provenance
        self.max_retries = max_retries
        self.faults = faults or FaultInjector()
        self.memory_scopes = memory_scopes

    def run_routed_handoff(
        self,
        *,
        task_id: str,
        step_name: str,
        source: str,
        intent: dict[str, Any],
        payload: dict[str, Any],
        signing_key: Optional[SigningKey] = None,
        verify_public_key: Optional[bytes] = None,
        execute: Optional[Callable[[], None]] = None,
    ) -> StepResult:
        key = _idem_key(task_id, step_name, payload)
        prior = self.memory.get(key, reader_scopes=self.memory_scopes)
        if prior is not None and prior.value.get("committed"):
            self.provenance.append(
                task_id=task_id,
                event_type="STEP_REPLAY",
                payload={"step": step_name, "idempotency_key": key},
            )
            return StepResult(
                ok=True,
                reason="F9: replay — already committed",
                attempts=0,
                idempotency_key=key,
                replayed=True,
            )

        route_intent = dict(intent)
        if self.faults.force_ambiguity():
            route_intent["candidates"] = ["research", "structure"]
            route_intent["confidence"] = 0.4

        decision = self.router.classify(route_intent)
        self.provenance.append(
            task_id=task_id,
            event_type="ROUTE_DECISION",
            payload={
                "step": step_name,
                "action": decision.action,
                "reason": decision.reason,
                "confidence": decision.confidence,
                "destination": decision.destination.canonical() if decision.destination else None,
            },
        )

        if decision.action == "escalate":
            return StepResult(
                False, decision.reason, 0, key, route=decision
            )
        if decision.action == "unroutable" or decision.destination is None:
            return StepResult(
                False, decision.reason, 0, key, route=decision
            )

        healthy_override = self.faults.destination_healthy_override()
        if healthy_override is False:
            rec = self.handoff.registry.lookup(decision.destination)
            if rec is not None:
                rec.healthy = False

        attempts = 0
        last_reason = "not attempted"
        result: Optional[HandoffResult] = None

        while attempts <= self.max_retries:
            attempts += 1
            if self.faults.should_fail_transient():
                last_reason = "F1: transient destination failure"
                self.provenance.append(
                    task_id=task_id,
                    event_type="TRANSIENT_FAIL",
                    payload={"step": step_name, "attempt": attempts},
                )
                continue

            dest_rec = self.handoff.registry.lookup(decision.destination)
            if dest_rec is not None and not dest_rec.healthy:
                last_reason = "F1: destination unhealthy"
                self.provenance.append(
                    task_id=task_id,
                    event_type="TRANSIENT_FAIL",
                    payload={"step": step_name, "attempt": attempts, "reason": last_reason},
                )
                # restore for subsequent attempts unless forced unhealthy for all
                if not self.faults.plan.force_unhealthy_destination:
                    dest_rec.healthy = True
                continue

            if self.faults.force_channel_deny():
                self.provenance.append(
                    task_id=task_id,
                    event_type="CHANNEL_DENIED",
                    payload={"step": step_name, "injected": True},
                )
                return StepResult(
                    False, "F7: channel violation (injected)", attempts, key, route=decision
                )

            verify_key = verify_public_key
            if self.faults.corrupt_verify():
                # Force verify path with a wrong key (caller should enable verify_signatures).
                verify_key = b"\x00" * 32
                if not self.handoff.flags.verify_signatures:
                    last_reason = "F10: signature fault requested but verify_signatures is off"
                    break

            result = self.handoff.handoff(
                task_id=task_id,
                source=source,
                destination=decision.destination,
                payload=payload,
                signing_key=signing_key,
                verify_public_key=verify_key,
            )
            if result.ok:
                if execute is not None:
                    execute()
                self.memory.put(
                    key,
                    {"committed": True, "envelope_id": result.envelope.envelope_id if result.envelope else None},
                    scope_tags=self.memory_scopes,
                    ttl_seconds=86400,
                    writer_scopes=self.memory_scopes,
                )
                self.provenance.append(
                    task_id=task_id,
                    event_type="STEP_COMMITTED",
                    payload={"step": step_name, "idempotency_key": key, "attempts": attempts},
                )
                return StepResult(
                    True, "ok", attempts, key, route=decision, handoff=result
                )

            last_reason = result.reason
            # Non-transient policy failures do not retry
            if result.reason.startswith("UNROUTABLE") or "authority" in result.reason or "channel" in result.reason or "signature" in result.reason:
                break

        return StepResult(
            False,
            last_reason if result is None else result.reason,
            attempts,
            key,
            route=decision,
            handoff=result,
        )
