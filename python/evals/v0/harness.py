"""Eval v0 harness — score RulesRouter against synthetic labels."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tronixmesh.registry import CoordinateRegistry
from tronixmesh.router import (
    RESEARCH_PUBLIC,
    REVIEW_CONF,
    STRUCTURE_CONF,
    RulesRouter,
)


CASES_PATH = Path(__file__).with_name("cases.jsonl")


@dataclass
class CaseScore:
    case_id: str
    ok: bool
    predicted_action: str
    gold_action: str
    detail: str


@dataclass
class EvalReport:
    total: int
    correct: int
    fp: int
    fn: int
    silent_forced: int
    scores: list[CaseScore]

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total else 0.0


def load_cases(path: Path = CASES_PATH) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            cases.append(json.loads(line))
    return cases


def _pilot_registry() -> CoordinateRegistry:
    reg = CoordinateRegistry()
    reg.register(RESEARCH_PUBLIC, "agent://research")
    reg.register(STRUCTURE_CONF, "agent://structure")
    reg.register(REVIEW_CONF, "agent://review")
    return reg


def score_case(router: RulesRouter, case: dict[str, Any]) -> CaseScore:
    decision = router.classify(case["intent"])
    gold = case["gold_action"]
    predicted = decision.action

    # Fail-closed non-routes both satisfy "do not silently wrong-route"
    if gold == "escalate" and predicted in ("escalate", "unroutable"):
        return CaseScore(case["id"], True, predicted, gold, decision.reason)

    if gold == "route" and predicted == "route" and decision.destination is not None:
        # Function family must match gold when provided
        gold_fn = case.get("gold_function")
        mapped = router.function_map.get(gold_fn) if gold_fn else None
        if mapped is None or decision.destination.canonical() == mapped:
            return CaseScore(case["id"], True, predicted, gold, decision.reason)
        return CaseScore(
            case["id"], False, predicted, gold, "routed to wrong coordinate"
        )

    return CaseScore(case["id"], False, predicted, gold, decision.reason)


def run_eval_v0(*, confidence_threshold: float = 0.75) -> EvalReport:
    router = RulesRouter(_pilot_registry(), confidence_threshold=confidence_threshold)
    scores: list[CaseScore] = []
    fp = fn = silent = 0

    for case in load_cases():
        s = score_case(router, case)
        scores.append(s)
        cls = case["sensitivity_class"]
        if not s.ok:
            if cls == "public" and s.predicted_action == "route" and case["gold_action"] != "route":
                fp += 1
            elif cls == "public" and s.predicted_action == "route":
                # wrong coordinate on public set
                if "wrong" in s.detail:
                    fp += 1
            if cls == "boundary" and s.predicted_action != "route":
                fn += 1
            if cls == "ambiguous" and s.predicted_action == "route":
                silent += 1

    correct = sum(1 for s in scores if s.ok)
    return EvalReport(
        total=len(scores),
        correct=correct,
        fp=fp,
        fn=fn,
        silent_forced=silent,
        scores=scores,
    )
