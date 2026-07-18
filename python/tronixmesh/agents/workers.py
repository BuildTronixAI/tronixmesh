"""Agent workers — LLM-untrusted stubs for Phase B (replace with real model calls later)."""

from __future__ import annotations

from typing import Any


def research_worker(query: str, *, prior: dict[str, Any] | None = None) -> dict[str, Any]:
    """Recommend findings only — no authority."""
    _ = prior
    return {
        "role": "research",
        "query": query,
        "findings": [
            {"claim": f"synthetic finding for: {query}", "confidence": 0.82, "source": "stub"}
        ],
        "recommendation": "structure_for_confidential_review",
    }


def structure_worker(research: dict[str, Any]) -> dict[str, Any]:
    findings = research.get("findings") or []
    return {
        "role": "structure",
        "framed": {
            "thesis": findings[0]["claim"] if findings else "no findings",
            "risks": ["synthetic-risk"],
            "sensitivity": "confidential",
        },
        "recommendation": "review",
    }


def review_worker(structure: dict[str, Any]) -> dict[str, Any]:
    framed = structure.get("framed") or {}
    return {
        "role": "review",
        "verdict": "accept_with_notes",
        "notes": ["stub review — human remains Tier 0"],
        "thesis": framed.get("thesis"),
        "recommendation": "complete",
    }
