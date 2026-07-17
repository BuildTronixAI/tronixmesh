"""Channel rules — default-deny at boundaries; tag-add on sensitivity increase."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .coordinate import MeshCoordinate


@dataclass(frozen=True)
class ChannelDecision:
    allowed: bool
    reason: str
    tags_to_add: tuple[str, ...] = ()


@dataclass(frozen=True)
class ChannelRule:
    """Allowlist rule between coordinate patterns (exact middle-cell + function pair)."""

    source_function: str
    dest_function: str
    allow_sensitivity_increase: bool = True
    require_authority: bool = False
    tags_on_increase: tuple[str, ...] = ("sensitivity-elevated",)


class ChannelRuleEngine:
    """Fail-closed channel evaluation for Phase B single-tenant Engineering cell."""

    def __init__(self, rules: Optional[list[ChannelRule]] = None) -> None:
        self._rules = rules or [
            ChannelRule(
                source_function="research",
                dest_function="structure",
                allow_sensitivity_increase=True,
                require_authority=True,
                tags_on_increase=("sensitivity-elevated", "confidential-context"),
            ),
            ChannelRule(
                source_function="structure",
                dest_function="review",
                allow_sensitivity_increase=False,
                require_authority=False,
            ),
        ]

    def evaluate(
        self,
        source: MeshCoordinate,
        destination: MeshCoordinate,
        *,
        has_authority: bool = False,
    ) -> ChannelDecision:
        if source.middle_cell() != destination.middle_cell():
            return ChannelDecision(False, "cross-middle-cell denied in Phase B")

        matching = [
            r
            for r in self._rules
            if r.source_function == source.function and r.dest_function == destination.function
        ]
        if not matching:
            return ChannelDecision(False, "no channel rule (default deny)")

        rule = matching[0]
        increasing = source.is_sensitivity_increase(destination)

        if increasing and not rule.allow_sensitivity_increase:
            return ChannelDecision(False, "sensitivity increase not permitted by rule")

        if increasing and rule.require_authority and not has_authority:
            return ChannelDecision(False, "authority required for sensitivity-increasing handoff")

        tags = rule.tags_on_increase if increasing else ()
        return ChannelDecision(True, "allowed", tags_to_add=tags)
