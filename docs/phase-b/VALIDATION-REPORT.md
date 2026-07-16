# Phase B Plan — Validation Report

**Document type:** Adversarial validation of *Tronix Mesh — Phase B Inner-First Build Plan* (Draft)  
**Validated against:** v1.1 Architecture, Engineering Integration Guide v1.0, Peer Review Final v1.0, Doctrine Bundle v1.1, Whitepaper/v2.3, Flowchart v1.0  
**Date:** 2026-07-16  
**Validator:** Cursor cloud agent (Production plan validation)  
**Status:** Plan is directionally correct; **not execution-ready** as written

---

## Verdict

The Phase B mission is right: prove the handoff primitive under failure before fractal topology theater. The selected workflow, out-of-scope list, and M/F/A gate structure are sound.

The draft is **not production-grade / bulletproof**. It cannot be kicked off until schedule, architecture identity, ownership, authority model, and ops/security gaps below are resolved. An updated plan is in [`PHASE-B-BUILD-PLAN-v1.1.md`](./PHASE-B-BUILD-PLAN-v1.1.md).

---

## What Holds (Keep)

| Item | Why it survives |
|------|-----------------|
| Inner-first / handoff-first mission | Matches v1.1 §6 and peer-review reduction-to-practice pressure |
| Competitive intel 3-agent chain + one sensitivity boundary | Real business value, one representative boundary, repeatable |
| Hard out-of-scope (cross-tenant, Decision Tokens, personas, streaming) | Protects a credible ship |
| M / F / A primary gates; P secondary within 2× | Correct priority ordering |
| Fail-closed + provenance-survives-failure principles | Aligns with doctrine and v1.1 §8.5 |
| Eval set as first-class artifact | Without labels, criteria are subjective |
| Owners-unassigned as kickoff blocker | Correct; still open |

---

## Critical Defects (Must Fix Before Kickoff)

### C1 — Schedule is stale
Draft targets **May 30, 2026 soft launch**. Validation date is **2026-07-16**. Soft-launch date and day-numbered dependency graph must be rebaselined. Treating the original calendar as live is false precision.

### C2 — Two incompatible substrate stories
Documents in the corpus describe **different systems** under one brand:

| Axis | v1.1 + Phase B draft | v2.3 / Eng Guide / Peer Review / Doctrine |
|------|----------------------|-------------------------------------------|
| Address | `L2R.Buildtronix.Engineering.research.public…` | `v1:e1:apex:confidential:mem:…` 8-tuple |
| Core unit | Context Envelope + handoff | Traversal + ProofPackage + GovernanceEpoch |
| Orchestration | LangGraph agent chain | MeshResolver 13-step pipeline |
| Phase naming | Phase B = primitive validation | Phase 1B = crypto signer authenticity |
| Repo evidence | Marketing Next.js site in `tronixmesh` | Python package described; not present in this checkout |

**Production requirement:** Phase B must name a **canonical substrate** and a **mapping layer** (or explicitly freeze v1.1-only for the pilot). Building both in parallel without a bridge is dual-implementation debt and will invalidate eval labels.

### C3 — Component owners still TBD
Every row in §3.1 is `[OWNER: TBD]`. Draft correctly calls this Critical. Kickoff remains blocked.

### C4 — Authority model for public→confidential is underspecified
Draft defers Decision Tokens to Phase C, but the selected boundary is **sensitivity-increasing** and architecture requires authority checks at boundaries. Without a Phase B **minimal authority grant** (static signed grant, HMAC channel permit, or frozen bootstrap grant), F7 and the boundary story are theater.

### C5 — Latency targets contradict classifier design
P1 demands classification p50 &lt; 100ms / p95 &lt; 300ms while Stage 3 is a **Haiku LLM call**. That will miss by 1–2 orders of magnitude. Either:

- Stage 1–2 are rule-based hot path (p50/p95 apply only there), and LLM escalate is a separate metric, or  
- P1 targets are rewritten for LLM classification.

Leaving both as written makes the gate unmeetable by design.

### C6 — “No new infra” contradicts stack
Draft says run on existing Vultr and avoid new infra, then proposes Redis, Postgres hash chain, HashiCorp Vault / AWS KMS, Honeycomb. For production-grade: inventory what exists today, what is greenfield, and what is explicitly deferred (e.g. Vault → sealed env file with rotation runbook for pilot only).

---

## High Gaps (Production Hardening Required)

### H1 — Delivery semantics
F5/F6 require no duplicate side effects but omit:

- Idempotency keys per step  
- Exactly-once vs at-least-once policy  
- Side-effect ledger (external writes, tool calls)  
- Dedup window and poison-message quarantine  

### H2 — Security / threat model absent
For a confidential-boundary pilot, minimum required:

- Threat model (STRIDE or equivalent) scoped to Phase B  
- Prompt-injection / data-exfil across public→confidential handoff  
- Secret handling for model API keys  
- Signing key lifecycle (even bootstrap)  
- Soft-launch data handling: internal capability data must not leak to unauthorized soft-launch users  

### H3 — Observability is named, not operationalized
Need: trace IDs across handoffs, red/black dashboards for F1–F8, alert routes, retention, PII scrubbing in logs.

### H4 — Soft launch without runbooks
Need: operator runbook, incident severities, rollback (feature flag / kill switch), freeze procedure when provenance integrity fails, who is on-call for 2-week soft launch.

### H5 — Eval set incomplete as a contract
Need gold labels for: coordinate sequence, boundary events, required envelope fields, pass/fail rubric for “correct output,” ambiguity expected behavior, injected failure expected behavior. Chris personal review must be a dated sign-off artifact.

### H6 — Integration / CI missing
No definition of: unit vs contract vs chaos suites, CI gate for soft launch, schema migration policy, backup/restore drill for Postgres provenance.

### H7 — Cost model mismatch
v1.1 estimates ~$920–2,140/mo; draft suggests $5–10k for 20-day compute. Reconcile or explain (contractor vs compute vs one-time).

### H8 — Repo / packaging unclear
This repository is currently a Next.js marketing site. Phase B code location, language, package boundary, and deploy path are unspecified.

---

## Medium Gaps

| ID | Gap |
|----|-----|
| M1 | Classifier confidence threshold numeric value undefined |
| M2 | `max_retries`, backoff, jitter, timeout budgets undefined |
| M3 | Envelope schema versioning / forward compatibility undefined |
| M4 | Channel rule grammar artifact location undefined |
| M5 | Soft launch audience identity / access control undefined |
| M6 | Naming collision: Phase B (pilot) vs Phase 1B (crypto doctrine) — must disambiguate in all docs |
| M7 | Peer-review “PostgreSQL store pending” vs Phase B provenance Postgres — same store or parallel? |
| M8 | Operator dashboard deferred but F3/F7 require “surfaced to operator” — need minimal operator surface (CLI OK) |

---

## Alignment Checks

| Source claim | Phase B draft | Result |
|--------------|---------------|--------|
| v1.1 Phase B hypotheses H-ROUTE-1, H-MEM-2 | Covered | Pass |
| v1.1 §8.2 handoff failures | F1–F8 cover + extend | Pass |
| Doctrine fail-closed | Stated | Pass (needs enforcement tests) |
| Doctrine Phase 1B crypto authenticity | Explicitly deferred | Acceptable only if labeled **not** crypto-certified |
| Eng Guide MeshResolver as core | Not referenced | Fail / reconcile |
| Patent / IP reduction-to-practice | Competitive intel is good RTP | Pass if provenance + boundary evidence captured |

---

## Recommended Disposition

1. Accept mission, workflow, and M/F/A gate structure.  
2. Adopt updated plan v1.1 (production).  
3. Answer **blocking questions** in the updated plan §0 before any build day is counted.  
4. Do not market or soft-launch as “constitutional / cryptographically certified” until doctrine Phase 1B crypto items are in scope (later phase).

---

*End of validation report.*
