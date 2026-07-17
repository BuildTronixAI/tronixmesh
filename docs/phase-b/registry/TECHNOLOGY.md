# Phase B Technology Registry

Status: **approved** (use in Phase B) · **experimental** (allowed behind flag / eval only) · **rejected** (do not introduce in Phase B window)

| Technology | Status | Notes |
|------------|--------|-------|
| Python 3.11+ | Approved | Runtime language |
| LangGraph | Approved | Agent chain only · ADR-0002 |
| PostgreSQL | Approved | Provenance + task state · ADR-0003 |
| Envelope signature block (agnostic layout) | Approved | Frozen fields · ADR-0004 |
| Ed25519 | Approved | Intended first `algorithm_id` · ADR-0004 |
| HMAC-SHA256 | Experimental | Same opaque layout only; no schema fork · ADR-0004 |
| Redis | Experimental | Only if already on Vultr · ADR-0005 |
| Postgres JSONB cell memory | Approved | Default if Redis absent |
| OpenTelemetry | Approved | Traces/metrics |
| Honeycomb (or existing sink) | Experimental | Use existing sink first |
| HashiCorp Vault / cloud KMS | Experimental | Prefer existing; else sealed env + runbook |
| Direct Anthropic API | Approved | Sonnet/Opus/Haiku workers + escalate |
| Direct Google Gemini API | Approved | Research worker |
| OpenRouter | Rejected | Deferred C/D |
| Multi-region HA | Rejected | Deferred D |
| Decision Tokens | Rejected | Deferred C |
| Full MeshResolver hot path | Experimental | Schema-ready; behavior flagged off by default |
| Doctrine-1B crypto authenticity | Rejected | Separate schedule |
| Operator full web dashboard | Rejected | CLI in B; UI in C |
| SBOM / formal supply-chain program | Rejected | Useful later; not Phase B Gate 0 |
| Architecture board / multi-owner RACI | Rejected | Founder-scale ownership instead |

Update this table when Gate 0 or an ADR changes a choice.
