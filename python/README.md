# Tronix Mesh — Phase B Runtime (Python)

**Status:** Approved for Build (Gate 0) · T0 started 2026-07-17  
**Scope:** Coordinate registry, proof-native Context Envelope (ADR-0004), provenance hash chain, channel rules, minimal authority.

```bash
cd python
pip install -e ".[dev]"
pytest
```

Verification of signatures / MeshResolver hot path is **feature-flagged** (`TRONIX_VERIFY_SIGNATURES=1` to enable).
