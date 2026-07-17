"""v1.1 fractal-grid coordinates (Phase B canonical form)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


SENSITIVITY_ORDER = ("public", "internal", "confidential", "restricted", "top-secret")


@dataclass(frozen=True)
class MeshCoordinate:
    """
    Canonical address:
    {outer}.{middle_org}.{middle_domain}.{function}.{sensitivity}.{model_tier}.{modality}.{context_size}

    Example: L2R.Buildtronix.Engineering.research.public.balanced.text.long
    """

    outer: str
    middle_org: str
    middle_domain: str
    function: str
    sensitivity: str
    model_tier: str
    modality: str
    context_size: str
    alias: Optional[str] = None  # optional v2.3 8-tuple alias slot (schema-forward)

    def __post_init__(self) -> None:
        parts = [
            self.outer,
            self.middle_org,
            self.middle_domain,
            self.function,
            self.sensitivity,
            self.model_tier,
            self.modality,
            self.context_size,
        ]
        for p in parts:
            if not p or "." in p or " " in p:
                raise ValueError(f"invalid coordinate segment: {p!r}")
        if self.sensitivity not in SENSITIVITY_ORDER:
            raise ValueError(f"unknown sensitivity: {self.sensitivity}")

    @classmethod
    def parse(cls, value: str) -> MeshCoordinate:
        parts = value.strip().split(".")
        if len(parts) != 8:
            raise ValueError(
                f"coordinate must have 8 dotted segments, got {len(parts)}: {value!r}"
            )
        return cls(*parts)

    def canonical(self) -> str:
        return ".".join(
            [
                self.outer,
                self.middle_org,
                self.middle_domain,
                self.function,
                self.sensitivity,
                self.model_tier,
                self.modality,
                self.context_size,
            ]
        )

    def __str__(self) -> str:
        return self.canonical()

    def middle_cell(self) -> str:
        return f"{self.outer}.{self.middle_org}.{self.middle_domain}"

    def sensitivity_rank(self) -> int:
        return SENSITIVITY_ORDER.index(self.sensitivity)

    def is_sensitivity_increase(self, other: MeshCoordinate) -> bool:
        """True if moving from self → other increases sensitivity."""
        return other.sensitivity_rank() > self.sensitivity_rank()
