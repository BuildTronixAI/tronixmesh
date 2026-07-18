"""Agent workers — LLM-untrusted; recommendations only; never grant authority."""

from __future__ import annotations

from typing import Any, Optional

from .providers import StubProvider, WorkerProvider, extract_json_object, get_provider


_RESEARCH_SYSTEM = (
    "You are a research worker in Tronix Mesh. Recommend findings only. "
    "You have NO authority to escalate sensitivity or approve actions. "
    "Reply with a single JSON object: "
    '{"findings":[{"claim":str,"confidence":number,"source":str}],'
    '"recommendation":"structure_for_confidential_review"}'
)

_STRUCTURE_SYSTEM = (
    "You are a structure worker. Frame research for confidential review. "
    "You have NO authority. Reply JSON only: "
    '{"framed":{"thesis":str,"risks":[str],"sensitivity":"confidential"},'
    '"recommendation":"review"}'
)

_REVIEW_SYSTEM = (
    "You are a review worker. Recommend accept/reject notes only. "
    "Humans remain Tier 0. Reply JSON only: "
    '{"verdict":"accept_with_notes"|"reject","notes":[str],"recommendation":"complete"}'
)


def _complete_json(provider: WorkerProvider, *, system: str, user: str) -> dict[str, Any]:
    try:
        raw = provider.complete(system=system, user=user)
        return extract_json_object(raw)
    except Exception:
        # Soft-fail worker path — never elevate; fall back to stub-shaped output
        stub = StubProvider()
        return extract_json_object(stub.complete(system=system, user=user))


def research_worker(
    query: str,
    *,
    prior: dict[str, Any] | None = None,
    provider: Optional[WorkerProvider] = None,
) -> dict[str, Any]:
    _ = prior
    prov = provider or get_provider()
    data = _complete_json(prov, system=_RESEARCH_SYSTEM, user=f"Research query:\n{query}")
    findings = data.get("findings") or [
        {"claim": f"synthetic finding for: {query}", "confidence": 0.5, "source": prov.name}
    ]
    return {
        "role": "research",
        "query": query,
        "findings": findings,
        "recommendation": data.get("recommendation") or "structure_for_confidential_review",
        "provider": prov.name,
    }


def structure_worker(
    research: dict[str, Any],
    *,
    provider: Optional[WorkerProvider] = None,
) -> dict[str, Any]:
    prov = provider or get_provider()
    data = _complete_json(
        prov,
        system=_STRUCTURE_SYSTEM,
        user="Frame this research JSON:\n" + str(research),
    )
    findings = research.get("findings") or []
    framed = data.get("framed") or {
        "thesis": findings[0]["claim"] if findings else "no findings",
        "risks": ["synthetic-risk"],
        "sensitivity": "confidential",
    }
    return {
        "role": "structure",
        "framed": framed,
        "recommendation": data.get("recommendation") or "review",
        "provider": prov.name,
    }


def review_worker(
    structure: dict[str, Any],
    *,
    provider: Optional[WorkerProvider] = None,
) -> dict[str, Any]:
    prov = provider or get_provider()
    data = _complete_json(
        prov,
        system=_REVIEW_SYSTEM,
        user="Review this structured JSON:\n" + str(structure),
    )
    framed = structure.get("framed") or {}
    return {
        "role": "review",
        "verdict": data.get("verdict") or "accept_with_notes",
        "notes": data.get("notes") or ["review — human remains Tier 0"],
        "thesis": framed.get("thesis"),
        "recommendation": data.get("recommendation") or "complete",
        "provider": prov.name,
    }
