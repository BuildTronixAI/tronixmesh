"""F-series chaos / validation harness (plan §4.2) — deterministic fault injection."""

from __future__ import annotations

from tronixmesh.authority import BootstrapGrant, MinimalAuthorityModule
from tronixmesh.channel import ChannelRuleEngine
from tronixmesh.faults import FaultInjector, FaultPlan
from tronixmesh.flags import FeatureFlags
from tronixmesh.handoff import HandoffService
from tronixmesh.memory import CellMemoryStore
from tronixmesh.provenance import ProvenanceStore
from tronixmesh.registry import CoordinateRegistry
from tronixmesh.router import RESEARCH_PUBLIC, REVIEW_CONF, STRUCTURE_CONF, RulesRouter
from tronixmesh.runner import IdempotentStepRunner
from tronixmesh.signing import generate_ed25519_key


def _runner(faults: FaultInjector | None = None, *, verify: bool = False) -> IdempotentStepRunner:
    reg = CoordinateRegistry()
    reg.register(RESEARCH_PUBLIC, "agent://research")
    reg.register(STRUCTURE_CONF, "agent://structure")
    reg.register(REVIEW_CONF, "agent://review")
    auth = MinimalAuthorityModule()
    auth.add_grant(
        BootstrapGrant(
            grant_id="grant-pub-to-conf",
            source_function="research",
            dest_function="structure",
            allow_sensitivity_increase=True,
        )
    )
    prov = ProvenanceStore(":memory:")
    handoff = HandoffService(
        registry=reg,
        channels=ChannelRuleEngine(),
        authority=auth,
        provenance=prov,
        flags=FeatureFlags(verify_signatures=verify),
    )
    return IdempotentStepRunner(
        router=RulesRouter(reg),
        handoff=handoff,
        memory=CellMemoryStore(":memory:"),
        provenance=prov,
        max_retries=2,
        faults=faults or FaultInjector(),
    )


def test_f1_transient_then_ok():
    r = _runner(FaultInjector(FaultPlan(transient_destination_failures=1)))
    out = r.run_routed_handoff(
        task_id="f1",
        step_name="s",
        source=RESEARCH_PUBLIC,
        intent={"function": "structure", "confidence": 0.9},
        payload={"n": 1},
    )
    assert out.ok and out.attempts == 2


def test_f2_ambiguity_escalates():
    r = _runner(FaultInjector(FaultPlan(force_ambiguity=True)))
    out = r.run_routed_handoff(
        task_id="f2",
        step_name="s",
        source=RESEARCH_PUBLIC,
        intent={"function": "structure", "confidence": 0.9},
        payload={},
    )
    assert not out.ok and out.route and out.route.action == "escalate"


def test_f3_unroutable_unknown_function():
    r = _runner()
    out = r.run_routed_handoff(
        task_id="f3",
        step_name="s",
        source=RESEARCH_PUBLIC,
        intent={"function": "nope", "confidence": 0.99},
        payload={},
    )
    assert not out.ok
    assert out.route and out.route.action == "unroutable"


def test_f7_channel_violation_injected():
    r = _runner(FaultInjector(FaultPlan(force_channel_violation=True)))
    out = r.run_routed_handoff(
        task_id="f7",
        step_name="s",
        source=RESEARCH_PUBLIC,
        intent={"function": "structure", "confidence": 0.9},
        payload={},
    )
    assert not out.ok and "F7" in out.reason


def test_f9_idempotent_replay():
    r = _runner()
    kwargs = dict(
        task_id="f9",
        step_name="s",
        source=STRUCTURE_CONF,
        intent={"function": "review", "confidence": 0.95},
        payload={"x": 1},
    )
    assert r.run_routed_handoff(**kwargs).ok
    second = r.run_routed_handoff(**kwargs)
    assert second.ok and second.replayed


def test_f10_signature_invalid():
    r = _runner(FaultInjector(FaultPlan(force_signature_invalid=True)), verify=True)
    key, pub = generate_ed25519_key("f10")
    out = r.run_routed_handoff(
        task_id="f10",
        step_name="s",
        source=RESEARCH_PUBLIC,
        intent={"function": "structure", "confidence": 0.9},
        payload={},
        signing_key=key,
        verify_public_key=pub,
    )
    assert not out.ok and "signature" in out.reason


def test_f8_hash_mismatch_detected():
    prov = ProvenanceStore(":memory:")
    prov.append(task_id="f8", event_type="A", payload={"n": 1})
    # Tamper with stored payload without updating hash
    prov._conn.execute(
        "UPDATE provenance SET payload_json = ? WHERE task_id = ?",
        ('{"n": 2}', "f8"),
    )
    prov._conn.commit()
    assert prov.verify_chain() is False
