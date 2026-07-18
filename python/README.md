# Tronix Mesh — Phase B Runtime (Python)

**Status:** Approved for Build (Gate 0) · T8+ in progress · package `0.4.0`

> Agents reason. The runtime governs. Humans retain ultimate authority.

**Scope:** Coordinates, proof-native envelopes, provenance, channels, authority, cell memory, rules router, LangGraph pilot (enforcement outside), pluggable workers, telemetry correlation, security floor, eval v1, operator CLI.  
**Doctrine:** [`../docs/architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../docs/architecture/TRONIXMESH-DESIGN-DOCTRINE.md) · **Runbook:** [`../docs/phase-b/ops/OPERATOR-RUNBOOK.md`](../docs/phase-b/ops/OPERATOR-RUNBOOK.md)

```bash
cd python
pip install -e ".[dev]"
pytest                          # 47 passed
tronixmesh-ops eval-campaign --set v1
tronixmesh-ops run-pilot "synthetic competitor query" --task-id demo-1
```

Default worker provider is **stub**. Set `TRONIX_WORKER_PROVIDER=anthropic|gemini` plus API keys for live recommendations (still no authority). Signature verify remains feature-flagged (`TRONIX_VERIFY_SIGNATURES=1`).
