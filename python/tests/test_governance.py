import pytest

from tronixmesh.governance import GovernanceState, can_transition, may_execute, transition


def test_happy_path_transitions():
    s = GovernanceState.DRAFT
    for nxt in (
        GovernanceState.PROPOSED,
        GovernanceState.UNDER_REVIEW,
        GovernanceState.APPROVED,
        GovernanceState.AUTHORIZED,
        GovernanceState.EXECUTING,
        GovernanceState.EXECUTED,
        GovernanceState.VERIFIED,
        GovernanceState.SEALED,
    ):
        s = transition(s, nxt)
    assert s is GovernanceState.SEALED


def test_fail_closed_illegal_transition():
    with pytest.raises(PermissionError):
        transition(GovernanceState.PROPOSED, GovernanceState.EXECUTED)


def test_reviewers_cannot_execute():
    assert not may_execute(GovernanceState.UNDER_REVIEW)
    assert not may_execute(GovernanceState.APPROVED)
    assert may_execute(GovernanceState.AUTHORIZED)
    assert can_transition(GovernanceState.UNDER_REVIEW, GovernanceState.BLOCKED)
