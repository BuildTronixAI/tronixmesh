"""Failure-injection harness for Phase B F-series behaviors."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class FaultPlan:
    """Declarative faults applied by name during a run."""

    transient_destination_failures: int = 0
    force_unhealthy_destination: bool = False
    force_signature_invalid: bool = False
    force_channel_violation: bool = False
    force_ambiguity: bool = False
    force_hash_mismatch_on_read: bool = False


@dataclass
class FaultInjector:
    """
    Counters / switches consulted by IdempotentStepRunner and tests.

    Not a chaos monkey for production — a deterministic harness for F1–F10.
    """

    plan: FaultPlan = field(default_factory=FaultPlan)
    _transient_remaining: int = 0

    def __post_init__(self) -> None:
        self._transient_remaining = self.plan.transient_destination_failures

    def should_fail_transient(self) -> bool:
        if self._transient_remaining > 0:
            self._transient_remaining -= 1
            return True
        return False

    def destination_healthy_override(self) -> Optional[bool]:
        if self.plan.force_unhealthy_destination:
            return False
        return None

    def corrupt_verify(self) -> bool:
        return self.plan.force_signature_invalid

    def force_channel_deny(self) -> bool:
        return self.plan.force_channel_violation

    def force_ambiguity(self) -> bool:
        return self.plan.force_ambiguity


StepFn = Callable[[], None]
