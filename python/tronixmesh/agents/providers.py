"""
LLM provider adapters — recommendations only; never grant authority.

Default: stub (no network). Set TRONIX_WORKER_PROVIDER=anthropic|gemini and API keys
to call live models. Failures fall back to stub-shaped output (worker soft-fail).
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Optional, Protocol


class WorkerProvider(Protocol):
    name: str

    def complete(self, *, system: str, user: str) -> str: ...


@dataclass
class StubProvider:
    name: str = "stub"

    def complete(self, *, system: str, user: str) -> str:
        _ = system
        # Deterministic JSON the workers can parse
        if "research" in user.lower() or "query" in user.lower():
            q = user.strip().splitlines()[-1][:200]
            return json.dumps(
                {
                    "findings": [
                        {"claim": f"synthetic finding for: {q}", "confidence": 0.82, "source": "stub"}
                    ],
                    "recommendation": "structure_for_confidential_review",
                }
            )
        if "structure" in system.lower() or "frame" in user.lower():
            return json.dumps(
                {
                    "framed": {
                        "thesis": "structured synthetic thesis",
                        "risks": ["synthetic-risk"],
                        "sensitivity": "confidential",
                    },
                    "recommendation": "review",
                }
            )
        return json.dumps(
            {
                "verdict": "accept_with_notes",
                "notes": ["stub review — human remains Tier 0"],
                "recommendation": "complete",
            }
        )


def _http_json(
    url: str,
    *,
    headers: dict[str, str],
    body: dict[str, Any],
    timeout: float = 60.0,
) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail[:500]}") from exc


@dataclass
class AnthropicProvider:
    """Direct Anthropic Messages API — optional live path."""

    api_key: str
    model: str = "claude-sonnet-4-20250514"
    name: str = "anthropic"

    def complete(self, *, system: str, user: str) -> str:
        payload = _http_json(
            "https://api.anthropic.com/v1/messages",
            headers={
                "content-type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            body={
                "model": self.model,
                "max_tokens": 1024,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            },
        )
        blocks = payload.get("content") or []
        texts = [b.get("text", "") for b in blocks if isinstance(b, dict) and b.get("type") == "text"]
        return "\n".join(texts).strip()


@dataclass
class GeminiProvider:
    """Direct Google Gemini generateContent — optional live path."""

    api_key: str
    model: str = "gemini-2.0-flash"
    name: str = "gemini"

    def complete(self, *, system: str, user: str) -> str:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )
        payload = _http_json(
            url,
            headers={"content-type": "application/json"},
            body={
                "system_instruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": user}]}],
            },
        )
        candidates = payload.get("candidates") or []
        if not candidates:
            return ""
        parts = (((candidates[0] or {}).get("content") or {}).get("parts")) or []
        return "\n".join(p.get("text", "") for p in parts if isinstance(p, dict)).strip()


_JSON_RE = re.compile(r"\{[\s\S]*\}")


def extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        val = json.loads(text)
        if isinstance(val, dict):
            return val
    except json.JSONDecodeError:
        pass
    m = _JSON_RE.search(text)
    if not m:
        raise ValueError("no JSON object in model output")
    val = json.loads(m.group(0))
    if not isinstance(val, dict):
        raise ValueError("model JSON is not an object")
    return val


def get_provider(name: Optional[str] = None) -> WorkerProvider:
    """
    Resolve provider from argument or TRONIX_WORKER_PROVIDER.
    Values: stub (default) | anthropic | gemini
    """
    choice = (name or os.environ.get("TRONIX_WORKER_PROVIDER") or "stub").strip().lower()
    if choice in {"", "stub", "none", "offline"}:
        return StubProvider()
    if choice == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("TRONIX_ANTHROPIC_API_KEY")
        if not key:
            return StubProvider()
        model = os.environ.get("TRONIX_ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        return AnthropicProvider(api_key=key, model=model)
    if choice == "gemini":
        key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("TRONIX_GEMINI_API_KEY")
        if not key:
            return StubProvider()
        model = os.environ.get("TRONIX_GEMINI_MODEL", "gemini-2.0-flash")
        return GeminiProvider(api_key=key, model=model)
    raise ValueError(f"unknown TRONIX_WORKER_PROVIDER: {choice!r}")
