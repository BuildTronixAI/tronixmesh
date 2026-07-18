"""
LangGraph competitive-intel chain: research → structure → review.

Doctrine: agents reason; runtime governs. Every inter-agent transition goes
through IdempotentStepRunner (channel / authority / envelope / provenance).
LangGraph only sequences worker calls — it is not an enforcement plane.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Optional, TypedDict

from langgraph.graph import END, START, StateGraph

from ..authority import BootstrapGrant, MinimalAuthorityModule
from ..channel import ChannelRuleEngine
from ..flags import FeatureFlags
from ..handoff import HandoffService
from ..memory import CellMemoryStore
from ..provenance import ProvenanceStore
from ..registry import CoordinateRegistry
from ..router import RESEARCH_PUBLIC, REVIEW_CONF, STRUCTURE_CONF, RulesRouter
from ..runner import IdempotentStepRunner, StepResult
from ..taskstore import TaskStatus, TaskStore
from ..telemetry import new_correlation_id, reset_correlation_id, set_correlation_id
from . import workers


class PilotState(TypedDict, total=False):
    task_id: str
    query: str
    research: dict[str, Any]
    structure: dict[str, Any]
    review: dict[str, Any]
    status: str
    error: Optional[str]
    last_step: str


def _pilot_registry() -> CoordinateRegistry:
    reg = CoordinateRegistry()
    reg.register(RESEARCH_PUBLIC, "agent://research")
    reg.register(STRUCTURE_CONF, "agent://structure")
    reg.register(REVIEW_CONF, "agent://review")
    return reg


def _pilot_authority() -> MinimalAuthorityModule:
    auth = MinimalAuthorityModule()
    auth.add_grant(
        BootstrapGrant(
            grant_id="grant-pub-to-conf",
            source_function="research",
            dest_function="structure",
            allow_sensitivity_increase=True,
        )
    )
    return auth


@dataclass
class MeshRuntime:
    """Shared Mesh enforcement stack for the pilot graph."""

    registry: CoordinateRegistry
    provenance: ProvenanceStore
    memory: CellMemoryStore
    tasks: TaskStore
    runner: IdempotentStepRunner
    handoff: HandoffService

    @classmethod
    def create(
        cls,
        *,
        db_path: str = ":memory:",
        verify_signatures: bool = False,
    ) -> "MeshRuntime":
        # Separate SQLite DBs when durable. :memory: stays true in-memory (not ":memory:.prov" files).
        if db_path == ":memory:":
            provenance = ProvenanceStore(":memory:")
            memory = CellMemoryStore(":memory:")
            tasks = TaskStore(":memory:")
        else:
            provenance = ProvenanceStore(f"{db_path}.prov")
            memory = CellMemoryStore(f"{db_path}.mem")
            tasks = TaskStore(f"{db_path}.tasks")
        registry = _pilot_registry()
        handoff = HandoffService(
            registry=registry,
            channels=ChannelRuleEngine(),
            authority=_pilot_authority(),
            provenance=provenance,
            flags=FeatureFlags(verify_signatures=verify_signatures),
        )
        runner = IdempotentStepRunner(
            router=RulesRouter(registry),
            handoff=handoff,
            memory=memory,
            provenance=provenance,
        )
        return cls(
            registry=registry,
            provenance=provenance,
            memory=memory,
            tasks=tasks,
            runner=runner,
            handoff=handoff,
        )


def build_pilot_graph(runtime: MeshRuntime):
    """Compile LangGraph StateGraph with Mesh-governed transitions."""

    def _fail(state: PilotState, step: str, reason: str) -> PilotState:
        runtime.tasks.quarantine(state["task_id"], reason)
        runtime.provenance.append(
            task_id=state["task_id"],
            event_type="QUARANTINE",
            payload={"step": step, "reason": reason},
        )
        return {
            **state,
            "status": TaskStatus.QUARANTINED.value,
            "error": reason,
            "last_step": step,
        }

    def _governed_handoff(
        *,
        state: PilotState,
        step_name: str,
        source: str,
        intent: dict[str, Any],
        payload: dict[str, Any],
    ) -> StepResult:
        return runtime.runner.run_routed_handoff(
            task_id=state["task_id"],
            step_name=step_name,
            source=source,
            intent=intent,
            payload=payload,
        )

    def research_node(state: PilotState) -> PilotState:
        runtime.tasks.update(
            state["task_id"], status=TaskStatus.RUNNING, step="research", clear_error=True
        )
        research = workers.research_worker(state["query"])
        # Ingress: research coordinate is the worker seat (no inbound handoff required)
        runtime.provenance.append(
            task_id=state["task_id"],
            event_type="WORKER_OUTPUT",
            payload={"step": "research", "recommendation": research.get("recommendation")},
        )
        return {
            **state,
            "research": research,
            "status": TaskStatus.RUNNING.value,
            "last_step": "research",
            "error": None,
        }

    def structure_node(state: PilotState) -> PilotState:
        research = state.get("research") or {}
        step = _governed_handoff(
            state=state,
            step_name="research_to_structure",
            source=RESEARCH_PUBLIC,
            intent={"function": "structure", "confidence": 0.9, "requires_confidential": True},
            payload={"research": research},
        )
        if not step.ok:
            return _fail(state, "research_to_structure", step.reason)

        structure = workers.structure_worker(research)
        runtime.tasks.update(state["task_id"], step="structure", payload={"structure": structure})
        runtime.provenance.append(
            task_id=state["task_id"],
            event_type="WORKER_OUTPUT",
            payload={"step": "structure", "recommendation": structure.get("recommendation")},
        )
        return {
            **state,
            "structure": structure,
            "status": TaskStatus.RUNNING.value,
            "last_step": "structure",
            "error": None,
        }

    def review_node(state: PilotState) -> PilotState:
        structure = state.get("structure") or {}
        step = _governed_handoff(
            state=state,
            step_name="structure_to_review",
            source=STRUCTURE_CONF,
            intent={"function": "review", "confidence": 0.95},
            payload={"structure": structure},
        )
        if not step.ok:
            return _fail(state, "structure_to_review", step.reason)

        review = workers.review_worker(structure)
        runtime.tasks.update(
            state["task_id"],
            status=TaskStatus.COMPLETED,
            step="review",
            payload={"review": review},
            clear_error=True,
        )
        runtime.provenance.append(
            task_id=state["task_id"],
            event_type="WORKER_OUTPUT",
            payload={"step": "review", "verdict": review.get("verdict")},
        )
        runtime.provenance.append(
            task_id=state["task_id"],
            event_type="TASK_COMPLETED",
            payload={"step": "review"},
        )
        return {
            **state,
            "review": review,
            "status": TaskStatus.COMPLETED.value,
            "last_step": "review",
            "error": None,
        }

    def route_after_structure(state: PilotState) -> str:
        if state.get("status") == TaskStatus.QUARANTINED.value:
            return "quarantine_end"
        return "review"

    def route_after_research(state: PilotState) -> str:
        if state.get("status") == TaskStatus.QUARANTINED.value:
            return "quarantine_end"
        return "structure"

    def quarantine_end(state: PilotState) -> PilotState:
        return state

    g: StateGraph = StateGraph(PilotState)
    g.add_node("research", research_node)
    g.add_node("structure", structure_node)
    g.add_node("review", review_node)
    g.add_node("quarantine_end", quarantine_end)
    g.add_edge(START, "research")
    g.add_conditional_edges(
        "research",
        route_after_research,
        {"structure": "structure", "quarantine_end": "quarantine_end"},
    )
    g.add_conditional_edges(
        "structure",
        route_after_structure,
        {"review": "review", "quarantine_end": "quarantine_end"},
    )
    g.add_edge("review", END)
    g.add_edge("quarantine_end", END)
    return g.compile()


class CompetitiveIntelChain:
    """Operator-facing facade over the LangGraph pilot + Mesh runtime."""

    def __init__(self, runtime: Optional[MeshRuntime] = None) -> None:
        self.runtime = runtime or MeshRuntime.create()
        self.graph = build_pilot_graph(self.runtime)

    def start(self, query: str, *, task_id: Optional[str] = None) -> PilotState:
        tid = task_id or str(uuid.uuid4())
        cid = new_correlation_id()
        token = set_correlation_id(cid)
        try:
            if self.runtime.tasks.get(tid) is None:
                self.runtime.tasks.create(
                    tid, step="start", payload={"query": query, "correlation_id": cid}
                )
            else:
                self.runtime.tasks.update(
                    tid,
                    status=TaskStatus.RUNNING,
                    step="start",
                    payload={"query": query, "correlation_id": cid},
                    clear_error=True,
                )

            self.runtime.provenance.append(
                task_id=tid,
                event_type="TASK_START",
                payload={"query": query, "correlation_id": cid},
            )

            initial: PilotState = {
                "task_id": tid,
                "query": query,
                "status": TaskStatus.RUNNING.value,
                "error": None,
                "last_step": "start",
            }
            result = self.graph.invoke(initial)
            return result  # type: ignore[return-value]
        finally:
            reset_correlation_id(token)

    def resume(self, task_id: str) -> PilotState:
        rec = self.runtime.tasks.get(task_id)
        if rec is None:
            raise KeyError(f"unknown task: {task_id}")
        if rec.status == TaskStatus.COMPLETED:
            return {
                "task_id": task_id,
                "query": rec.payload.get("query", ""),
                "status": rec.status.value,
                "last_step": rec.step,
                "error": None,
                **{k: v for k, v in rec.payload.items() if k in ("research", "structure", "review")},
            }
        query = rec.payload.get("query") or ""
        # Re-run from start; idempotent step runner prevents duplicate commits.
        return self.start(query, task_id=task_id)
