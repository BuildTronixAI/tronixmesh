# Vultr Inventory — Phase B T0

**Date:** 2026-07-18  
**Owner:** Christopher C. Leiser (ops)  
**Purpose:** Close ADR-0005 and ground deploy assumptions. Soft-launch still gated by staged rollout.

## Status

| Item | Present on Vultr today? | Notes |
|------|-------------------------|-------|
| PostgreSQL | **Assumed / preferred** | ADR-0003 accepted; local pilot uses SQLite-shaped stand-in until DSN is wired |
| Redis | **Not confirmed — treat as absent** | Do not stand up Redis solely for Phase B |
| Object storage / backups | Unknown | A5 restore drill when Postgres DSN exists |
| Vault / secrets manager | Unknown | Env / local keys for Phase B verify flags |
| OpenTelemetry collector | Unknown | Correlation IDs in provenance payloads first |
| Existing deploy host | Unknown | Capacity check remains Chris stop-authority |

## Decision input for ADR-0005

- Redis **not** confirmed → **do not** add Redis for pilot.  
- Cell memory backend: **Postgres JSONB** (logical); **SQLite JSON** local stand-in in `python/tronixmesh/memory.py` until Vultr DSN is supplied.  
- Scope tags + TTL required regardless of backend.

## Follow-ups (ops, non-blocking for coding)

1. Paste real Vultr Postgres host / version / backup policy when available.  
2. Confirm whether any Redis already runs on the same account (if yes, reopen ADR-0005 only if Redis is lower-ops).  
3. Name soft-launch host and on-call backup.

*Inventory may be refined without reopening Gate 0.*
