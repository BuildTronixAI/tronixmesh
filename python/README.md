# Tronix Mesh — Phase B Runtime (Python)

**Status:** Approved for Build (Gate 0) · T0 started 2026-07-17  

> Agents reason. The runtime governs. Humans retain ultimate authority.

**Scope (Phase B slice):** Coordinate registry, proof-native Context Envelope (ADR-0004), provenance hash chain, channel rules, minimal authority, governance state types.  
**Doctrine:** [`../docs/architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../docs/architecture/TRONIXMESH-DESIGN-DOCTRINE.md)

```bash
cd python
pip install -e ".[dev]"
pytest
```

Verification of signatures / MeshResolver hot path is **feature-flagged** (`TRONIX_VERIFY_SIGNATURES=1` to enable). Decision Tokens and persona agents are **out of Phase B**.
