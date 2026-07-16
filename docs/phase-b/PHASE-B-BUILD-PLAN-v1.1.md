# Tronix Mesh — Phase B Inner-First Build Plan (Production)

**Document type:** Pilot execution plan (production-hardened)  
**Phase:** B — Primitive Validation (**not** Doctrine “Phase 1B” crypto authenticity)  
**Tenant:** Buildtronix (single) · **Domain:** Engineering (single)  
**Baseline architecture:** v1.1 Fractal Grid + **proof-native schema** (verification phased)  
**Supersedes:** Phase B Inner-First Build Plan (Draft, May 2026 soft-launch target)  
**Status:** Draft for Chris Gate 0 sign-off  
**Owners (default):** Architecture/Ops — Chris · Runtime — Robert · Security review — peer/council before release  
**Updated:** 2026-07-16 (v1.3 refinements)  
**Companions:** [`VALIDATION-REPORT.md`](./VALIDATION-REPORT.md) · [`DOCTRINE-TRACEABILITY.md`](./DOCTRINE-TRACEABILITY.md) · [`adr/`](./adr/) · [`registry/`](./registry/)

---

## Gate 0 — Streamlined Sign-Off

Kickoff is blocked until these decisions are written and approved. Founder-scale: high signal, no invented committees.

| # | Gate | Decision required | Owner | Status |
|---|------|-------------------|-------|--------|
| G0.1 | **Architecture** | Core schemas and interfaces frozen (§1.2 proof-native envelope; address + handoff APIs) | Chris | _Open_ |
| G0.2 | **Security** | Authn/authz, secrets, fail-closed behavior defined for Phase B scope | Chris (+ peer review before release) | _Open_ |
| G0.3 | **Operations** | Rollback, monitoring, backups documented for pilot environment | Chris | _Open_ |
| G0.4 | **Ownership** | Single accountable owner per major subsystem (§3.1) | Chris | _Open_ |
| G0.5 | **Capacity** | **Who builds this, and what stops while they do?** (§11) | Chris | _Open_ |
| G0.6 | **IP** | Disclosure boundary approved with counsel as needed (§10) | Chris | _Open_ |
| G0.7 | **Budget** | Infra + model spend limits approved | Chris | _Open_ |
| G0.8 | **Execution** | Milestones, acceptance criteria, staged rollout defined (§3.4, §4, §9) | Chris | _Open_ |
| G0.9 | **ADRs** | Irreversible architecture decisions recorded (§1.3, [`adr/`](./adr/)) | Chris | _Open_ |

**Retained from original review (keep):** FP/FN classifier objectives · tech registry (approved/rejected/experimental) · staged rollout · Gate 0 as decision point.

**Remaining tactical questions** (latency split, retries, HMAC vs Ed25519 Day 1, CLI vs web ops, etc.) are answered by **T3**, not Gate 0 — see §13. Signature algorithm choice must land in an ADR by T3 even if Gate 0.9 covers the rest.

Once Gate 0 is signed, Phase B is locked. Scope adds go to the Phase C queue.

---

## 1. Mission Statement

Prove the **handoff primitive** end-to-end across **one** sensitivity boundary crossing in **one** tenant/domain, under realistic failure conditions, using a workflow with business value beyond the pilot.

If this primitive cannot survive retries, ambiguity, escalation, provenance reconstruction, state persistence, interruption/recovery, **idempotent recovery**, and **fail-closed channel enforcement** — fractal topology discussion is premature.

Phase B’s only job is to find that out with measurable evidence.

This is not a demo. It is the smallest credible reduction-to-practice of the v1.1 architecture, with schemas that preserve forward compatibility for proof and governance capabilities that patentable differentiation may depend on.

### 1.1 Non-Goals / Naming Hygiene

- **Not** Doctrine Bundle “Phase 1B” (Ed25519 signer authenticity, SERIALIZABLE quorum). Call that **Doctrine-1B**.  
- **Not** a claim of constitutional cryptographic certification. Soft-launch copy: **pilot / non-certified**.  
- **Not** multi-tenant, Decision Tokens, personas, streaming, or OpenRouter.  
- **Not** “implement every proof-generation and verification path in v1.” Design for them; enable later.

### 1.2 Proof-Native Schema, Feature-Flagged Behavior

The dependency is **not** “envelope first, proof later.” It is:

```
Proof model
    → Envelope schema
        → Storage
            → Interfaces
                → Behavior (feature-flagged)
```

If the envelope eventually contains signature blocks, hash-chain references, governance metadata, proof identifiers, and witness coordinates, those fields influence the schema from day one. Retrofitting them later forces API, persistence, and compatibility migrations.

| Layer | Rule |
|-------|------|
| **Schema** | Proof-native — fields present, versioned, and persisted |
| **Behavior** | Feature-flagged — verification / MeshResolver / distributed enforcement can be off, stubbed, or partial |

| Design now (schema / interfaces) | Enable later (flagged behavior) |
|----------------------------------|---------------------------------|
| Envelope schema with proof fields | Full ProofPackage verification paths |
| Proof / governance / witness reference slots | MeshResolver as hot-path enforcer |
| Signature blocks (structure + verify hook) | Distributed enforcement |
| Schema versioning + compatibility policy | Cross-node consensus |

**Phase B implements:** populate and persist proof-relevant fields; hash-chain provenance; signature verify where keys exist; fail-closed channel rules.  
**Phase B may feature-flag off:** full MeshResolver 13-step pipeline, Doctrine-1B crypto authenticity, distributed verification.

**Narrow claim:** If patentable differentiation depends on proof and governance, preserve those capabilities in schema/interfaces from the outset — without shipping every verification path in Phase B.

Default: **proof-native v1.1 envelopes**; MeshResolver/ProofPackage attach later **without schema break**.

### 1.3 Architecture Decision Records (Gate 0.9)

For each irreversible decision, capture: Decision · Alternatives · Rationale · Consequences · Date.  
Template and initial ADRs live in [`adr/`](./adr/). A handful of ADRs replaces a formal architecture board.

Minimum ADRs before or at Gate 0 close:

| ADR | Topic |
|-----|-------|
| ADR-0001 | Proof-native envelopes (schema vs behavior) |
| ADR-0002 | LangGraph for agent orchestration |
| ADR-0003 | PostgreSQL for provenance + task state |
| ADR-0004 | Ed25519 vs HMAC for envelope signatures *(may finalize by T3)* |
| ADR-0005 | Redis vs Postgres for cell memory *(after Vultr inventory)* |

---

## 2. Pilot Workflow

### 2.1 Selected Workflow

Engineering competitive intel pipeline. Three-agent chain with one sensitivity-increasing boundary.

| Step | Agent coordinate | Task |
|------|------------------|------|
| 1 | `L2R.Buildtronix.Engineering.research.public.balanced.text.long` | Research target competitor public technical posture |
| 2 | `L2R.Buildtronix.Engineering.structure.confidential.frontier.text.medium` | Combine with internal capability data; comparative analysis |
| 3 | `L2R.Buildtronix.Engineering.review.confidential.frontier.text.long` | Review for accuracy, gaps, actionable insights |

**Boundary:** Step 1 → 2 is `public → confidential`. Exercises channel tag-add and Phase B minimal authority (bootstrap grant / static channel permit — Decision Tokens remain Phase C).

### 2.2 Why This Workflow

Business value, real boundary, bounded scope, repeatable volume, aligns with Design^BOB / Competitive Intel.

### 2.3 Out of Scope (Locked)

| Excluded | Deferred to |
|----------|-------------|
| Cross-tenant (AMS, OeniVault, …) | C+ |
| Multi-domain | C+ |
| Decision Token issuance | C |
| Human approval gates (except soft-launch manual output review) | C |
| Persona agents | C+ |
| Multi-modal / streaming | D+ / Future |
| Production load / multi-region HA | D |
| Full MeshResolver hot path / Doctrine-1B crypto | Later (schema reserved now) |
| Operator full dashboard UI | C (minimal CLI required in B) |
| OpenRouter | C/D |

---

## 3. Architectural Components to Build

### 3.1 Build Inventory — Scale-Appropriate Ownership

Accountability without inventing a 50-person org chart. Default single owners:

| Area | Accountable owner |
|------|-------------------|
| Architecture (schemas, interfaces, freeze) | **Chris** |
| Runtime implementation | **Robert** |
| Operations (deploy, backups, kill switch, on-call) | **Chris** |
| Security review before release | **Peer review / council** (not a standing board) |

Subsystem map (one name each; same person may own multiple):

| Subsystem | Purpose | Phase B acceptance | Owner |
|-----------|---------|--------------------|-------|
| Coordinate registry | Lookup + health | Versioned schema; empty-coordinate escalate | Robert |
| Intake classifier | Assign coordinates | 3-stage; FP/FN objectives (§4.1a); confidence + escalate | Robert |
| Routing + channel rules | Enforce boundaries | Fail-closed; default-deny | Robert |
| Context Envelope library | Ser/de + proof-native fields | Schema freeze; signature hook | Robert |
| Minimal authority | Sensitivity↑ without Decision Tokens | Bootstrap/static grant verify | Robert |
| Provenance store | Append-only hash chain | Integrity job; restore drill | Robert |
| Task/state + cell memory | Resume + scoped ephemeral state | Idempotency keys; scope deny | Robert |
| Agent runtimes (×3) | Research / structure / review | Direct APIs; structured I/O | Robert |
| Validation harness | Eval + failure injection | M/F/A automatable | Robert |
| Telemetry + operator CLI | Traces, quarantine, retry/kill | Correlation IDs; CLI demo | Chris (ops) / Robert (impl) |
| Kill switch | Halt admissions + freeze in-flight | Documented; tested | Chris |

Gate 0.4 confirms or overrides this table. Do **not** require four owners per component or a formal architecture board.

### 3.2 Tech Stack (Default)

| Layer | Choice | Notes |
|-------|--------|-------|
| Language | Python 3.11+ | Aligns with reference Mesh package |
| Orchestration | LangGraph | Agent chain only — not a substitute for channel/provenance · ADR-0002 |
| Envelope | JSON + signature block (Ed25519 preferred) | Proof-native fields; verify feature-flagged · ADR-0001/0004 |
| Provenance / task state | PostgreSQL | Append-only ledger · ADR-0003 |
| Cell memory | Redis **or** Postgres JSONB | Match Vultr inventory · ADR-0005 |
| Classifier | Rules (hot path) + Haiku escalate | FP/FN objectives; separate latency metrics |
| Telemetry | OpenTelemetry → existing sink | `task_id`, `handoff_id`, `envelope_hash` |
| Deploy | Existing Vultr | Capacity check at T0 |
| Secrets | Existing KMS/Vault or sealed env + rotation runbook | Document any downgrade |
| Model APIs | Direct Gemini / Anthropic | No OpenRouter |

Technology status is tracked in [`registry/TECHNOLOGY.md`](./registry/TECHNOLOGY.md) (**approved / rejected / experimental**).  
Interface stub for later MeshResolver attach: thin adapter behind envelope/channel API — **no dual implementation** in Phase B.

### 3.3 Delivery Semantics

| Concern | Rule |
|---------|------|
| Delivery | At-least-once handoffs |
| Step effects | Idempotency key = `hash(task_id, step, attempt_bucket)` |
| Side effects | Idempotent workers or side-effect ledger before external call |
| Poison | After `max_retries` → quarantine; never silent drop |
| Clock | Trusted NTP; reject envelope skew &gt; 5 min |
| Concurrency | One active executor lease per `task_id` |

### 3.4 Build Dependency Graph (T0-relative)

Soft-launch proposal: **T0 + 30 calendar days**, contingent on Gate 0.

| Window | Deliverables | Parallel |
|--------|--------------|----------|
| T0 | Gate 0 signed; capacity statement; infra inventory; eval v0 | IP boundary freeze |
| T0–T3 | Envelope schema freeze (proof-native) + coordinate registry | Threat model; doctrine gap verify |
| T0–T4 | Provenance store + integrity checker | Backup/restore drill |
| T4–T8 | Routing + channel rules + minimal authority | Failure-injection hooks |
| T8–T13 | Agent runtimes + idempotent step runner | Telemetry correlation |
| T13–T16 | Memory scope + task resume | Operator CLI |
| T16–T19 | Classifier (rules + escalate) | Eval v1 gold labels |
| T19–T23 | Validation harness + chaos (F-series) | CI gates |
| T23–T27 | E2E + security floor | Runbooks |
| T27–T30 | Eval campaigns + Soft Launch Readiness Review | Phase C queue freeze |

**Slip rule:** M/F/A fail → slip launch. Full dashboard may slip; operator CLI may not. P &gt;2× → Phase D tag, not hard block. Mesh overhead P2/P3 &gt;10× → architectural defect review.

---

## 4. Pilot Validation Criteria

Ship gate: **M, F, A** primary; **S, O** as defined below (prefer mapping to existing doctrine — see traceability); **P** within 2×.

Do **not** invent duplicate gate docs where doctrine already specifies the invariant. New criteria only where the matrix shows Open/Partial.

### 4.1 Mechanical (M)

| # | Criterion | Measurement |
|---|-----------|-------------|
| M1 | Correct output ≥90% | 50-task labeled eval |
| M2 | Handoff E2E ≥99% (no injection) | Successful / total |
| M3 | ≥5 variations + ≥3 ambiguity patterns | Design review |
| M4 | Complete Context Envelope per handoff | 100% |
| M5 | Valid hash-chained provenance | 100% |
| M6 | Sensitivity↑ has valid minimal authority artifact | 100% |
| M7 | Envelope carries required proof-native fields (populated or explicitly null-versioned) | Schema contract test |

### 4.1a Classifier Objectives (FP/FN) — Retained from Original Review

Accuracy alone is insufficient. Track false positives and false negatives on the labeled eval set:

| Error | Definition (Phase B) | Target | Why it matters |
|-------|----------------------|--------|----------------|
| **FP** | Routed to confidential / higher-sensitivity coordinate when gold is public-only (or wrong function) | FP rate ≤ 2% on clean public set | Unauthorized sensitivity↑ / wrong worker |
| **FN** | Failed to escalate or assign confidential/structure when gold requires boundary crossing | FN rate ≤ 5% on boundary set | Missed governed path; silent under-routing |
| **Ambiguity handling** | Low-confidence cases that should escalate but were forced | 0 silent forced routes | F2 |

Report confusion matrix + FP/FN at every eval campaign. Tune thresholds against these objectives, not headline accuracy alone.

### 4.2 Failure Modes (F)

Recover within bounds **or** fail closed with operator surface. Never silent drop / silent wrong route.

| # | Mode | Required behavior |
|---|------|-------------------|
| F1 | Transient destination failure | ≤ `max_retries`; each attempt in provenance |
| F2 | Classification ambiguity | Escalate; log uncertainty; no silent wrong coordinate |
| F3 | Unroutable | Hard fail; quarantine; operator surface |
| F4 | Partial mid-chain failure | Resume from last commit; provenance reflects recovery |
| F5 | Process restart | Durable resume; no duplicate committed effects |
| F6 | Agent killed | Lease timeout → retry/escalate; no orphans |
| F7 | Channel violation | Reject; log; surface |
| F8 | Provenance hash mismatch | Detect; reject; alert; quarantine |
| F9 | Idempotency / replayed step | No-op or reject; record replay |
| F10 | Invalid envelope signature | Reject; do not execute |

### 4.3 Performance (P) — Secondary

| # | Criterion | Target | Applies to |
|---|-----------|--------|------------|
| P1a | Rules Stages 1–2 | p50 &lt; 100ms, p95 &lt; 300ms | Hot path |
| P1b | LLM Stage 3 escalate | p50 &lt; 2s, p95 &lt; 5s | Non-blocking if P1a holds |
| P2 | Intra-cell handoff (excl. model) | p50 &lt; 50ms, p95 &lt; 150ms | Mesh overhead |
| P3 | Sensitivity-boundary handoff (excl. model) | p50 &lt; 200ms, p95 &lt; 500ms | Mesh overhead |
| P4 | E2E 3-agent | p50 &lt; 60s, p95 &lt; 180s | Incl. model |

### 4.4 Audit (A)

| # | Criterion | Measurement |
|---|-----------|-------------|
| A1 | Event per handoff | ratio = 1.0 |
| A2 | Hash chain integrity | Periodic + on-read |
| A3 | Reconstruct from audit alone | Forensic drill |
| A4 | Tamper detectable | Injected event fails |
| A5 | Backup/restore | Chain verifies post-restore |

### 4.5 Security Floor (S) — Only Where Doctrine Gaps Require It

Prefer doctrine/runtime specs; Phase B adds pilot-scoped tests:

| # | Criterion | Notes |
|---|-----------|-------|
| S1 | Phase B threat model (short) | Or pointer into existing security doctrine |
| S2 | Boundary prompt-injection / exfil suite | ≥10 cases; zero unauthorized confidential egress |
| S3 | Secrets not in git/logs | Scan + redaction |
| S4 | Kill switch &lt; 60s | Chaos |
| S5 | Soft-launch ACL isolation | Per-user tasks |
| S6 | No Doctrine-1B certification claims in copy | Copy review |

### 4.6 Operability (O)

| # | Criterion | Measurement |
|---|-----------|-------------|
| O1 | Operator CLI (list / provenance / quarantine / retry-kill) | SLRR demo |
| O2 | Runbooks for F1–F10 + kill switch + provenance break | Written + tabletop |
| O3 | On-call for soft-launch window | Chris primary (default); backup named |
| O4 | CI: unit + contract + chaos subset | Green on main |
| O5 | Correlation IDs on 100% handoff spans | Trace sample |

### 4.7 Soft Launch Gate

Ship if M/F/A/S/O met, P within 2× (or Phase D tag), Gate 0 still valid, Chris SLRR sign-off.

---

## 5. Eval Set Design (Contract)

### 5.1 Composition (50)

| Category | Count |
|----------|-------|
| Clean research-public | 15 |
| Clean confidential / boundary | 10 |
| Ambiguous research vs structure | 5 |
| Ambiguous sensitivity | 5 |
| Full 3-agent | 10 |
| Injected failure | 5 |

### 5.2 Per-Task Fields

`task_id`, input, gold coordinate **sequence**, expected boundary events, expected authority outcome, output rubric, ambiguity behavior, injection + expected recovery, fixture sensitivity.

Automated eval uses **synthetic confidential fixtures**. Real internal data only under soft-launch IP/data policy (Gate 0.6).

### 5.3 Sign-Off

Chris reviews eval v1 before T19. Artifact: `docs/phase-b/eval/SIGN_OFF.md` (date + commit SHA). Runtime owner (Robert) maintains the set.

---

## 6. Security & Threat Model (Phase B Scope)

| Threat | Mitigation |
|--------|------------|
| Prompt injection → confidential egress | Channel enforce + output allowlist + S2 |
| Envelope forgery / replay | Signature blocks + idempotency + F9/F10 |
| Provenance tampering | Hash chain + A4/A5 |
| API key theft | Secrets path + rotation runbook |
| Soft-launch lateral read | Per-user ACL |
| Operator error | Kill switch; quarantine over delete |

Out of scope for B: formal pentest, SOC2, cross-tenant adversarial suite, hardware key ceremony (Doctrine-1B).

Peer/council security review is a **release gate**, not a standing architecture board.

---

## 7. Risk Register

| Risk | L | I | Mitigation |
|------|---|---|------------|
| 30-day window aggressive | H | M | Scope cuts; parallel chaos; CLI not UI |
| Eval set late | M | H | Chris drafts v0 at T0 |
| Classifier &lt;95% | M | M | Escalate model on ambiguity; tune in D |
| Schema without proof fields | H | H | §1.2 proof-native freeze at T3 |
| Capacity conflict with other products | H | H | Gate 0.5 displacement statement |
| IP leak via public repo / plan | M | C | Gate 0.6; private eng repo for RTP code |
| Scope creep | H | H | Locked Gate 0; Phase C queue |
| Infra assumptions wrong | M | H | T0 inventory |
| Failure injection finds gap | M | H | Slip; revise — intended |
| Overclaim certification | M | H | S6 |

---

## 8. Phase B → Phase C / Doctrine-1B Handoff

Exit package: failure catalog · latency baselines · classifier confusion matrix · invalidated architecture decisions · v1.2 delta · gap list for MeshResolver attach · soft-launch ops report · schema compatibility notes for proof enablement.

Phase C (Decision Tokens, approval gates) only after B exit. Doctrine-1B scheduled with explicit capacity — do not silently fold into C.

---

## 9. Staged Rollout & Soft Launch (Gate 0.8)

Retained staged model (original review). Do not jump stages.

| Stage | Audience | Exit to next |
|-------|----------|--------------|
| **R1 Synthetic** | Eval harness + injected failures only | M/F/A green on synthetic set |
| **R2 Internal** | Chris (+ Robert as operator) | 3 consecutive days, no unrecoverable failure |
| **R3 Trusted users** | 2–3 named Buildtronix users | 14 days; ACL + S5 pass; manual review before business action |
| **R4 Production** | Broader / customer-facing | **Out of Phase B** — Phase D+ |

| Dimension (R3) | Proposal |
|----------------|----------|
| Access | Allowlisted; per-task ACL |
| Volume | 10–20 real tasks/day + continuous synthetic eval |
| Mode | `pilot=true`; manual review before business action |
| Success | No unrecoverable failure; no security incident; alerts explained |
| Copy | “Internal pilot — not certified constitutional governance” |
| On-call | Chris primary; backup named at Gate 0 |

---

## 10. IP Posture (Gate 0.6)

Not merely document classification. Treat implementation visibility as an **IP decision**. Distinguish two concerns — and **do not make categorical legal claims** without attorney input:

| Concern | Practical note |
|---------|----------------|
| **Patent rights** | Public disclosure before or around filing dates can affect strategy; U.S. and international rules differ. Coordinate timing/content with patent counsel (Provisional 64/072,487 → non-provisional path). |
| **Trade secrets** | Publicly releasing implementation details generally eliminates trade-secret protection for those details. |

**Operational default (prudent, not a legal opinion):** Keep implementation-specific material private until counsel approves disclosure.

Before Gate 0 closes, Chris approves (with counsel as needed):

| Question | Decision |
|----------|----------|
| What may be disclosed publicly before counsel sign-off on non-provisional strategy? | _TBD_ |
| What remains private regardless of patent status (trade-secret candidates)? | _TBD_ |
| Which code, docs, eval fixtures, examples stay in **private** repos? | _TBD_ |
| May this planning pack remain in the public `tronixmesh` marketing repo? | _TBD_ |
| Which Phase B RTP artifacts need counsel review before any publish? | _TBD_ |

**Default until overridden:** Runtime RTP code, claim-sensitive schema detail, internal capability fixtures, failure-injection harness → **private eng repository**. Public site stays at marketing altitude. Relocate planning docs if Gate 0.6 requires private.

---

## 11. Capacity Planning (Gate 0.5) — Scheduling Constraint

Primary question is **not** “who owns this on an org chart?”  
It is: **Who builds this, and what stops while they do?**

This is a **scheduling** constraint for a founder-led portfolio, not an enterprise staffing exercise.

**Displacement statement (required at Gate 0):**

| Initiative | Status during Phase B window | Explicit choice |
|------------|------------------------------|-----------------|
| Robert / TronixMesh runtime (this plan) | _Primary / paused / shared %_ | _TBD_ |
| Pre-Con | _Continue / freeze / reduce_ | _TBD_ |
| Clover | _Continue / freeze / reduce_ | _TBD_ |
| AMS | _Continue / freeze / reduce_ | _TBD_ |
| FedTronix | _Continue / freeze / reduce_ | _TBD_ |
| Carl’s Wine Vault | _Continue / freeze / reduce_ | _TBD_ |
| Marketing site / other | _Continue / freeze / reduce_ | _TBD_ |

Also state:

1. **Who builds** (default: Robert runtime, Chris architecture/ops).  
2. **What stops** (or slows) for that window — name the displaced work explicitly.  
3. **Hours/week available** in T0–T30.  
4. **Ordered cut list** if capacity is insufficient (dashboard already cut; next…).  
5. **What slips** if TronixMesh is not the primary bet for that window.

No kickoff without this table filled.

---

## 12. CI, Environments, Budget

| Item | Requirement |
|------|-------------|
| Environments | `dev` · `pilot` (Vultr) — no “prod” alias |
| CI | lint · unit · envelope/provenance contract · chaos subset |
| Migrations | Expand/contract; never rewrite ledger rows |
| Rollback | Kill switch + prior image pin; ledger append-only |
| Retention | Pilot policy at T0 (suggest 90 days) |
| Budget | Model+infra align ~$1–2k/mo band unless justified; hard stop at Gate 0.7; T15 spend review |

---

## 13. Open Questions (Post–Gate 0 / by T3)

Gate 0 replaces the old Q1–Q10 blocking wall. These remain for early execution:

1. Soft-launch absolute date vs T0+30?  
2. Minimal authority artifact form (bootstrap signed grant vs static channel permit table)?  
3. Confirm P1a/P1b latency split?  
4. Vultr inventory (Postgres/Redis/Vault/OTel today)?  
5. Soft-launch audience names + real vs synthetic confidential data?  
6. Classifier confidence threshold?  
7. `max_retries` / timeout / lease budgets?  
8. HMAC acceptable Day 1 or Ed25519 mandatory?  
9. Operator surface: CLI-only or minimal web page?  
10. Relationship to Design^BOB / Competitive Intel — wrap, rewrite, or strangler?  
11. Address canonicalization: keep v1.1 dotted form only, or dual-encode v2.3 8-tuple as alias in schema now?  

---

## Document Control

| Version | Date | Notes |
|---------|------|-------|
| Draft | ~May 2026 | Original Phase B plan (May 30 target) |
| v1.1-PRODUCTION | 2026-07-16 | First production hardening pass |
| v1.2-PRODUCTION | 2026-07-16 | Proof-native schema; founder-scale ownership; IP; doctrine-first; capacity; Gate 0 |
| v1.3-PRODUCTION | 2026-07-16 | Proof→schema dependency; feature flags; capacity-as-scheduling; counsel-safe IP; FP/FN; tech registry; staged rollout; ADR Gate 0.9 |

*End of Phase B Inner-First Build Plan (Production v1.3).*
