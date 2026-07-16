# ADR-0005: Cell memory store (Redis vs Postgres)

- Status: Proposed
- Date: 2026-07-16
- Deciders: Chris (after Vultr inventory)

## Decision

**Pending inventory.** Prefer **whatever already runs on Vultr**. If Redis exists and is operated, use Redis with TTL + scope tags. If not, use **Postgres JSONB** with TTL sweeper — do not stand up Redis solely because a plan mentioned it.

## Alternatives considered

1. **Redis TTL** — fast ephemeral cell memory; extra infra if absent.  
2. **Postgres JSONB** — one less moving part; slightly higher latency.  
3. **In-process memory only** — rejected; fails F5 restart survival.

## Rationale

“No new infra during pilot” is a scheduling/ops constraint. Cell memory must survive process restart for in-flight tasks or be reconstructible; choose the lowest-ops option that meets scope enforcement.

## Consequences

- Scope tags enforced regardless of backend.  
- ADR accepted at T0 once inventory is written.  
- Switching backends later requires a short migration note, not a schema break for envelopes.
