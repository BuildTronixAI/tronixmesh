"""Eval v1 campaign reporter — accuracy + FP/FN + confusion breakdown."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from evals.v0.harness import CaseScore, load_cases, score_case
from tronixmesh.registry import CoordinateRegistry
from tronixmesh.router import RESEARCH_PUBLIC, REVIEW_CONF, STRUCTURE_CONF, RulesRouter

CASES_PATH = Path(__file__).with_name("cases.jsonl")


@dataclass
class CampaignReport:
    set_name: str
    total: int
    correct: int
    accuracy: float
    fp: int
    fn: int
    silent_forced: int
    fp_rate_public: float
    fn_rate_boundary: float
    public_n: int
    boundary_n: int
    ambiguous_n: int
    meets_floor: bool
    scores: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _pilot_registry() -> CoordinateRegistry:
    reg = CoordinateRegistry()
    reg.register(RESEARCH_PUBLIC, "agent://research")
    reg.register(STRUCTURE_CONF, "agent://structure")
    reg.register(REVIEW_CONF, "agent://review")
    return reg


def run_campaign(
    *,
    set_name: str = "v1",
    cases_path: Path = CASES_PATH,
    confidence_threshold: float = 0.75,
) -> CampaignReport:
    router = RulesRouter(_pilot_registry(), confidence_threshold=confidence_threshold)
    cases = load_cases(cases_path)
    scores: list[CaseScore] = []
    fp = fn = silent = 0
    public_n = boundary_n = ambiguous_n = 0

    for case in cases:
        cls = case["sensitivity_class"]
        if cls == "public":
            public_n += 1
        elif cls == "boundary":
            boundary_n += 1
        elif cls == "ambiguous":
            ambiguous_n += 1

        s = score_case(router, case)
        scores.append(s)

        if cls == "public" and s.predicted_action == "route" and case["gold_action"] != "route":
            fp += 1
        elif cls == "public" and not s.ok and "wrong" in s.detail:
            fp += 1
        if cls == "boundary" and case["gold_action"] == "route" and s.predicted_action != "route":
            fn += 1
        if cls == "ambiguous" and s.predicted_action == "route":
            silent += 1

    correct = sum(1 for s in scores if s.ok)
    total = len(scores)
    accuracy = correct / total if total else 0.0
    fp_rate = fp / public_n if public_n else 0.0
    fn_rate = fn / boundary_n if boundary_n else 0.0
    meets = (
        accuracy >= 0.90
        and fp_rate <= 0.02
        and fn_rate <= 0.05
        and silent == 0
    )
    return CampaignReport(
        set_name=set_name,
        total=total,
        correct=correct,
        accuracy=accuracy,
        fp=fp,
        fn=fn,
        silent_forced=silent,
        fp_rate_public=fp_rate,
        fn_rate_boundary=fn_rate,
        public_n=public_n,
        boundary_n=boundary_n,
        ambiguous_n=ambiguous_n,
        meets_floor=meets,
        scores=[asdict(s) for s in scores],
    )


def report_json(report: CampaignReport) -> str:
    return json.dumps(report.to_dict(), indent=2, sort_keys=True)
