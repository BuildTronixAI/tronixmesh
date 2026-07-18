from tronixmesh.agents.chain import CompetitiveIntelChain, MeshRuntime
from tronixmesh.faults import FaultInjector, FaultPlan
from tronixmesh.runner import IdempotentStepRunner
from tronixmesh.router import RulesRouter
from tronixmesh.taskstore import TaskStatus


def test_pilot_chain_completes():
    chain = CompetitiveIntelChain(MeshRuntime.create())
    result = chain.start("Procore vs Autodesk competitive notes", task_id="pilot-1")
    assert result["status"] == TaskStatus.COMPLETED.value
    assert result["research"]["role"] == "research"
    assert result["structure"]["role"] == "structure"
    assert result["review"]["verdict"] == "accept_with_notes"
    assert chain.runtime.provenance.verify_chain()
    events = [e.event_type for e in chain.runtime.provenance.events_for_task("pilot-1")]
    assert "HANDOFF" in events
    assert "TASK_COMPLETED" in events


def test_pilot_quarantines_on_injected_channel_fault():
    rt = MeshRuntime.create()
    # Rebuild runner with fault injector forcing channel deny on handoffs
    rt.runner = IdempotentStepRunner(
        router=RulesRouter(rt.registry),
        handoff=rt.handoff,
        memory=rt.memory,
        provenance=rt.provenance,
        faults=FaultInjector(FaultPlan(force_channel_violation=True)),
    )
    chain = CompetitiveIntelChain(rt)
    # graph was built with old runner — rebuild
    from tronixmesh.agents.chain import build_pilot_graph

    chain.graph = build_pilot_graph(rt)
    result = chain.start("fault injection query", task_id="pilot-fault")
    assert result["status"] == TaskStatus.QUARANTINED.value
    assert "F7" in (result.get("error") or "")
    task = rt.tasks.get("pilot-fault")
    assert task is not None and task.status == TaskStatus.QUARANTINED


def test_resume_completed_returns_terminal_state():
    chain = CompetitiveIntelChain(MeshRuntime.create())
    first = chain.start("resume case", task_id="pilot-resume")
    second = chain.resume("pilot-resume")
    assert first["status"] == TaskStatus.COMPLETED.value
    assert second["status"] == TaskStatus.COMPLETED.value


def test_rerun_hits_idempotent_step_replay():
    chain = CompetitiveIntelChain(MeshRuntime.create())
    chain.start("replay case", task_id="pilot-replay")
    # Force another full invoke; committed handoffs should STEP_REPLAY
    chain.start("replay case", task_id="pilot-replay")
    replays = [
        e
        for e in chain.runtime.provenance.events_for_task("pilot-replay")
        if e.event_type == "STEP_REPLAY"
    ]
    assert len(replays) >= 1