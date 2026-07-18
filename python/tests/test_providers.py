import json

from tronixmesh.agents.providers import StubProvider, extract_json_object, get_provider
from tronixmesh.agents.workers import research_worker, review_worker, structure_worker


def test_stub_provider_and_workers():
    prov = StubProvider()
    r = research_worker("Acme vs Beta", provider=prov)
    assert r["role"] == "research"
    assert r["provider"] == "stub"
    s = structure_worker(r, provider=prov)
    assert s["framed"]["sensitivity"] == "confidential"
    v = review_worker(s, provider=prov)
    assert v["verdict"]


def test_get_provider_defaults_stub(monkeypatch):
    monkeypatch.delenv("TRONIX_WORKER_PROVIDER", raising=False)
    assert get_provider().name == "stub"
    monkeypatch.setenv("TRONIX_WORKER_PROVIDER", "anthropic")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("TRONIX_ANTHROPIC_API_KEY", raising=False)
    # No key → soft stub
    assert get_provider().name == "stub"


def test_extract_json_embedded():
    raw = "here you go\n```json\n" + json.dumps({"a": 1}) + "\n```"
    assert extract_json_object(raw)["a"] == 1
