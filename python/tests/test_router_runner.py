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


def _stack(*, faults: FaultInjector | None = None, verify: bool = False):
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
    router = RulesRouter(reg)
    mem = CellMemoryStore(":memory:")
    runner = IdempotentStepRunner(
        router=router,
        handoff=handoff,
        memory=mem,
        provenance=prov,
        max_retries=2,
        faults=faults or FaultInjector(),
    )
    return runner, reg


def test_router_escalates_on_ambiguity():
    runner, _ = _stack()
    decision = runner.router.classify(
        {"function": "research", "candidates": ["research", "structure"], "confidence": 0.5}
    )
    assert decision.action == "escalate"


def test_runner_routes_and_commits():
    runner, _ = _stack()
    result = runner.run_routed_handoff(
        task_id="t1",
        step_name="to-structure",
        source=RESEARCH_PUBLIC,
        intent={"function": "structure", "confidence": 0.9},
        payload={"doc": "synthetic"},
    )
    assert result.ok
    assert result.attempts == 1
    assert result.handoff is not None and result.handoff.ok


def test_f1_transient_retries_then_success():
    faults = FaultInjector(FaultPlan(transient_destination_failures=2))
    runner, _ = _stack(faults=faults)
    result = runner.run_routed_handoff(
        task_id="t2",
        step_name="to-structure",
        source=RESEARCH_PUBLIC,
        intent={"function": "structure", "confidence": 0.9},
        payload={"doc": "retry"},
    )
    assert result.ok
    assert result.attempts == 3  # 2 injected fails + success


def test_f9_idempotent_replay():
    runner, _ = _stack()
    kwargs = dict(
        task_id="t3",
        step_name="to-review",
        source=STRUCTURE_CONF,
        intent={"function": "review", "confidence": 0.95},
        payload={"analysis": "x"},
    )
    first = runner.run_routed_handoff(**kwargs)
    second = runner.run_routed_handoff(**kwargs)
    assert first.ok and second.ok
    assert second.replayed


def test_f10_invalid_signature_injected():
    faults = FaultInjector(FaultPlan(force_signature_invalid=True))
    runner, _ = _stack(faults=faults, verify=True)
    key, pub = generate_ed25519_key("k")
    result = runner.run_routed_handoff(
        task_id="t4",
        step_name="to-structure",
        source=RESEARCH_PUBLIC,
        intent={"function": "structure", "confidence": 0.9},
        payload={},
        signing_key=key,
        verify_public_key=pub,
    )
    assert not result.ok
    assert "signature" in result.reason
