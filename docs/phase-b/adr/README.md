# Architecture Decision Records (Phase B)

Gate **0.9** requires ADRs for irreversible choices. Format is intentionally light — durable context without a review board.

## Template

```markdown
# ADR-NNNN: Title

- Status: Proposed | Accepted | Superseded
- Date: YYYY-MM-DD
- Deciders: …

## Decision
## Alternatives considered
## Rationale
## Consequences
```

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](./0001-proof-native-envelopes.md) | Proof-native envelopes | Accepted |
| [0002](./0002-langgraph-orchestration.md) | LangGraph for agent orchestration | Accepted |
| [0003](./0003-postgresql-provenance.md) | PostgreSQL for provenance + task state | Accepted |
| [0004](./0004-envelope-signatures.md) | Ed25519 vs HMAC signatures | Proposed |
| [0005](./0005-cell-memory-store.md) | Redis vs Postgres cell memory | Proposed |
