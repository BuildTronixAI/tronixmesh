# Phase B Slice — Doctrine → Pilot Mapping

**Purpose:** Preserve the Design Doctrine while keeping Phase B scope locked.  
**Rule:** Schema may be forward-compatible; behavior outside the slice stays deferred or feature-flagged.  
**Doctrine:** [`TRONIXMESH-DESIGN-DOCTRINE.md`](./TRONIXMESH-DESIGN-DOCTRINE.md)  
**Plan:** [`../phase-b/PHASE-B-BUILD-PLAN-v1.1.md`](../phase-b/PHASE-B-BUILD-PLAN-v1.1.md)

---

## Philosophy (in force for Phase B)

| Doctrine | Phase B expression |
|----------|-------------------|
| Agents reason; runtime governs | Handoff / channel / authority checked **outside** the LLM |
| LLM is untrusted compute | Models are workers only; no self-elevation |
| Fail closed | Default-deny channels; UNROUTABLE; invalid signature → reject when verify flag on |
| Human sovereignty | Soft-launch manual review; Decision Tokens / human gates in Phase C+ |
| Separation of reasoning and authority | Envelope + provenance + minimal authority ≠ model output |
| Immutable audit | Hash-chained provenance ledger |

---

## In Phase B (Authorized for Build)

| Component | Status in `python/tronixmesh/` |
|-----------|--------------------------------|
| Runtime owns handoff state | Handoff service + task_id / envelope |
| Coordinate identity | `coordinate.py` |
| Capability / channel boundary (sensitivity) | `channel.py` + bootstrap grants |
| Proof-native envelope + signatures | `envelope.py` / `signing.py` (ADR-0004) |
| Append-only audit / hash chain | `provenance.py` (SQLite; WAL direction) |
| Fail-closed routing | UNROUTABLE / CHANNEL_DENIED |
| Feature-flagged verify | `flags.py` |
| Governance **state types** (schema-forward) | `governance.py` (states defined; full engine later) |

**Pilot workflow:** competitive intel 3-agent chain · one public→confidential boundary · Buildtronix Engineering only.

---

## Deferred (explicit — do not pull into Phase B)

| Doctrine component | Deferred to |
|--------------------|-------------|
| Decision Tokens (full crypto authorization objects) | Phase C |
| Human approval gates / Chairman-in-loop tokens | Phase C |
| Full governance engine (all states + CPR/SEALED flows) | Phase C+ |
| BOB / Robert / Council persona agents | Phase C+ |
| Policy engine as separate hot-path service | C / D |
| Per-operation JWTs | Later |
| RFC 3161 timestamping | Planned |
| Cross-tenant / multi-domain | C+ |
| MeshResolver 13-step as hot path | Feature-flag / later |
| Doctrine-1B SERIALIZABLE quorum crypto authenticity | Doctrine-1B track |

---

## Trust stack (Phase B reduction)

```
Human (Gate 0 / soft authority / soft-launch review)
 ↓
Runtime (channel + minimal authority + envelope)
 ↓
Evidence (provenance hash chain + content_hash)
 ↓
Agent workers (LLM recommendations only)
 ↓
LLM
```

Decision Tokens sit above the runtime in the full stack; Phase B uses **bootstrap grants** as the minimal stand-in at sensitivity↑ boundaries.

---

## Non-regression rule

Any PR that merges reasoning authority into the model (e.g. “model said approve → execute”) is **out of doctrine** and must be rejected, even if it makes the pilot demo faster.

---

*End of Phase B Slice.*
