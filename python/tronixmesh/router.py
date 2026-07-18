"""Routing / classification — rules first; escalate on ambiguity (F2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .coordinate import MeshCoordinate
from .registry import CoordinateRegistry


# Competitive-intel pilot chain (Engineering cell)
RESEARCH_PUBLIC = "L2R.Buildtronix.Engineering.research.public.balanced.text.long"
STRUCTURE_CONF = "L2R.Buildtronix.Engineering.structure.confidential.frontier.text.medium"
REVIEW_CONF = "L2R.Buildtronix.Engineering.review.confidential.frontier.text.long"


@dataclass(frozen=True)
class RouteDecision:
    action: str  # route | escalate | unroutable
    destination: Optional[MeshCoordinate]
    confidence: float
    reason: str
    gold_function: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.action == "route" and self.destination is not None


class RulesRouter:
    """
    Stage 1–2 rules classifier for the 3-agent pilot.

    - High-confidence function match → route to registered coordinate.
    - Ambiguity / low confidence → escalate (F2), never silent wrong route.
    - Unknown / unregistered destination → unroutable (F3).
    """

    def __init__(
        self,
        registry: CoordinateRegistry,
        *,
        confidence_threshold: float = 0.75,
        function_map: Optional[dict[str, str]] = None,
    ) -> None:
        self.registry = registry
        self.confidence_threshold = confidence_threshold
        self.function_map = function_map or {
            "research": RESEARCH_PUBLIC,
            "structure": STRUCTURE_CONF,
            "review": REVIEW_CONF,
            # Boundary synonyms used by eval fixtures
            "competitive_research": RESEARCH_PUBLIC,
            "structure_confidential": STRUCTURE_CONF,
            "review_gate": REVIEW_CONF,
        }

    def classify(self, intent: dict[str, Any]) -> RouteDecision:
        """
        intent keys (synthetic eval-friendly):
          - function: str | None
          - candidates: list[str] optional competing functions
          - confidence: float optional (defaults to 1.0 when single clear function)
          - requires_confidential: bool optional hint for boundary cases
        """
        function = intent.get("function")
        candidates = list(intent.get("candidates") or [])
        confidence = float(intent.get("confidence", 1.0 if function and not candidates else 0.0))

        if candidates and len(set(candidates)) > 1:
            return RouteDecision(
                action="escalate",
                destination=None,
                confidence=confidence,
                reason="F2: classification ambiguity — multiple candidates",
                gold_function=function,
            )

        if not function:
            return RouteDecision(
                action="escalate",
                destination=None,
                confidence=confidence,
                reason="F2: missing function — escalate",
            )

        if confidence < self.confidence_threshold:
            return RouteDecision(
                action="escalate",
                destination=None,
                confidence=confidence,
                reason="F2: confidence below threshold",
                gold_function=function,
            )

        dest_s = self.function_map.get(function)
        if dest_s is None:
            return RouteDecision(
                action="unroutable",
                destination=None,
                confidence=confidence,
                reason=f"F3: unknown function {function!r}",
                gold_function=function,
            )

        dest = MeshCoordinate.parse(dest_s)
        if self.registry.lookup(dest) is None:
            return RouteDecision(
                action="unroutable",
                destination=dest,
                confidence=confidence,
                reason="F3: UNROUTABLE destination not registered",
                gold_function=function,
            )

        if intent.get("requires_confidential") and dest.sensitivity == "public":
            # Force boundary path when gold says confidential needed
            alt = MeshCoordinate.parse(STRUCTURE_CONF)
            if self.registry.lookup(alt) is not None:
                return RouteDecision(
                    action="route",
                    destination=alt,
                    confidence=confidence,
                    reason="boundary: confidential required",
                    gold_function=function,
                )

        return RouteDecision(
            action="route",
            destination=dest,
            confidence=confidence,
            reason="rules match",
            gold_function=function,
        )
