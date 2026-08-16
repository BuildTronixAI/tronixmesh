<!--
CONFIDENTIAL — PRE-PATENT — DO NOT EXTERNALLY CIRCULATE
Track-A production-governance activation. Build on already-disclosed Patent 1/2 architecture.
Does not contain Patent-3 belief-graph/reconciliation schemas. See §Disclosure note.
-->

# TronixMesh Activation Directive

**Artifact ID:** `TRONIXMESH_ACTIVATION_DIRECTIVE_v1.0`
**Version:** 1.0 (consolidated + Patch Addendum v1.1 merged)
**Status:** **PENDING CHAIRMAN LOCK — NON-CANONICAL**
**Lock timestamp:** *(set at Chairman lock)*
**Document hash:** *(SHA-256 generated at Chairman lock over the final approved bytes)*
**Approving authority:** Christopher C. Leiser, Chairman
**Prepared:** 2026-08-16 (synthesis)
**Relationship to Canonical Manifest:** Not yet entered. On lock, this artifact is hashed and entered
into the Canonical Manifest with an authority tier and effective epoch (see §11).
**Change control:** Amendments require Chairman-approved change control (see §11.3).

> **Authority status.** This directive is **PENDING / NON-CANONICAL**. BOB may prepare analysis from it
> but SHALL NOT treat it as superior to existing locked canonical artifacts until Chairman lock, hash
> generation, and Canonical Manifest entry are complete. Where a higher normative authority conflicts
> with this directive, the higher authority wins unless Chairman-approved change control formally amends
> it.

---

## 0. Purpose

Get the **smallest defensible implementation** of TronixMesh governing **real BOB production effects** —
with authorization, durable INTENT, attributable evidence, recovery, and reconstructability **proven
before** expanding cognition. This document merges Patch Addendum v1.1 (Patches 1–8) into the
consolidated Activation Directive and defines the objective gates that make "TronixMesh Alive"
non-gameable.

**Scope discipline (locked):** the Epistemic / Cognitive Mesh track is **parallel and non-blocking** and
is **not on the production critical path** (§7, §8). Cognitive Mesh experimentation SHALL NOT be placed
on the production critical path.

---

## 1. Disclosure note (read first)

This directive is Track-A production governance built on the **already-disclosed** coordinate-native
governance architecture (Patents 1 & 2; see `../architecture/TRONIXMESH-ARCHITECTURE-v2.md`). It
**deliberately excludes** the Patent-3-sensitive belief-graph / dependence-aware reconciliation schemas,
which remain gated behind counsel review (see `../cognitive-mesh/`). Handle per the CONFIDENTIAL banner
above; do not externally circulate before counsel review.

---

## 2. A10 — Shadow Production *(Patch 1)*

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
**failure** actions. A minimum observation period and workload count SHALL be **frozen before** shadow
testing begins.

- Initial planning baseline: **≥ 3 consecutive operating days** and **≥ 100 representative
  effect-bearing production requests**, or a larger sample if required to cover every declared workload
  class.
- The final threshold is a **judgment call requiring Chairman approval before testing begins**.

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

## 3. A10.5 — Governed Staging Effect Trial *(Patch 3)*

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

## 4. Adversarial testing *(Patch 4)*

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

## 5. "TronixMesh Alive" milestone & cutover scope *(Patch 2)*

### 5.1 Cutover-scope artifact (create before A11 cutover)

Create **`TRONIXMESH_BOB_CUTOVER_SCOPE_v1.0`** declaring, per BOB workload class: whether it is governed
by TronixMesh at cutover; which classes remain temporarily excluded and why; current external-effect
volume attributable to each class; planned migration date for each excluded class; fallback behavior;
and responsible owner.

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
execution; (6) actions are reconstructable from authoritative evidence; (7) the pre-cutover gates have
passed. The cutover-scope document is part of the evidence supporting the milestone.

> **BOB CUTOVER = TRONIXMESH ALIVE.**

---

## 6. A13 — 30-Day Pre-Registered Proof Period *(Patch 5)*

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

## 7. Track B blocking-dispute authority *(Patch 7)*

Track B (Epistemic/Cognitive) may block Track A (production) when it discovers a defect affecting
governance, authorization, evidence integrity, execution safety, effect-commit semantics, or
reconstruction — subject to this adjudication rule.

**Blocking-finding procedure.** When Track B identifies a potential Track A blocker: (1) record the
finding; (2) identify the affected invariant; (3) provide evidence; (4) identify plausible production
consequence; (5) classify severity; (6) recommend remediation. BOB / reconciliation / implementation
agents do **not** possess unilateral authority to dismiss the blocker.

**Final adjudication authority.** The **Chairman** is the resolution authority for program-level blocking
disputes. Technical evidence may be supplied by BOB, independent reviewers, developers, acceptance-test
results, or runtime evidence; final program disposition remains human-authorized unless delegated
explicitly in canonical policy.

**Default while disputed.** If the alleged defect could reasonably compromise authorization, identity,
replay protection, governance integrity, evidence integrity, effect-commit semantics, execution safety,
or reconstructability → **FAIL CLOSED (treat as blocking until adjudicated)**. For findings unrelated to
those invariants, Track A may continue while adjudication occurs.

---

## 8. Critical path (pre-Alive) *(Patch 8)*

```
Runtime blocker closure
→ actual-state inventory                     (see §10)
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

The Epistemic/Cognitive track remains **parallel and non-blocking** except under the §7 blocking-finding
procedure.

---

## 9. Governance interpretation & denied-action lifecycle *(carried; deterministic-first)*

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

## 10. Section 22 — Repository / Implementation Inventory (evidence-based)

Actual-state inventory of this repository as of `origin/main` @ `be3bfad`. **Evidence over self-report.**
Test evidence: `cd python && pytest` → **15 passed** (and **15 passed** with
`TRONIX_VERIFY_SIGNATURES=1`), Python 3.12.3, pytest 9.1.1. Runtime commit of record for the Phase B
primitives: `51485d4` ("Phase B Gate 0 signed + T0 runtime").

**Status legend:** `VERIFIED` (code + passing test) · `PARTIAL` (code present; incomplete vs the
activation requirement) · `ABSENT` (not implemented in this repo).

| Critical-path component | Status | Evidence / notes |
|-------------------------|--------|------------------|
| Coordinate addressing | **VERIFIED** | `python/tronixmesh/coordinate.py`; `tests/test_coordinate.py` (3 tests: parse/canonical, invalid-segment, sensitivity) |
| Envelope + signatures (Ed25519) | **VERIFIED** | `envelope.py`, `signing.py`; `tests/test_envelope_adr0004.py` (sign/verify, tamper-fails-verify, frozen fields) |
| Key component | **VERIFIED** | `signing.py` Ed25519 + HMAC-SHA256; sign/verify covered by envelope tests |
| Store (append-only, hash-chained) | **VERIFIED** | `provenance.py` (SQLite; `verify_chain`); `tests/test_provenance.py` (chain integrity, tamper detected) |
| Governance state machine (fail-closed) | **PARTIAL** | `governance.py` (`transition` fail-closed, `may_execute`); `tests/test_governance.py` (happy path, illegal transition, reviewers-cannot-execute). Not yet wired as a full Governance Gate over authorization envelopes + canonical-state lookup |
| Channel + minimal authority handoff | **VERIFIED** (as Phase B bootstrap) | `channel.py`, `authority.py`, `handoff.py`; `tests/test_handoff.py` (authority-gated increase, denied without grant, UNROUTABLE). Decision Tokens deferred to Phase C |
| Identity / principal binding | **PARTIAL** | Coordinate + bootstrap-grant function identity only; no principal/credential registry or credential-bound `source_identity` |
| **Nonce ledger / replay protection** | **ABSENT** | No nonce/replay module present. Design doctrine lists nonce ledger as a target; not implemented. **Required by the A10 fault matrix (duplicate nonce, replay).** |
| **RR-0056 Evidence Authority (hardened)** | **PARTIAL** | `provenance.py` provides a SQLite hash chain (Phase B primitive). RR-0056 SECURITY-DEFINER Postgres append-only, tenant-scoped chains, external anchoring: **not implemented** |
| **Canonical state registry (CURRENT_STATE)** | **ABSENT** | `registry.py` is a *coordinate/endpoint* registry, not a canonical authoritative-state store with versioned reads |
| **Governance Gate (wired)** | **ABSENT** | State-machine kernel exists; a gate that requires valid authorization + canonical-state lookup for every in-scope external effect is not assembled |
| **Predictive Execution Wrapper (INTENT/RESULT)** | **ABSENT** | No durable INTENT-before-effect / RESULT-after-effect wrapper; no crash-boundary recovery |
| **Reversible production adapter** | **ABSENT** | No adapter (e.g. throwaway Git / sandbox FS) implementing the A10.5 effect boundary |
| Acceptance-test harness (activation) | **ABSENT** | 15 unit tests exist; no activation acceptance suite, shadow harness, fault-injection matrix, or adversarial suite |
| Feature flags | **VERIFIED** | `flags.py` (`TRONIX_VERIFY_SIGNATURES`) exercised in handoff/verify paths |

**Runtime blocker closure** (first critical-path step) references the BOB-system runtime blocker, which
is **external to this repository** and cannot be verified here; disposition pending access to the BOB
Canonical Manifest system.

**COMPLETE-claim rule honored:** no component above is marked complete without commit + passing-test
evidence; `PARTIAL`/`ABSENT` items are explicitly not claimed complete. **No implementation-duration
estimate is given**, per the immediate instruction — duration follows from remediating the `ABSENT`
critical-path items once the runtime blocker is closed.

---

## 11. Canonicalization *(Patch 6)*

### 11.1 Supersession matrix

This directive **amends specific clauses**; it does not wholesale-supersede prior artifacts. Format:
**Artifact → Section → Prior Rule → New Rule → Reason → Authority.**

| Artifact | Section | Prior Rule | New Rule | Reason | Authority |
|----------|---------|-----------|----------|--------|-----------|
| Consolidated Activation Directive | A10 Shadow Production | Open-ended shadow requirement, exitable by judgment | Objective A10 Exit Gate (frozen coverage/period/count; unresolved auth disagreement = 0; full fault matrix) | Prevent judgment-only cutover | Chairman |
| Consolidated Activation Directive | Cutover / "Alive" | "Alive" undefined by workload coverage | `TRONIXMESH_BOB_CUTOVER_SCOPE_v1.0` + 100%-in-scope coverage rule + precise language | Milestone cannot be gamed | Chairman |
| Consolidated Activation Directive | Effect testing | Shadow only (no real effects) | New **A10.5** governed staging effect trial (real reversible effects) before cutover | Close simulated-vs-real gap | Chairman |
| Consolidated Activation Directive | Red-team (A12) | Attacks only post-cutover | Cheap/safe attacks moved into A10/A10.5 pre-cutover exit gate | Find defects before production | Chairman |
| Consolidated Activation Directive | 30-day run (A13) | Telemetry collection | Pre-registered `TRONIXMESH_30_DAY_PROOF_PROTOCOL_v1.0` with zero-tolerance criteria | No post-selected success | Chairman |
| Consolidated Activation Directive | Track A/B relationship | Track B may block Track A | Blocking-finding procedure + Chairman adjudication + fail-closed default | Balance safety vs progress | Chairman |
| This directive | Governance | Unversioned normative message | Canonical artifact w/ hash + manifest entry (this §11) | Directives must be versioned/canonical | Chairman |

**Artifacts external to this repository** (in the BOB Canonical Manifest system) that MUST be inspected
for clause-level conflict before lock — **conflict inspection pending access**, do not assume covered:

- Operating Doctrine · Engineering Directive · Runtime Specification · OpenClaw Migration Plan ·
  Acceptance Test Plan · previous activation/migration sequencing documents.

Example categories requiring reconciliation (per Patch 6): definition of "TronixMesh Alive";
production-cutover sequencing; Cognitive Mesh relationship to production; Raft requirement or
non-requirement; Evidence Authority sequencing; OpenClaw fallback rules; pre-cutover attack requirements.

### 11.2 Conflict inspection against in-repo canonical/locked artifacts

| In-repo artifact | Potential conflict | Disposition |
|------------------|--------------------|-------------|
| `../architecture/TRONIXMESH-DESIGN-DOCTRINE.md` (trust stack, fail-closed, human sovereignty) | None — this directive is a strict application | Consistent |
| `../architecture/TRONIXMESH-ARCHITECTURE-v2.md` (governance state machine, Decision Tokens, RR-0056) | "Alive" execution requires Decision Tokens; Phase B uses bootstrap grants | Cutover scope must state token vs bootstrap-grant posture for in-scope classes |
| `../architecture/PHASE-B-SLICE.md` ("soft-launch / production deploy … staged rollout"; Decision Tokens deferred to Phase C) | This directive drives a production cutover using Phase B primitives | **Flag for Chairman:** confirm whether cutover is authorized on Phase B bootstrap-grant authority or requires the Phase C Decision-Token path |
| `../phase-b/GATE-0-AUTHORIZATION.md` | Gate 0 authorized coding/T0, not production cutover | Production cutover is a new gate beyond Gate 0; requires its own authorization |
| `../cognitive-mesh/` (Directive v0.9, Substrate v0.2) | Cognition must stay off critical path | Consistent — §7/§8 keep Track B non-blocking |

### 11.3 Canonical Manifest entry (after Chairman lock)

1. Hash the final directive (SHA-256 over approved bytes).
2. Enter version + hash into the Canonical Manifest.
3. Assign its authority tier.
4. Mark superseded subordinate clauses (per §11.1).
5. Record effective epoch / time.

Until all five complete, this directive remains **PENDING / NON-CANONICAL**. **Change control:**
amendments require Chairman approval, re-hash, and a new manifest entry; a higher normative authority
wins over this directive unless Chairman-approved change control amends it.

---

## 12. Disposition of the immediate instruction to BOB

| # | Instruction | Disposition |
|---|-------------|-------------|
| 1 | Merge patches into the consolidated Activation Directive | Done — Patches 1–8 merged (§2–§9) |
| 2 | Create the supersession matrix | Done — §11.1 (in-repo) + external-artifact list pending access |
| 3 | Inspect Canonical Manifest & locked artifacts for conflicts | In-repo done (§11.2); BOB-system artifacts **pending access** — not assumed covered |
| 4 | Return proposed `TRONIXMESH_ACTIVATION_DIRECTIVE_v1.0.md` | This document |
| 5 | Mark PENDING CHAIRMAN LOCK | Done — header + §11.3 |
| 6 | Repository/implementation inventory (Section 22) | Done — §10, evidence-based |
| 7 | Support every COMPLETE claim with commit/test/runtime evidence | Done — §10 legend; only `VERIFIED` rows claim completeness |

**Constraints honored:** no new implementation begun; operational components not re-specified; unverified
components not claimed complete; **no duration estimate**; Cognitive Mesh experimentation kept **off** the
production critical path.

---

*End of TronixMesh Activation Directive v1.0 — PENDING CHAIRMAN LOCK.*
