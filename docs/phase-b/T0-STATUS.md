# Phase B — T0 Status

**T0 started:** 2026-07-17  
**Authorization:** Gate 0 signed — Christopher C. Leiser, Chairman  
**Plan status:** Approved for Build  
**Updated:** 2026-07-18

## Doctrine alignment

Architecture v2.0: [`../architecture/TRONIXMESH-ARCHITECTURE-v2.md`](../architecture/TRONIXMESH-ARCHITECTURE-v2.md)  
Condensed doctrine: [`../architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../architecture/TRONIXMESH-DESIGN-DOCTRINE.md)  
Phase B slice: [`../architecture/PHASE-B-SLICE.md`](../architecture/PHASE-B-SLICE.md)

**In force now:** coordinate-native addressing · fail-closed · runtime owns handoff authority · LLM untrusted · proof-native schema · hash-chain audit · four-topology invariants (reduced) · Postgres JSONB cell memory (ADR-0005).  
**Deferred:** Decision Tokens · Witness/Little Voice · Heartbeat force-tests · RR-0056 Postgres production DSN · BOB/Robert/Council personas (Phase C+) · Redis.

## Delivered

| Item | Location | Tests |
|------|----------|-------|
| Coordinate parsing (v1.1 8-segment) | `python/tronixmesh/coordinate.py` | pass |
| Proof-native envelope + ADR-0004 signature block | `python/tronixmesh/envelope.py` | pass |
| Ed25519 / HMAC signing helpers | `python/tronixmesh/signing.py` | pass |
| Provenance append-only hash chain (SQLite) | `python/tronixmesh/provenance.py` | pass |
| Coordinate registry | `python/tronixmesh/registry.py` | pass |
| Channel rules (default-deny) | `python/tronixmesh/channel.py` | pass |
| Minimal authority (bootstrap grants) | `python/tronixmesh/authority.py` | pass |
| Handoff primitive | `python/tronixmesh/handoff.py` | pass |
| Feature flags | `python/tronixmesh/flags.py` | — |
| Governance state types (fail-closed transitions) | `python/tronixmesh/governance.py` | pass |
| Vultr inventory (T0) | `docs/phase-b/ops/VULTR-INVENTORY.md` | — |
| ADR-0005 Accepted (Postgres JSONB cell memory) | `docs/phase-b/adr/0005-cell-memory-store.md` | — |
| Cell memory (scoped TTL; SQLite stand-in) | `python/tronixmesh/memory.py` | pass |
| Rules router (escalate on ambiguity) | `python/tronixmesh/router.py` | pass |
| Idempotent step runner + fault injection | `python/tronixmesh/runner.py` / `faults.py` | pass |
| Eval set v0 (synthetic) | `python/evals/v0/` | pass |

```bash
cd python && pip install -e ".[dev]" && pytest
```

## Next (T8–T16)

1. Wire Postgres DSN when Vultr host is confirmed (provenance + cell memory)  
2. Three agent runtimes (research / structure / review) on LangGraph — enforcement stays outside  
3. Operator CLI surface (resume / quarantine / replay)  
4. Eval v1 gold labels + FP/FN campaign reporting  
5. Backup/restore drill (A5) once Postgres exists  

## IP note

Runtime code lives under `python/` in this repository per current Authorized for Build path. Keep claim-sensitive expansion and internal fixtures out of public marketing surfaces; relocate to private eng repo if counsel requires.
