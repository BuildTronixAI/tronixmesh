# Tronix Mesh — Phase B Inner-First Build Plan (Production)

**Document type:** Pilot execution plan (production-hardened)  
**Phase:** B — Primitive Validation (**not** Doctrine “Phase 1B” crypto authenticity)  
**Tenant:** Buildtronix (single) · **Domain:** Engineering (single)  
**Baseline architecture:** v1.1 Fractal Grid (locked for this pilot)  
**Supersedes:** Phase B Inner-First Build Plan (Draft, May 2026 soft-launch target)  
**Status:** Draft for Chris sign-off — **kickoff blocked** until §0 questions answered  
**Owner:** Chris · **Updated:** 2026-07-16  
**Companion:** [`VALIDATION-REPORT.md`](./VALIDATION-REPORT.md)

---

## 0. Blocking Decisions (Answer Before Day 1 Counts)

Kickoff is **forbidden** until every item below has a written answer and owner. Partial answers do not unlock the clock.

| # | Decision | Options / Notes | Owner | Answer |
|---|----------|-----------------|-------|--------|
| Q1 | **Canonical substrate for Phase B** | **A)** v1.1 Context Envelope + channel rules only · **B)** v2.3 MeshResolver/ProofPackage as enforcement core with v1.1 addresses as alias · **C)** Explicit dual-run (not recommended) | Chris | _TBD_ |
| Q2 | **Code home** | This `tronixmesh` repo (new `packages/` or `python/`) vs separate private eng repo vs existing Bob/OpenClaw tree on Vultr | Chris | _TBD_ |
| Q3 | **Component owners** | Name one accountable owner per §3.1 row (can be same person for ≤3 rows) | Chris | _TBD_ |
| Q4 | **Soft-launch date** | Propose calendar below; confirm or override | Chris | _TBD_ |
| Q5 | **Phase B minimal authority** | How does public→confidential get authorized without Decision Tokens? (bootstrap signed grant / static channel permit / HMAC permit table) | Chris | _TBD_ |
| Q6 | **Classifier latency contract** | Hot-path rules-only SLOs vs LLM-escalate as separate non-gating metric | Chris | _TBD_ |
| Q7 | **Infra inventory** | What already exists on Vultr (Postgres, Redis, Vault, OTel)? What is greenfield? | Ops owner | _TBD_ |
| Q8 | **Soft-launch audience + data policy** | Who may see confidential comparative analysis? Manual review gate before business use? | Chris | _TBD_ |
| Q9 | **Budget cap** | Compute + tools + contractor split; hard stop amount | Chris | _TBD_ |
| Q10 | **Tech stack overrides** | Accept §3.2 or list rejects | Chris | _TBD_ |

**Assumption until answered (explicit, revisable):** Proceed with planning under **Q1=A** (v1.1-only pilot), leave a thin adapter stub so a later MeshResolver wrap is possible, and treat Phase B as **governance-semantics pilot**, not crypto-certified doctrine Phase 1B.

---

## 1. Mission Statement

Prove the **handoff primitive** end-to-end across **one** sensitivity boundary crossing in **one** tenant/domain, under realistic failure conditions, using a workflow with business value beyond the pilot.

If this primitive cannot survive retries, ambiguity, escalation, provenance reconstruction, state persistence, interruption/recovery, **idempotent recovery**, and **fail-closed channel enforcement** — fractal topology and constitutional marketing are premature.

Phase B’s only job is to find that out with **measurable, adversarial evidence**.

This is not a demo. It is the smallest credible reduction-to-practice of the v1.1 architecture, instrumented to production-pilot standards (runbooks, kill switch, eval contract, security floor).

### 1.1 Non-Goals / Naming Hygiene

- **Not** Doctrine Bundle “Phase 1B” (Ed25519 signer authenticity, SERIALIZABLE quorum). Call that **Doctrine-1B** in all future docs.  
- **Not** a claim of constitutional cryptographic certification. Soft-launch language must say **pilot / non-certified**.  
- **Not** multi-tenant, Decision Tokens, personas, streaming, or OpenRouter.

---

## 2. Pilot Workflow

### 2.1 Selected Workflow

Engineering competitive intel pipeline. Three-agent chain with one sensitivity-increasing boundary.

| Step | Agent coordinate | Task |
|------|------------------|------|
| 1 | `L2R.Buildtronix.Engineering.research.public.balanced.text.long` | Research target competitor public technical posture (docs, blog, GitHub, jobs) |
| 2 | `L2R.Buildtronix.Engineering.structure.confidential.frontier.text.medium` | Combine research with internal Buildtronix capability data; comparative analysis |
| 3 | `L2R.Buildtronix.Engineering.review.confidential.frontier.text.long` | Review for accuracy, gaps, actionable insights |

**Boundary crossing:** Step 1 → Step 2 crosses `public → confidential` (sensitivity-increasing). Exercises channel-rule tag-add behavior and **Phase B minimal authority** (Q5).

### 2.2 Why This Workflow

- **Business value:** Real competitive intel for product/positioning.  
- **Real boundary:** Most common production pattern.  
- **Bounded:** Three agents, one cell, one boundary.  
- **Repeatable:** Many competitors → telemetry volume.  
- **Aligned:** Feeds Design^BOB / Competitive Intel stream.

### 2.3 Out of Scope (Locked)

| Excluded | Deferred to |
|----------|-------------|
| Cross-tenant traffic (AMS, OeniVault) | C+ |
| Multi-domain workflows | C+ |
| Decision Token issuance | C |
| Human approval gates (except soft-launch manual review of outputs) | C |
| Persona agents (BOB, Robert, …) | C+ |
| Multi-modal inputs | D+ |
| Real-time streaming | Future |
| Production load / multi-region HA | D |
| Doctrine-1B crypto signer authenticity | Doctrine-1B |
| Operator full dashboard UI | C (CLI/minimal surface required in B — see §3.1) |
| OpenRouter | C/D |

Scope additions during the build window go to a **Phase C queue**, not the active build.

---

## 3. Architectural Components to Build

### 3.1 Build Inventory (Owners Required)

| Component | Purpose | Production acceptance | Owner |
|-----------|---------|----------------------|-------|
| Coordinate registry | Storage + lookup of populated coordinates | Schema versioned; health heartbeat; empty-coordinate spawn/escalate policy | _TBD_ |
| Intake classifier | Assigns coordinates to tasks | 3-stage; confidence + escalate path; labeled metrics | _TBD_ |
| Routing layer | Coordinate → endpoint; channel enforcement | Fail-closed; no silent drop | _TBD_ |
| Context Envelope library | Serialize/deserialize/sign envelopes | Schema version; required fields; signature verify | _TBD_ |
| Channel rule engine | Evaluate rules at boundaries | Default-deny; tag-add on sensitivity↑; audit event | _TBD_ |
| Minimal authority module | Phase B stand-in for Decision Tokens | Bootstrap grant verify on sensitivity↑ | _TBD_ |
| Provenance store | Append-only hash-chained event log | Postgres; integrity job; restore drill | _TBD_ |
| Memory store (cell) | Ephemeral scoped state | TTL + scope tags; deny cross-scope | _TBD_ |
| Task/state store | Durable workflow state | Resume after restart; idempotency keys | _TBD_ |
| Three agent runtimes | Research / structure / review workers | Direct APIs; timeout; structured I/O | _TBD_ |
| Validation harness | Eval + failure injection | Automates M/F/A; CI-runnable | _TBD_ |
| Telemetry | Logs, metrics, traces | OTel; correlation IDs across handoffs | _TBD_ |
| Operator surface (minimal) | View tasks, failures, quarantine | **CLI or single page required** (full dashboard deferrable) | _TBD_ |
| Kill switch | Global halt of new tasks + in-flight freeze | Documented; tested | _TBD_ |

Suggested RACI until named: Chris = architecture + sign-off; implementers = build; Bob (chief of staff) = ops coordination; on-call for soft launch named in §9.

### 3.2 Tech Stack (Default; Overridable via Q10)

| Layer | Choice | Production notes |
|-------|--------|------------------|
| Language / runtime | Python 3.11+ | Aligns with reference Mesh package story |
| Orchestration | LangGraph | Agent chain only; **not** a substitute for channel/provenance enforcement |
| Envelope | JSON + Ed25519 (or HMAC-SHA256 if keys not ready — must document downgrade) | Prefer Ed25519; if HMAC pilot, escalate to Ed25519 before Phase C |
| Provenance | PostgreSQL append-only + SHA-256 hash chain | No UPDATE/DELETE on ledger table; app role lacks those grants |
| Task state | PostgreSQL | Same instance OK if schemas isolated |
| Cell memory | Redis TTL **or** Postgres JSONB if Redis absent | Choose based on Q7 inventory; do not invent Redis “because plan said so” |
| Classifier Stage 1–2 | Deterministic rules | Hot-path latency SLOs apply here |
| Classifier Stage 3 | Haiku structured output | Escalation path; **separate** latency metric |
| Telemetry | OpenTelemetry → existing sink or Honeycomb | Correlation: `task_id`, `handoff_id`, `envelope_hash` |
| Deploy | Existing Vultr | Capacity check Day 0 |
| Secrets | Prefer existing KMS/Vault; else sealed env + rotation runbook | Document downgrade explicitly |
| Model APIs | Direct Gemini / Anthropic only | No OpenRouter in B |

**Adapter stub (if Q1=A):** `mesh/adapters/resolver_stub.py` with interface compatible with future MeshResolver wrap — no dual implementation.

### 3.3 Delivery & Consistency Semantics (Production Floor)

| Concern | Phase B rule |
|---------|--------------|
| At-least-once handoff delivery | Yes |
| Exactly-once **agent step effects** | Best-effort via idempotency key = `hash(task_id, step, attempt_bucket)` |
| Side effects | Workers must be idempotent or write to side-effect ledger before external call |
| Poison messages | After `max_retries`, quarantine + operator surface; never silent drop |
| Clock | Single trusted NTP source on Vultr; reject envelopes with `created_at` skew &gt; 5 min |
| Concurrency | One active executor per `task_id` (lease/lock) |

### 3.4 Build Dependency Graph (Rebaselined)

Calendar is **relative to Kickoff Day (T0)**, not May 30. Soft-launch target proposal: **T0 + 30 calendar days**, contingent on owners assigned at T0.

| Window | Deliverables | Parallel tracks |
|--------|--------------|-----------------|
| T0 | Owners named; infra inventory; secrets path; kill switch design; eval set v0 reviewed by Chris | — |
| T0–T3 | Coordinate registry + Envelope library + schema freeze | Threat model draft |
| T0–T4 | Provenance store + integrity checker | Backup/restore drill |
| T4–T8 | Routing + channel rules + minimal authority | Failure-injection hooks |
| T8–T13 | Three agent runtimes + idempotent step runner | Telemetry correlation |
| T13–T16 | Memory scope enforcement + task state resume | Operator CLI |
| T16–T19 | Intake classifier (rules + escalate) | Eval set v1 gold labels |
| T19–T23 | Validation harness + chaos suite (F1–F8) | CI gates |
| T23–T27 | E2E integration + security floor tests | Runbooks |
| T27–T30 | Eval campaigns + Soft Launch Readiness Review (SLRR) | Freeze Phase C queue |

**Slip rule:** Core M/F/A slip → soft launch slips. Dashboard UI may slip; operator CLI may not. Performance &gt;2× targets → tag for Phase D, not a hard block (same as draft).

---

## 4. Pilot Validation Criteria

Ship gate: **all M, F, A, S, O** pass. P within 2× (or documented Phase D tag).

### 4.1 Mechanical Correctness (Primary)

| # | Criterion | Measurement |
|---|-----------|-------------|
| M1 | 3-agent chain correct output ≥90% | 50-task labeled eval; rubric in §5 |
| M2 | Handoff E2E success ≥99% when no injection | Successful E2E / total |
| M3 | Eval covers ≥5 task variations + ≥3 ambiguity patterns | Design review sign-off |
| M4 | Every handoff has complete Context Envelope | 100% in audit |
| M5 | Every completed task has valid hash-chained provenance | 100% integrity check |
| M6 | Every sensitivity↑ handoff has valid minimal authority proof | 100% |

### 4.2 Failure Mode Survival (Primary)

“Correct” = recover within bounds **or** fail closed with logging + operator surface. Never silent drop / silent wrong route.

| # | Failure mode | Required behavior |
|---|--------------|-------------------|
| F1 | Transient destination failure | Retry ≤ `max_retries` (default 3) with backoff; each attempt in provenance; exactly which attempt succeeded |
| F2 | Classification ambiguity | Below confidence threshold → escalate path; log uncertainty; **no silent wrong coordinate** |
| F3 | Destination unavailable + no spawn + no fallback | Hard fail `UNROUTABLE`; operator surface; quarantine |
| F4 | Partial failure mid-chain | Resume from last committed handoff; provenance shows partial + recovery |
| F5 | Process restart mid-task | Durable state; resume; no duplicate **committed** step effects |
| F6 | Agent killed mid-execution | Detect via lease timeout; retry or escalate; no orphan leases; no duplicate side effects |
| F7 | Channel rule violation | Reject at enforcement point; log; operator surface |
| F8 | Provenance hash mismatch | Detect; reject; alert; quarantine forensic |
| F9 | Idempotency conflict / replayed step | Second execution no-ops or rejects; provenance records replay attempt |
| F10 | Envelope signature invalid | Reject; alert; do not execute |

### 4.3 Performance (Secondary)

| # | Criterion | Target | Applies to |
|---|-----------|--------|------------|
| P1a | Intake classification (rules Stages 1–2) | p50 &lt; 100ms, p95 &lt; 300ms | Hot path |
| P1b | Classification escalate (LLM Stage 3) | p50 &lt; 2s, p95 &lt; 5s | Escalation only; **not** soft-launch blocker if P1a holds |
| P2 | Inner-grid handoff (intra-cell, excl. model time) | p50 &lt; 50ms, p95 &lt; 150ms | Mesh overhead |
| P3 | Cross-cell handoff (sensitivity boundary, excl. model) | p50 &lt; 200ms, p95 &lt; 500ms | Mesh overhead |
| P4 | E2E 3-agent workflow | p50 &lt; 60s, p95 &lt; 180s | Includes model latency |

If mesh overhead (P2/P3) is &gt;10× off, treat as architectural defect (hard look), not “Phase D polish.”

### 4.4 Audit & Provenance (Primary)

| # | Criterion | Measurement |
|---|-----------|-------------|
| A1 | Auditable event per handoff | events / handoffs = 1.0 |
| A2 | Hash chain integrity anytime | Periodic job + on-read verify |
| A3 | Reconstruct trail from logs alone | Kill live state; reconstruct from audit |
| A4 | Tamper detectable | Injected fake event fails integrity |
| A5 | Backup/restore drill | Restore Postgres; chain still verifies |

### 4.5 Security Floor (Primary — New)

| # | Criterion | Measurement |
|---|-----------|-------------|
| S1 | Threat model published for Phase B scope | Reviewed doc in repo |
| S2 | Prompt-injection / exfil suite on boundary | ≥10 adversarial cases; zero unauthorized confidential egress |
| S3 | Secrets not in git / logs | Secret scan + log redaction check |
| S4 | Kill switch stops new admissions &lt; 60s | Chaos test |
| S5 | Soft-launch users cannot read other users’ confidential outputs | Access control test |
| S6 | No claim of Doctrine-1B crypto certification in UI/copy | Copy review |

### 4.6 Operability (Primary — New)

| # | Criterion | Measurement |
|---|-----------|-------------|
| O1 | Operator CLI: list tasks, show provenance, quarantine, retry-or-kill | Demo in SLRR |
| O2 | Runbooks for F1–F10 + kill switch + provenance break | Written + tabletop |
| O3 | On-call named for soft-launch window | Roster |
| O4 | CI: unit + contract + chaos subset green on main | Pipeline |
| O5 | Correlation IDs present on 100% of handoff spans | Trace sample |

### 4.7 Soft Launch Gate Decision

Soft launch ships only if:

- All **M, F, A, S, O** met  
- **P** within 2× (or explicit Phase D tag with no user-facing SLA)  
- SLRR checklist signed by Chris  

If any M/F/A/S/O fails → slip. Correctness before speed; safety before narrative.

---

## 5. Eval Set Design (Contract)

### 5.1 Composition (50 tasks)

| Category | Count | Purpose |
|----------|-------|---------|
| Clean — research-public | 15 | Baseline routing |
| Clean — confidential / boundary | 10 | Boundary crossing |
| Ambiguous — research vs structure | 5 | Classifier stress |
| Ambiguous — sensitivity unclear | 5 | Sensitivity rules |
| Multi-step full 3-agent | 10 | E2E chain |
| Failure scenarios (injected) | 5 | F-series |

### 5.2 Per-Task Required Fields

Each task record **must** include:

1. `task_id`  
2. Input text  
3. Gold coordinate **sequence** (not only first hop)  
4. Expected boundary events (none | public→confidential)  
5. Expected authority check outcome  
6. Output rubric (must-include / must-not-include / quality bar)  
7. Ambiguity expected behavior (if any)  
8. Injected failure + expected recovery (if any)  
9. Sensitivity of fixtures (public fixtures vs synthetic internal stubs)

**Internal capability data:** Use a **synthetic confidential fixture pack** for automated eval. Real internal data only in soft-launch with §0 Q8 policy.

### 5.3 Examples (unchanged intent, hardened expectation)

**Clean research-public:**  
“Analyze public technical positioning of Procore for mechanical contractors.”  
Gold: `…research.public.balanced.text.long` · no sensitivity↑ · output = public-sources-only summary.

**Boundary:**  
“Compare Procore positioning against Buildtronix competitive moat.”  
Gold sequence: research.public → structure.confidential → (optional) review.confidential · authority proof required at hop 1→2.

**Ambiguous:**  
“Tell me about ServiceTitan.”  
Expect low confidence; escalate or default per written policy; **never silent wrong confidential route**.

**Failure injection:**  
Kill structure agent mid-exec → retries recorded → success or operator escalation with full attempt provenance; no duplicate confidential write.

### 5.4 Ownership & Sign-Off

- Eval set owner: _TBD_  
- **Chris must sign** eval set v1 before T19 chaos campaign.  
- Sign-off artifact: `docs/phase-b/eval/SIGN_OFF.md` with date + commit SHA.

---

## 6. Security & Threat Model (Phase B Scope)

Minimum threats in scope (full write-up due T0–T3):

| Threat | Mitigation |
|--------|------------|
| Prompt injection in public research → coerce confidential egress | Channel enforce + output schema allowlist + S2 suite |
| Envelope forgery / replay | Signatures + nonces/idempotency + F9/F10 |
| Provenance tampering | Hash chain + A4/A5 |
| API key theft | Secrets store; least privilege; rotation runbook |
| Soft-launch lateral read | Per-user task ACL |
| Operator error | Kill switch; quarantine over delete |
| Dependency / supply chain | Lockfiles; pin model API versions where possible |

Out of scope for B (track for C/D): formal penetration test, SOC2, cross-tenant adversarial suite, hardware key ceremony.

---

## 7. Risk Register

| Risk | L | I | Mitigation |
|------|---|---|------------|
| 30-day window still aggressive | H | M | Pre-commit scope cuts; parallel chaos; CLI not UI |
| Eval set late | M | H | Chris drafts v0 at T0; owner refines |
| Classifier &lt;95% | M | M | Escalation to stronger model on ambiguity; tune in D |
| Architecture dualism (v1.1 vs v2.3) | H | H | Q1 mandatory; adapter stub only |
| Owners unassigned | C | C | **Block kickoff** |
| Scope creep | H | H | Chris “no additions” commitment; Phase C queue |
| Infra assumptions wrong | M | H | Q7 Day-0 inventory; AWS fallback scoped not built |
| Failure injection finds architectural gap | M | H | Slip launch; revise spec — intended outcome |
| Confidential data leak in soft launch | M | C | Synthetic eval fixtures; Q8 policy; S5 tests |
| Marketing overclaims certification | M | H | S6 copy gate |
| Timeline stigma from missed May 30 | M | L | Rebaseline publicly inside company; no backdating |

---

## 8. Phase B → Phase C / Doctrine-1B Handoff

Phase B exit package:

1. Catalog of observed failure modes (expected + novel)  
2. Latency baselines (P1a/b, P2–P4)  
3. Classifier accuracy + confusion matrix  
4. Architecture decisions invalidated by reality  
5. Updated v1.1 → proposed **v1.2** delta  
6. Explicit gap list vs v2.3 MeshResolver / ProofPackage (input to integration)  
7. Soft-launch 2-week ops report  

**Phase C** (Decision Tokens, approval gates, authority inheritance) starts only after B exit.  
**Doctrine-1B** (crypto signer authenticity) is scheduled independently; do not silently fold into C without capacity.

---

## 9. Soft Launch Definition (Proposed)

| Dimension | Proposal |
|-----------|----------|
| Audience | Chris + 2–3 named Buildtronix users |
| Access | Allowlisted accounts; per-task ACL |
| Volume | 10–20 real tasks/day + continuous synthetic eval |
| Mode | Every task tagged `pilot=true`; **manual review before business action** |
| Data | Prefer synthetic/internal-stub for demos; real confidential use only under Q8 |
| Duration | 14 days ops → Phase C planning |
| Success | No unrecoverable failure; no security incident; all kill-switch/provenance alerts explained |
| On-call | Named primary + backup |
| Copy | “Internal pilot — not certified constitutional governance” |

If accepted, Phase C kickoff target = soft-launch end + 1 week planning buffer.

---

## 10. CI, Environments, Rollback

| Item | Requirement |
|------|-------------|
| Environments | `dev` (local) · `pilot` (Vultr) — no prod alias |
| CI gates | lint · unit · envelope/provenance contract · subset chaos |
| Migrations | Expand/contract; never rewrite ledger rows |
| Rollback | Kill switch + prior container image pin; ledger is append-only (no rollback of history) |
| Data retention | Pilot retention policy written at T0 (suggest 90 days) |

---

## 11. Budget (Reconcile)

| Bucket | Guidance |
|--------|----------|
| Model + infra (30 days) | Align to v1.1 ~$1–2k/mo band unless volume higher; justify outliers |
| Tools (Honeycomb, etc.) | Cap explicitly |
| Contractors | Separate from compute; named in Q9 |
| Hard stop | Written dollar cap; spend review at T15 |

---

## 12. Sign-Off Checklist

Before execution, Chris signs:

- [ ] §0 answers (Q1–Q10)  
- [ ] Workflow selection  
- [ ] Out-of-scope list  
- [ ] Tech stack (or overrides)  
- [ ] Validation criteria M/F/P/A/S/O  
- [ ] Eval set composition + Chris review commitment  
- [ ] Risk register  
- [ ] Component owners  
- [ ] Budget  
- [ ] Soft launch definition  
- [ ] Acknowledgement: Phase B ≠ Doctrine-1B certification  

Once signed, Phase B is locked. Changes → Phase C queue.

---

## 13. Clarifying Questions (For Chris — Full List)

### Blocking (also in §0)

1. **Q1 Substrate:** Is Phase B strictly v1.1 envelopes/channels, or must MeshResolver/ProofPackage be on the hot path now?  
2. **Q2 Code home:** Where does the implementation live relative to this marketing repo and existing Vultr Bob/OpenClaw code?  
3. **Q3 Owners:** Who owns each §3.1 component?  
4. **Q4 Date:** Confirm soft-launch target as T0+30 or set an absolute date.  
5. **Q5 Authority:** What is the minimal public→confidential authorization artifact without Decision Tokens?  
6. **Q6 Latency:** Confirm split P1a/P1b vs keeping a single (currently unmeetable) classifier SLO.  
7. **Q7 Infra:** What is already running on Vultr today?  
8. **Q8 Audience/data:** Who sees confidential outputs, and may real internal capability data be used?  
9. **Q9 Budget:** Hard cap and contractor plan?  
10. **Q10 Stack:** Any rejects (LangGraph, Redis, Honeycomb, Ed25519, Haiku)?  

### Important (Answer by T3)

11. Numeric **confidence threshold** for classifier escalate?  
12. Exact **max_retries / timeout / lease** budgets?  
13. Is **HMAC acceptable** as envelope signature downgrade for pilot, or is Ed25519 mandatory Day 1?  
14. Should operator surface be **CLI-only** or is a minimal web page required?  
15. Soft-launch **success metric** beyond “no unrecoverable failure” — any business KPI?  
16. Relationship to **Design^BOB / Competitive Intel Agent** existing code — wrap, rewrite, or strangler?  
17. May we publish this plan in-repo (this PR), or is distribution restricted to confidential channels only?  

---

## Document Control

| Version | Date | Notes |
|---------|------|-------|
| Draft | ~May 2026 | Original Phase B plan (May 30 target) |
| v1.1-PRODUCTION | 2026-07-16 | Rebaselined; S/O gates; idempotency; dual-architecture reconciliation; Doctrine-1B naming split |

*End of Phase B Inner-First Build Plan (Production v1.1).*
