<!--
CONFIDENTIAL — PRE-PATENT — DO NOT EXTERNALLY CIRCULATE
Track-A production-governance activation. Builds on already-disclosed Patent 1/2 architecture.
Does not contain Patent-3 belief-graph/reconciliation schemas. See §1 Disclosure note.
-->

# TronixMesh Activation Directive

**Artifact ID:** `TRONIXMESH_ACTIVATION_DIRECTIVE_v1.0`
**Version:** 1.0 (consolidated + Patch Addendum v1.1 merged; rev. 2026-08-16 incorporating Chairman-review feedback)
**Status:** **PENDING CHAIRMAN LOCK — NON-CANONICAL**
**Lock timestamp:** *(set at Chairman lock)*
**Document hash:** *(SHA-256 generated at Chairman lock over the final approved bytes)*
**Approving authority:** Christopher C. Leiser, Chairman
**Prepared:** 2026-08-16 (synthesis)
**Relationship to Canonical Manifest:** Not yet entered. On lock, hashed and entered with an authority tier and effective epoch (§11.3).
**Change control:** Amendments require Chairman-approved change control (§11.3).

**Patch provenance (Addendum v1.1 → sections):** P1→§2 · P2→§5 · P3→§3 · P4→§4 · P5→§6 · P6→§11 · P7→§7 · P8→§8.

> **Authority status.** This directive is **PENDING / NON-CANONICAL**. BOB may prepare analysis from it
> but SHALL NOT treat it as superior to existing locked canonical artifacts until Chairman lock, hash
> generation, and Canonical Manifest entry are complete. Where a higher normative authority conflicts
> with this directive, the higher authority wins unless Chairman-approved change control formally amends
> it.

---

## Decisions Required from Chairman (resolve at lock)

These are the explicit decision points for the lock signature:

1. **Final A10 shadow-coverage threshold** — freeze the observation period + workload count + coverage rule **before** shadow begins (§2.1).
2. **Cutover scope** — approve `TRONIXMESH_BOB_CUTOVER_SCOPE_v1.0`: which workload classes are IN-SCOPE at initial cutover, and which are temporarily excluded and why (§5.1).
3. **Cutover authority basis** — confirm whether production cutover runs on Phase B **bootstrap-grant** authority or requires the Phase C **Decision-Token** path (§11.2 flag).
4. **Coordination mechanism** — confirm the decision rule (authoritative coordination required; PostgreSQL transactional authority vs Raft chosen **only after** inventory shows whether single-authority transactional semantics suffice; §8.1).
5. **Runtime Spec v1.1 blockers** — approve/deny any Runtime Specification amendments that gate the critical path (external artifact; §11.1).
6. **Disclosure / Track C** — direct the response to the public-repo exposure of the Patent-3-sensitive cognitive-mesh material now on `main` (Track C, §0; Paris deadline **2027-05-22**).

---

## 0. Purpose and track structure

Get the **smallest defensible implementation** of TronixMesh governing **real BOB production effects** —
with authorization, durable INTENT, attributable evidence, recovery, and reconstructability **proven
before** expanding cognition. Core principle: **get governance alive first; make it intelligent second.**

### 0.1 Three tracks

| Track | Scope | Blocking relationship |
|-------|-------|-----------------------|
| **A — Production Governance** | The critical path to "TronixMesh Alive" (§8) | **The critical path.** Everything gates here |
| **B — Epistemic / Cognitive Mesh** | Belief graph, reconciliation, cognitive channels (`../cognitive-mesh/`) | **Parallel and non-blocking**, except a genuine safety/governance defect via the §7 blocking-finding procedure. **SHALL NOT** sit on the production critical path |
| **C — Patent / IP Protection** | Patent 3 filing + counsel review; controls external circulation of Track-B material | **Hard deadline 2027-05-22** (Paris Convention). Gates external disclosure of belief-graph/reconciliation specs |

---

## 1. Disclosure note (read first)

This directive is Track-A production governance built on the **already-disclosed** coordinate-native
governance architecture (Patents 1 & 2; `../architecture/TRONIXMESH-ARCHITECTURE-v2.md`). It
**deliberately excludes** the Patent-3-sensitive belief-graph / dependence-aware reconciliation schemas
(`../cognitive-mesh/`), which remain gated behind Track C. Handle per the CONFIDENTIAL banner; do not
externally circulate before counsel review.

---

## 2. A10 — Shadow Production

Run representative real BOB production workloads through the current production path (actual execution)
and, simultaneously, the TronixMesh shadow path with **no external effect**:

```
production path → actual execution
TronixMesh shadow path →
    proposal
    → canonical-state lookup
    → governance evaluation
    → prediction
    → authorization decision
    → simulated INTENT/RESULT handling
    → NO external effect
```

**Shadow mode SHALL NOT be exited by judgment alone.**

### 2.1 A10 Exit Gate (objective)

**Workload coverage.** Shadow evaluation must cover every BOB workload class intended to be governed at
initial cutover, plus representative **allowed**, **denied**, **escalated**, **state-dependent**, and
**failure** actions.

> **FROZEN THRESHOLD (mandatory).** The exit threshold — observation period, workload count, and the
> coverage rule — **SHALL be frozen and Chairman-approved before shadow testing begins**, and recorded in
> the cutover-scope artifact (§5.1). It may not be adjusted after observing results.
>
> **Planning baseline for that freeze (subject to Chairman approval):** **≥ 3 consecutive operating days**
> **and** **≥ 100 representative effect-bearing production requests**, **and** complete coverage of every
> declared IN-SCOPE workload class — whichever is the larger requirement governs. A larger sample is used
> if required to cover every declared class.

**Decision comparison.** Every production external effect observed during shadow mode must have a
corresponding TronixMesh authorization disposition. Every disagreement between what production actually
did and what TronixMesh would have authorized must be individually **classified and dispositioned**. No
disagreement may remain unexplained at cutover.

> For safety-critical authorization behavior: **Unresolved authorization disagreement = 0.** An
> incorrect TronixMesh authorization that would permit an action prohibited by canonical policy is a
> **cutover blocker**.

**Fault-injection completion.** The complete pre-cutover fault matrix must pass. At minimum: verifier
unavailable; stale canonical state; conflicting canonical state; duplicate nonce; replay attempt;
malformed authorization envelope; invalid signature; expired delegation; excessive delegation scope;
database interruption; Evidence Authority unavailable; adapter timeout; provider response ambiguity;
crash after INTENT before external effect; crash after external effect before RESULT; duplicate
execution attempt; failed compensation; unresolved human escalation.

**Failure behavior.** If the A10 gate fails: BOB remains on the current production path; no cutover
authorization is issued; each failure is recorded; the defect is remediated; affected tests are rerun.
**There is no waiver-by-schedule.**

---

## 3. A10.5 — Governed Staging Effect Trial

Shadow mode validates decisions but does not exercise the complete effect boundary. Before production
cutover, run TronixMesh against a **real but isolated reversible** execution environment (throwaway Git
repository, sandbox filesystem, isolated test service, or equivalent). This SHALL execute **actual
effects**.

```
proposal
→ canonical-state verification
→ Governance Gate
→ authorization envelope
→ durable INTENT
→ actual external effect
→ RESULT
→ evidence append
→ reconstruction / reconciliation
```

Test actual: successful execution; denied execution; duplicate request; crash after INTENT before
effect; crash after effect before RESULT; restart/recovery; timeout; uncertain provider result;
idempotent retry; compensation; failed compensation; human escalation.

### 3.1 A10.5 Exit Gate

Production cutover is **prohibited** until: actual reversible effects execute correctly; **no
unauthorized effect** occurs; INTENT/RESULT reconstruction succeeds; incomplete-effect recovery behaves
per Runtime Spec; duplicate-execution protection passes; compensation remains **bounded**; failed
compensation **escalates rather than recursing**.

---

## 4. Adversarial testing

### 4.1 Pre-Cutover Adversarial Suite (part of the A10 / A10.5 exit gate)

Any attack that is **cheap and safe** to run before cutover SHALL be part of the exit gate — not
postponed to production. Execute against staging/shadow configuration: prompt injection;
policy-confusion; attempted governance reinterpretation; forged principal identity; invalid credential;
replay; nonce reuse; stale authorization; expired authorization; excessive delegation; poisoned
evidence; forged provenance; circular evidence / self-confirmation; fabricated tool-result claims; model
falsely claiming execution occurred; compromised/malicious adapter responses; contradictory state;
unavailable authority; deliberate timing races; crash-boundary attacks; attempted compensation
recursion.

### 4.2 A12 — Post-Cutover Production Red-Team

After cutover, rerun the applicable suite against the **actual production configuration** and add attacks
requiring live infrastructure characteristics. Production attack testing must respect **blast-radius
limits** and must not deliberately create uncontrolled external harm.

---

## 5. "TronixMesh Alive" milestone & cutover scope

### 5.1 Cutover-scope artifact (create before A11 cutover)

Create **`TRONIXMESH_BOB_CUTOVER_SCOPE_v1.0`** declaring, per BOB workload class: whether it is governed
by TronixMesh at cutover; which classes remain temporarily excluded and why; current external-effect
volume attributable to each class; planned migration date for each excluded class; fallback behavior;
responsible owner; **and the frozen A10 exit threshold (§2.1).**

**Cutover coverage rule.** Within every **IN-SCOPE** class, **100% of external effects** must pass
through the TronixMesh Governance Gate. No alternate ungoverned execution path may exist for an in-scope
class. Publish the proportion of BOB's total production external-effect activity represented by the
in-scope classes.

> **Language discipline.** Do **not** claim "BOB is fully governed by TronixMesh" if material workload
> classes remain outside the gate. Use: *"TronixMesh governs 100% of external effects within the declared
> production scope, representing X% of BOB's measured production effect activity during the reporting
> period."*

### 5.2 Alive definition (locked)

**TRONIXMESH ALIVE** occurs when: (1) BOB performs real production work through TronixMesh; (2) all
external effects in the declared cutover scope pass through the Governance Gate; (3) valid authorization
is required; (4) durable INTENT precedes governed execution; (5) attributable RESULT evidence follows
execution; (6) actions are **reconstructable from authoritative evidence, independent of BOB
self-report**; (7) the pre-cutover gates have passed. The cutover-scope document is part of the evidence
supporting the milestone.

> **BOB CUTOVER = TRONIXMESH ALIVE.**

---

## 6. A13 — 30-Day Pre-Registered Proof Period

A13 SHALL NOT merely collect telemetry. Before the run begins, create
**`TRONIXMESH_30_DAY_PROOF_PROTOCOL_v1.0`** and **freeze evaluation criteria before observing final
results**.

**Zero-tolerance criteria (mandatory):**

| Criterion | Target |
|-----------|--------|
| Unauthorized external effects | **0** (no governed external effect without valid authorization under applicable canonical policy) |
| Evidence reconstruction (authorization → INTENT → effect/result → evidence chain) | **100%** of sampled governed actions; sampling procedure declared beforehand |
| Unresolved denials / escalations | **0** (final disposition or explicitly documented still-open state with accountable ownership; no silent disappearance) |
| Evidence-chain integrity | No known undetected mutation, unexplained ledger discontinuity, or unaccounted authoritative-state divergence |

**Operational metrics (also measured):** runtime availability; false-positive denial rate;
human-intervention rate; mean escalation latency; failed execution rate; recovery success; adapter
errors; provider ambiguity; governance latency overhead; evidence-writing overhead.

> **No post-selection.** Availability and intervention targets are judgment-call metrics. Either
> **pre-register thresholds** before the proof period, **or** explicitly label the first 30-day period as
> **baseline measurement** for that metric and use it to set prospective thresholds for the next
> operating period. Do not retroactively declare thresholds after observing the data.

---

## 7. Track B blocking-dispute authority (Blocking-Finding Procedure)

Track B may block Track A when it discovers a defect affecting governance, authorization, evidence
integrity, execution safety, effect-commit semantics, or reconstruction — subject to this adjudication
rule.

**Blocking-finding procedure.** When Track B identifies a potential Track A blocker: (1) record the
finding; (2) identify the affected invariant; (3) provide evidence; (4) identify plausible production
consequence; (5) classify severity; (6) recommend remediation. BOB / reconciliation / implementation
agents do **not** possess unilateral authority to dismiss the blocker.

**Final adjudication authority.** The **Chairman** is the resolution authority for program-level blocking
disputes. Technical evidence may be supplied by BOB, independent reviewers, developers, acceptance-test
results, or runtime evidence; final program disposition remains human-authorized unless delegated
explicitly in canonical policy.

**Default while disputed (tightened).** Any finding touching **authorization, identity, replay
protection, governance integrity, evidence integrity, effect-commit semantics, execution safety, or
reconstructability** defaults to **FAIL CLOSED**: treat as blocking **and pause all cutover-related work
until adjudicated**. Findings **not** touching those invariants do **not** pause cutover work; Track A
continues while adjudication proceeds.

---

## 8. Critical path (pre-Alive)

```
Runtime blocker closure
→ actual-state inventory                     (§10 — first executable work after lock)
→ verify existing identity/key/nonce/store components
→ RR-0056 Evidence Authority hardening
→ canonical state registry
→ Governance Gate
→ Predictive Execution Wrapper (INTENT/RESULT)
→ one reversible production adapter
→ acceptance tests
→ shadow production (A10)                     (§2)
→ pre-cutover adversarial suite               (§4.1)
→ real reversible staging effects (A10.5)     (§3)
→ cutover-scope approval                      (§5.1)
→ BOB production cutover                      → TRONIXMESH ALIVE (§5.2)

then:
production red-team rerun (A12)               (§4.2)
→ 30-day pre-registered proof period (A13)    (§6)
→ hardening
→ scope expansion
```

Track B remains **parallel and non-blocking** except under the §7 blocking-finding procedure.

### 8.1 Coordination-mechanism decision rule

> **Authoritative coordination is required; the specific mechanism is chosen only after the inventory.**
> PostgreSQL single-authority transactional semantics vs Raft (or equivalent distributed consensus) is
> decided **only after** the actual-state inventory (§10) shows whether single-authority transactional
> semantics suffice for the in-scope workload. **Distributed consensus is not a sophistication goal**;
> prefer the simplest mechanism that guarantees authoritative, serializable commit. Do not adopt Raft as
> a future "badge"; adopt it only if a concrete inventory finding requires it.

---

## 9. Governance interpretation & denied-action lifecycle (deterministic-first)

Governance interpretation is **deterministic first**; the epistemic reconciler does **not** arbitrate
governance ambiguity. A cognitive process may propose an interpretation; the canonical governance
interpreter evaluates it; **DETERMINATE** → allow/deny; **AMBIGUOUS** → `GOVERNANCE_DISPUTE` →
**human constitutional authority**.

**Quarantine rule.** Do **not** quarantine for misinterpretation (that is error, not attack). **Do**
quarantine for repeated bypass attempts, unauthorized mutation, forged authority, or policy-evasion
behavior.

**Denied-action belief lifecycle.** A belief such as "X likely maximizes profit" (ACCEPTED) with
governance "X prohibited" derives `ACTION_FEASIBILITY = PROHIBITED`; the planner searches for permitted
alternatives; no repeated reconsideration of X without a governance-review request. (Consistent with the
cognitive-mesh doctrine that governance constrains **action**, not **observation**.)

---

## 10. Repository / Implementation Inventory (fulfils canonical Section 22)

Actual-state inventory of this repository as of `origin/main` @ `be3bfad`. **Evidence over self-report.**
Test evidence: `cd python && pytest` → **15 passed** (also **15 passed** with
`TRONIX_VERIFY_SIGNATURES=1`), Python 3.12.3, pytest 9.1.1. Commit of record for the Phase B primitives:
`51485d4` ("Phase B Gate 0 signed + T0 runtime").

**Status legend (static vs operational evidence are distinct):**

- `RUNTIME-VERIFIED` — exercised end-to-end in a **live/shadow** environment (strongest evidence). Available only from A10/A10.5 onward.
- `UNIT-VERIFIED` — code present + passing **unit** test (static/functional evidence only; **not** operationally exercised).
- `PARTIAL` — code present but incomplete versus the activation requirement.
- `ABSENT` — not implemented in this repository.

> **No component is `RUNTIME-VERIFIED` yet** — nothing here has been exercised in a live/shadow
> environment. That status becomes attainable during A10/A10.5, not before.

| Critical-path component | Status | Evidence / notes |
|-------------------------|--------|------------------|
| Coordinate addressing | **UNIT-VERIFIED** | `python/tronixmesh/coordinate.py`; `tests/test_coordinate.py` (parse/canonical, invalid-segment, sensitivity) |
| Envelope + signatures (Ed25519) | **UNIT-VERIFIED** | `envelope.py`, `signing.py`; `tests/test_envelope_adr0004.py` (sign/verify, tamper-fails-verify, frozen fields) |
| Key component | **UNIT-VERIFIED** | `signing.py` Ed25519 + HMAC-SHA256; covered by envelope tests |
| Store (append-only, hash-chained) | **UNIT-VERIFIED** | `provenance.py` (SQLite; `verify_chain`); `tests/test_provenance.py` (chain integrity, tamper detected) |
| Governance state machine (fail-closed) | **PARTIAL** | `governance.py` (`transition` fail-closed, `may_execute`); `tests/test_governance.py`. Not yet wired as a Governance Gate over authorization envelopes + canonical-state lookup |
| Channel + minimal authority handoff | **UNIT-VERIFIED** (Phase B bootstrap) | `channel.py`, `authority.py`, `handoff.py`; `tests/test_handoff.py`. Decision Tokens deferred to Phase C |
| Identity / principal binding | **PARTIAL** | Coordinate + bootstrap-grant function identity only; no principal/credential registry or credential-bound `source_identity` |
| **Nonce ledger / replay protection** | **ABSENT** | No nonce/replay module. **Required by the A10 fault matrix (duplicate nonce, replay).** |
| **RR-0056 Evidence Authority (hardened)** | **PARTIAL** | `provenance.py` = SQLite hash chain (Phase B primitive). RR-0056 SECURITY-DEFINER Postgres append-only, tenant-scoped chains, external anchoring: **not implemented** |
| **Canonical state registry (CURRENT_STATE)** | **ABSENT** | `registry.py` is a *coordinate/endpoint* registry, not an authoritative-state store with versioned reads |
| **Governance Gate (wired)** | **ABSENT** | State-machine kernel exists; a gate requiring valid authorization + canonical-state lookup for every in-scope external effect is not assembled |
| **Predictive Execution Wrapper (INTENT/RESULT)** | **ABSENT** | No durable INTENT-before-effect / RESULT-after-effect wrapper; no crash-boundary recovery |
| **Reversible production adapter** | **ABSENT** | No adapter (throwaway Git / sandbox FS) implementing the A10.5 effect boundary |
| Acceptance-test harness (activation) | **ABSENT** | 15 unit tests exist; no activation acceptance suite, shadow harness, fault-injection matrix, or adversarial suite |
| Feature flags | **UNIT-VERIFIED** | `flags.py` (`TRONIX_VERIFY_SIGNATURES`) exercised in handoff/verify paths |

**Runtime blocker closure** (first critical-path step) references the BOB-system runtime blocker,
**external to this repository**; disposition pending access to the BOB Canonical Manifest system.

**COMPLETE-claim rule honored:** no component is claimed operationally complete; `UNIT-VERIFIED` denotes
static test evidence only, `PARTIAL`/`ABSENT` are explicitly incomplete, and `RUNTIME-VERIFIED` is
reserved for live/shadow evidence not yet available. **No implementation-duration estimate is given.**

---

## 11. Canonicalization

### 11.1 Supersession matrix

This directive **amends specific clauses**; it does not wholesale-supersede prior artifacts. Format:
**Artifact → Section → Prior Rule → New Rule → Reason → Authority.**

| Artifact | Section | Prior Rule | New Rule | Reason | Authority |
|----------|---------|-----------|----------|--------|-----------|
| Consolidated Activation Directive | A10 Shadow Production | Open-ended shadow, exitable by judgment | Objective A10 Exit Gate (Chairman-frozen coverage/period/count; unresolved auth disagreement = 0; full fault matrix) | Prevent judgment-only cutover | Chairman |
| Consolidated Activation Directive | Cutover / "Alive" | "Alive" undefined by workload coverage | `TRONIXMESH_BOB_CUTOVER_SCOPE_v1.0` + 100%-in-scope rule + precise language | Milestone cannot be gamed | Chairman |
| Consolidated Activation Directive | Effect testing | Shadow only (no real effects) | New A10.5 governed staging effect trial | Close simulated-vs-real gap | Chairman |
| Consolidated Activation Directive | Red-team (A12) | Attacks only post-cutover | Cheap/safe attacks moved into A10/A10.5 exit gate | Find defects before production | Chairman |
| Consolidated Activation Directive | 30-day run (A13) | Telemetry collection | Pre-registered `TRONIXMESH_30_DAY_PROOF_PROTOCOL_v1.0` w/ zero-tolerance criteria | No post-selected success | Chairman |
| Consolidated Activation Directive | Track A/B relationship | Track B may block Track A | Blocking-finding procedure + Chairman adjudication + fail-closed default that pauses cutover work | Balance safety vs progress | Chairman |
| This directive | Governance | Unversioned normative message | Canonical artifact w/ hash + manifest entry (§11.3) | Directives must be versioned/canonical | Chairman |

**Prior artifacts requiring clause-level conflict inspection — list by exact title + date.** In-repo
artifacts (dated) are inspected in §11.2. Artifacts **external to this repository** (BOB Canonical
Manifest system) — **conflict inspection pending access; dates to be confirmed on access; do not assume
covered:**

- *TronixMesh Operating Doctrine* — (date pending access)
- *TronixMesh Engineering Directive* — (date pending access)
- *TronixMesh Runtime Specification* (incl. any v1.1) — (date pending access)
- *OpenClaw Migration Plan* — (date pending access; **keep fallback language exactly as written therein**)
- *Acceptance Test Plan* — (date pending access)
- *Prior activation / migration sequencing documents* — (dates pending access)

Categories requiring reconciliation (Patch 6): definition of "TronixMesh Alive"; production-cutover
sequencing; Cognitive Mesh relationship to production; Raft requirement or non-requirement (§8.1);
Evidence Authority sequencing; OpenClaw fallback rules; pre-cutover attack requirements.

### 11.2 Conflict inspection against in-repo canonical/locked artifacts (title + date)

| In-repo artifact (title — recorded date) | Potential conflict | Disposition |
|------------------------------------------|--------------------|-------------|
| *TronixMesh Design Doctrine* — 2026-07-17 | None — strict application of the trust stack / fail-closed / human sovereignty | Consistent |
| *TronixMesh Comprehensive Architecture Write-Up v2.0* — 2026-07-17 | "Alive" execution vs Decision Tokens; Phase B uses bootstrap grants | Cutover scope must state token vs bootstrap-grant posture per in-scope class |
| *Phase B Slice* — 2026-07-17 | Decision Tokens deferred to Phase C; production deploy is staged-rollout-gated | **Flag for Chairman (Decision 3):** confirm cutover authority basis |
| *Gate 0 Authorization — Phase B* — 2026-07-17 | Gate 0 authorized coding/T0, not production cutover | Production cutover is a new gate requiring its own authorization |
| *Cognitive Architecture Directive v0.9* — 2026-08-15 | Cognition must stay off critical path | Consistent — §7/§8 keep Track B non-blocking |
| *Epistemic Substrate Spec v0.2* — 2026-08-15 | (Track B; Patent-3 sensitive) | Consistent; Track C controls its external disclosure |

### 11.3 Canonical Manifest entry (after Chairman lock)

1. Hash the final directive (SHA-256 over approved bytes).
2. Enter version + hash into the Canonical Manifest.
3. Assign its authority tier.
4. Mark superseded subordinate clauses (§11.1).
5. Record effective epoch / time.

Until all five complete, this directive remains **PENDING / NON-CANONICAL**. **Change control:**
amendments require Chairman approval, re-hash, and a new manifest entry; a higher normative authority
wins over this directive unless Chairman-approved change control amends it.

---

## 12. Disposition of the immediate instruction, and post-lock hand-off

| # | Instruction | Disposition |
|---|-------------|-------------|
| 1 | Merge patches into the consolidated Activation Directive | Done — Patches 1–8 merged (§2–§9) |
| 2 | Create the supersession matrix | Done — §11.1 (in-repo, dated) + external-artifact list (titles; dates pending access) |
| 3 | Inspect Canonical Manifest & locked artifacts for conflicts | In-repo done (§11.2); BOB-system artifacts **pending access** |
| 4 | Return proposed `TRONIXMESH_ACTIVATION_DIRECTIVE_v1.0.md` | This document |
| 5 | Mark PENDING CHAIRMAN LOCK | Done — header + §11.3 |
| 6 | Repository/implementation inventory (Section 22) | Done — §10, evidence-based |
| 7 | Support every COMPLETE claim with commit/test/runtime evidence | Done — §10 legend distinguishes static vs operational evidence |

**Post-lock hand-off (unambiguous).** After Chairman lock, the **first and only** executable work is the
**actual-state inventory table (§10)** — verifying the status of existing components with commit/test/
runtime evidence and producing the dependency-sequenced implementation table. **No Epistemic Substrate
v0.2 drafting, no Reconciliation Protocol work, and no new high-level roadmaps** begin until that table
is produced and reviewed. Track B proceeds only as non-blocking parallel work under §7. Do not begin new
implementation merely because this directive exists; do not re-specify components already shown
operational; do not claim unverified components complete; do not estimate duration until the inventory
establishes what remains.

---

*End of TronixMesh Activation Directive v1.0 — PENDING CHAIRMAN LOCK.*
