# Tronix Mesh — Phase B Runtime (Python)

**Status:** Approved for Build (Gate 0) · T0 in progress · package `0.3.0`

> Agents reason. The runtime governs. Humans retain ultimate authority.

**Scope:** Coordinates, proof-native envelopes (ADR-0004), provenance, channels, minimal authority, cell memory (ADR-0005), rules router, LangGraph pilot chain (ADR-0002 — enforcement outside the graph), operator CLI.  
**Doctrine:** [`../docs/architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../docs/architecture/TRONIXMESH-DESIGN-DOCTRINE.md)

```bash
cd python
pip install -e ".[dev]"
pytest

# Operator surface
tronixmesh-ops run-pilot "synthetic competitor query" --task-id demo-1
tronixmesh-ops provenance demo-1
tronixmesh-ops list --status completed
```

Workers are **stubs** (no live LLM). Signature verify / MeshResolver hot path remain **feature-flagged** (`TRONIX_VERIFY_SIGNATURES=1`). Decision Tokens and persona agents are **out of Phase B**.
