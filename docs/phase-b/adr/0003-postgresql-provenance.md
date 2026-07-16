# ADR-0003: PostgreSQL for provenance and task state

- Status: Accepted
- Date: 2026-07-16
- Deciders: Chris (Gate 0)

## Decision

Use **PostgreSQL** for the append-only hash-chained provenance ledger and durable task/workflow state in Phase B.

## Alternatives considered

1. **SQLite** — fine for laptop demos; weak for pilot ops/backup story.  
2. **Object storage only (S3 Object Lock)** — strong immutability; higher latency and ops novelty for inner-grid pilot.  
3. **PostgreSQL (chosen)** — transactional guarantees, existing skill set, restore drill feasible on Vultr.

## Rationale

Provenance integrity and resume-after-restart are Phase B primary gates. Postgres provides ACID commits for task leases/idempotency and a practical path for A5 backup/restore. App DB role must lack UPDATE/DELETE on the ledger table.

## Consequences

- Ledger is append-only by policy and grants.  
- Same instance may host task state in a separate schema.  
- Tier-2 Object Lock archival can be Phase C/D without changing the logical event model.
