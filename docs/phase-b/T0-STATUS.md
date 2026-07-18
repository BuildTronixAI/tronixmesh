# Phase B — T0 / T8+ Status

**T0 started:** 2026-07-17  
**Authorization:** Gate 0 signed — Christopher C. Leiser, Chairman  
**Plan status:** Approved for Build  
**Updated:** 2026-07-18  
**Package:** `tronixmesh` 0.4.0

## Doctrine alignment

Architecture v2.0: [`../architecture/TRONIXMESH-ARCHITECTURE-v2.md`](../architecture/TRONIXMESH-ARCHITECTURE-v2.md)  
Condensed doctrine: [`../architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../architecture/TRONIXMESH-DESIGN-DOCTRINE.md)  
Phase B slice: [`../architecture/PHASE-B-SLICE.md`](../architecture/PHASE-B-SLICE.md)  
Operator runbook: [`ops/OPERATOR-RUNBOOK.md`](./ops/OPERATOR-RUNBOOK.md)

**In force:** coordinate-native · fail-closed · runtime governs handoffs · LLM untrusted · proof-native schema · hash-chain audit · ADR-0002/0004/0005 · telemetry correlation IDs · security floor checks · eval v1 campaign.  
**Deferred:** Decision Tokens · Witness/Little Voice · Heartbeat · RR-0056 live Postgres cutover · BOB/Robert/Council personas · Redis · soft-launch.

## Window coverage

| Window | Status |
|--------|--------|
| T0–T8 | Done (schema, provenance, routing, authority, faults) |
| T8–T13 | Done (LangGraph agents, idempotent runner, telemetry correlation) |
| T13–T16 | Done (cell memory scope, task resume, operator CLI) |
| T16–T19 | Done (rules classifier + eval v1 gold / FP/FN campaign) |
| T19–T23 | Done (F-series chaos harness + GitHub Actions Python CI) |
| T23–T27 | Partial (security floor module + runbook; E2E live models optional) |
| T27–T30 | Open (eval campaigns ongoing; Soft Launch Readiness Review gated) |

## Delivered (latest)

| Item | Location |
|------|----------|
| Pluggable workers (stub / Anthropic / Gemini) | `agents/providers.py` + `workers.py` |
| Correlation IDs on provenance | `telemetry.py` |
| Security floor (S1–S3) | `security.py` |
| Eval v1 + FP/FN campaign | `evals/v1/` · `tronixmesh-ops eval-campaign` |
| F-series chaos tests | `tests/test_chaos_f_series.py` |
| Postgres DSN ping helper | `postgres.py` (cutover when Vultr ready) |
| Operator runbook | `docs/phase-b/ops/OPERATOR-RUNBOOK.md` |
| Python CI | `.github/workflows/python-ci.yml` |

```bash
cd python && pip install -e ".[dev]" && pytest
# 47 passed

tronixmesh-ops eval-campaign --set v1
tronixmesh-ops run-pilot "synthetic competitor query" --task-id demo-1
```

## Next (toward soft-launch gate)

1. Vultr Postgres DSN → cut over provenance / memory / tasks; A5 backup/restore drill  
2. Soft Launch Readiness Review (plan §4.7 / §9) — still **not** authorized by this increment  
3. Optional: enable live workers in a private env with keys (never in public CI)  

## IP note

Runtime under `python/`. Keep claim-sensitive expansion and real confidential fixtures out of public marketing surfaces.
