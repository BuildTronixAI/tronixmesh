# ADR-0005: Cell memory store (Redis vs Postgres)

- Status: **Accepted**
- Date: 2026-07-18
- Deciders: Chris (via T0 inventory default — Cursor execution)
- Inventory: [`../ops/VULTR-INVENTORY.md`](../ops/VULTR-INVENTORY.md)

## Decision

**Postgres JSONB** for Phase B cell memory (TTL + scope tags).

Redis is **not** confirmed on Vultr inventory → do not stand up Redis solely for the pilot. Local / CI stand-in may use **SQLite JSON** with the same logical model (`key`, `scope_tags`, `value`, `expires_at`) until a Postgres DSN is wired.

## Alternatives considered

1. **Redis TTL** — fast ephemeral cell memory; extra infra if absent. Rejected for Phase B absent inventory confirmation.  
2. **Postgres JSONB (chosen)** — one less moving part; aligns with ADR-0003 provenance/task store.  
3. **In-process memory only** — rejected; fails F5 restart survival.

## Rationale

“No new infra during pilot” is a scheduling/ops constraint. Cell memory must survive process restart for in-flight tasks or be reconstructible; Postgres JSONB (SQLite stand-in locally) is the lowest-ops option that meets scope enforcement without inventing Redis ops.

## Consequences

- Scope tags enforced regardless of backend.  
- Switching to Redis later requires a short migration note, not a schema break for envelopes.  
- Technology registry marks Redis Experimental / unused for Phase B until inventory changes.  
- ADR status lives **only** in this file — no separate Decision Log.
