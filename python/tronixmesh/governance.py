"""
Governance state machine — schema-forward types (Design Doctrine).

Full engine (Decision Tokens, CPR, SEALED flows) is Phase C+.
Phase B may record intended/observed states on provenance events.
Runtime must fail closed if a required state transition is unmet.
"""

from __future__ import annotations

from enum import Enum
from typing import FrozenSet


class GovernanceState(str, Enum):
    """Normative governance states from the Design Doctrine."""

    DRAFT = "DRAFT"
    PROPOSED = "PROPOSED"
    UNDER_REVIEW = "UNDER_REVIEW"
    CPR = "CPR"  # Conditional Pending Review
    APPROVED = "APPROVED"
    BLOCKED = "BLOCKED"
    AUTHORIZED = "AUTHORIZED"
    EXECUTING = "EXECUTING"
    EXECUTED = "EXECUTED"
    VERIFIED = "VERIFIED"
    SEALED = "SEALED"
    ROLLED_BACK = "ROLLED_BACK"


# Happy-path edges (non-exhaustive; BLOCKED/ROLLED_BACK are terminal-ish escapes)
_ALLOWED: dict[GovernanceState, FrozenSet[GovernanceState]] = {
    GovernanceState.DRAFT: frozenset({GovernanceState.PROPOSED}),
    GovernanceState.PROPOSED: frozenset(
        {GovernanceState.UNDER_REVIEW, GovernanceState.BLOCKED}
    ),
    GovernanceState.UNDER_REVIEW: frozenset(
        {
            GovernanceState.CPR,
            GovernanceState.APPROVED,
            GovernanceState.BLOCKED,
        }
    ),
    GovernanceState.CPR: frozenset(
        {GovernanceState.UNDER_REVIEW, GovernanceState.APPROVED, GovernanceState.BLOCKED}
    ),
    GovernanceState.APPROVED: frozenset(
        {GovernanceState.AUTHORIZED, GovernanceState.BLOCKED}
    ),
    GovernanceState.AUTHORIZED: frozenset(
        {GovernanceState.EXECUTING, GovernanceState.BLOCKED}
    ),
    GovernanceState.EXECUTING: frozenset(
        {GovernanceState.EXECUTED, GovernanceState.ROLLED_BACK, GovernanceState.BLOCKED}
    ),
    GovernanceState.EXECUTED: frozenset(
        {GovernanceState.VERIFIED, GovernanceState.ROLLED_BACK}
    ),
    GovernanceState.VERIFIED: frozenset({GovernanceState.SEALED}),
    GovernanceState.SEALED: frozenset(),
    GovernanceState.BLOCKED: frozenset(),
    GovernanceState.ROLLED_BACK: frozenset(),
}


def can_transition(current: GovernanceState, nxt: GovernanceState) -> bool:
    return nxt in _ALLOWED.get(current, frozenset())


def transition(current: GovernanceState, nxt: GovernanceState) -> GovernanceState:
    """Fail closed: raise if transition is not allowed."""
    if not can_transition(current, nxt):
        raise PermissionError(
            f"governance fail-closed: cannot transition {current.value} → {nxt.value}"
        )
    return nxt


def may_execute(state: GovernanceState) -> bool:
    """Execution only from AUTHORIZED or EXECUTING — never from review/recommend states."""
    return state in {GovernanceState.AUTHORIZED, GovernanceState.EXECUTING}
