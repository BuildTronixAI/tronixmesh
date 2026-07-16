# ADR-0002: LangGraph for agent orchestration

- Status: Accepted
- Date: 2026-07-16
- Deciders: Chris (Gate 0)

## Decision

Use **LangGraph** for the three-agent competitive-intel chain (research → structure → review) in Phase B.

## Alternatives considered

1. **Custom state machine** — full control; more build time; reinvent checkpointing.  
2. **Temporal / Restate** — strong workflow semantics; infra and learning cost exceed pilot.  
3. **LangGraph (chosen)** — already in use / compatible with Robert–BOB direction; adequate for single-tenant chain.

## Rationale

Phase B validates the handoff primitive and channel/provenance enforcement, not a new workflow engine. LangGraph is the agent chain layer only — **not** a substitute for channel rules, envelopes, or provenance.

## Consequences

- Enforcement remains outside LangGraph (routing, channel engine, envelope library).  
- Checkpoint/resume must align with Postgres task state + idempotency keys.  
- If LangGraph checkpointing conflicts with Mesh semantics, Mesh state store wins (document in follow-up ADR if needed).
