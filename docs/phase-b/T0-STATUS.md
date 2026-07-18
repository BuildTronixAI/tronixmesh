# Phase B — T0 Status

**T0 started:** 2026-07-17  
**Authorization:** Gate 0 signed — Christopher C. Leiser, Chairman  
**Plan status:** Approved for Build  
**Updated:** 2026-07-18

## Doctrine alignment

Architecture v2.0: [`../architecture/TRONIXMESH-ARCHITECTURE-v2.md`](../architecture/TRONIXMESH-ARCHITECTURE-v2.md)  
Condensed doctrine: [`../architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../architecture/TRONIXMESH-DESIGN-DOCTRINE.md)  
Phase B slice: [`../architecture/PHASE-B-SLICE.md`](../architecture/PHASE-B-SLICE.md)

**In force now:** coordinate-native addressing · fail-closed · runtime owns handoff authority · LLM untrusted · proof-native schema · hash-chain audit · four-topology invariants (reduced) · Postgres JSONB cell memory (ADR-0005) · LangGraph pilot chain with Mesh enforcement outside (ADR-0002).  
**Deferred:** Decision Tokens · Witness/Little Voice · Heartbeat force-tests · RR-0056 Postgres production DSN · BOB/Robert/Council personas (Phase C+) · Redis · real model API workers.

## Delivered

| Item | Location | Tests |
|------|----------|-------|
| Coordinate / envelope / provenance / handoff | `python/tronixmesh/*` | pass |
| Cell memory (ADR-0005) | `memory.py` | pass |
| Rules router + fault injection | `router.py` / `runner.py` / `faults.py` | pass |
| Eval set v0 | `python/evals/v0/` | pass |
| Task store (resume / quarantine) | `taskstore.py` | pass |
| LangGraph competitive-intel chain | `agents/chain.py` | pass |
| Stub workers (research / structure / review) | `agents/workers.py` | pass |
| Operator CLI | `cli.py` → `tronixmesh-ops` | pass |

```bash
cd python && pip install -e ".[dev]" && pytest
# 31 passed

tronixmesh-ops run-pilot "synthetic competitor query" --task-id demo-1
tronixmesh-ops provenance demo-1
tronixmesh-ops quarantine demo-1 --reason "ops hold"
tronixmesh-ops resume demo-1
```

## Next

1. Wire Postgres DSN when Vultr host is confirmed (provenance + cell memory + tasks)  
2. Replace stub workers with Direct Anthropic / Gemini calls (still recommendations only)  
3. Eval v1 gold labels + FP/FN campaign reporting  
4. Backup/restore drill (A5) once Postgres exists  
5. Soft-launch readiness review — still gated by staged rollout  

## IP note

Runtime code lives under `python/` in this repository per current Authorized for Build path. Keep claim-sensitive expansion and internal fixtures out of public marketing surfaces; relocate to private eng repo if counsel requires.
