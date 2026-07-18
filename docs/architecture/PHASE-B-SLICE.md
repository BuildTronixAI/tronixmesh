# Phase B Slice — Architecture v2.0 → Pilot Mapping

**Purpose:** Preserve Architecture Write-Up v2.0 / Design Doctrine while keeping Phase B scope locked.  
**Rule:** Schema may be forward-compatible; behavior outside the slice stays deferred or feature-flagged.  
**Sources:** [`TRONIXMESH-ARCHITECTURE-v2.md`](./TRONIXMESH-ARCHITECTURE-v2.md) · [`TRONIXMESH-DESIGN-DOCTRINE.md`](./TRONIXMESH-DESIGN-DOCTRINE.md)  
**Plan:** [`../phase-b/PHASE-B-BUILD-PLAN-v1.1.md`](../phase-b/PHASE-B-BUILD-PLAN-v1.1.md)

---

## Philosophy (in force for Phase B)

| Doctrine / claim | Phase B expression |
|------------------|-------------------|
| Agents reason; runtime governs | Handoff / channel / authority checked **outside** the LLM |
| LLM is untrusted compute | Models are workers only; no self-elevation |
| **Coordinate-native governance** | v1.1 dotted coordinates on every agent/envelope; scope from address |
| Embedded enforcement proof (schema) | Proof-native envelope fields + provenance lineage (ADR-0001/0004) |
| Four topologies | Authority (bootstrap grants) · Routing (handoff) · Memory (task/provenance store) · Isolation (channel default-deny) |
| Fail closed | Default-deny channels; UNROUTABLE; invalid signature → reject when verify on |
| Human sovereignty (Tier 0) | Gate 0 / stop authority / soft-launch review; full Decision Tokens in C |
| Separation of reasoning and authority | Envelope + provenance + minimal authority ≠ model output |
| Immutable audit | Hash-chained provenance (SQLite now; RR-0056 Postgres target later) |

---

## In Phase B (Authorized for Build)

| Architecture v2 component | Phase B status |
|---------------------------|----------------|
| Coordinate addressing | `coordinate.py` — v1.1 8-segment |
| Runtime handoff enforcement | `handoff.py` |
| Channel / isolation boundary | `channel.py` |
| Minimal authority (Decision Token stand-in) | `authority.py` bootstrap grants |
| Proof-native envelope + signatures | `envelope.py` / `signing.py` |
| Append-only audit / hash chain | `provenance.py` (SQLite; RR-0056 direction) |
| Cell memory (TTL + scope tags) | `memory.py` — Postgres JSONB logical · ADR-0005; SQLite stand-in |
| Rules router + escalate-on-ambiguity | `router.py` |
| Idempotent step runner + fault injection | `runner.py` / `faults.py` |
| Eval set v0 (synthetic) | `python/evals/v0/` |
| Governance state vocabulary | `governance.py` (fail-closed transitions; full engine later) |
| Feature-flagged verify | `flags.py` |
| Competitive intel 3-agent pilot | LangGraph chain `agents/chain.py` — Mesh runner governs handoffs |
| Pluggable workers | `agents/providers.py` — stub default; Anthropic/Gemini via env |
| Task store + operator CLI | `taskstore.py` / `cli.py` (`tronixmesh-ops`) |
| Telemetry correlation | `telemetry.py` — correlation_id on provenance |
| Security floor | `security.py` — cross-cell / signature / no model authority |
| Eval v1 campaign | `evals/v1/` — FP/FN reporter |
| Postgres DSN helper | `postgres.py` — ping when `TRONIX_DATABASE_URL` set |

---

## Deferred (do not pull into Phase B)

| Architecture v2 component | Deferred to |
|---------------------------|-------------|
| Decision Tokens (full crypto objects) | Phase C |
| HITL / Tier-crossing approval gates | Phase C |
| Full Governance Engine (all CPR/SEALED product flows) | Phase C+ |
| Witness / Little Voice conscience modules | C+ (schema hooks optional later) |
| Focus Heartbeat + force-testing protocols | C+ / ops |
| Doctrine 8 full degraded-state product surface | Partial now (kill switch); full later |
| RR-0056 Postgres SECURITY DEFINER audit | When infra ready (replace/augment SQLite) |
| BOB / Robert / Council persona runtimes | Phase C+ |
| Tenant-scoped multi-tenant chains | C+ |
| Per-operation JWTs / RFC 3161 | Later |
| MeshResolver 13-step hot path | Feature-flag / later |
| Doctrine-1B SERIALIZABLE quorum crypto | Doctrine-1B track |

---

## Trust stack (Phase B reduction)

```
Human (Tier 0 — Gate 0 / stop authority / soft-launch review)
 ↓
Runtime (coordinate + channel + minimal authority + envelope)
 ↓
Evidence (provenance hash chain + content_hash)
 ↓
Agent workers (LLM recommendations only)
 ↓
LLM
```

Full stack inserts Decision Tokens and Governance Engine above Runtime; Phase B uses **bootstrap grants** at sensitivity↑ as the stand-in.

---

## Non-regression rules

1. Any PR that merges reasoning authority into the model is **out of doctrine** — reject.  
2. Any PR that drops coordinates from envelopes/handoffs breaks the patented core narrative — reject.  
3. Public marketing copy derived from Architecture v2.0 needs IP/counsel review (provisional 64/072,487; Paris deadline 05/22/2027).

---

*End of Phase B Slice.*
