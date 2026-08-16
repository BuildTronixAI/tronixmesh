# Epistemic Substrate Spec v0.1 — Review Record

**Artifact ID:** `TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1_REVIEW`
**Document type:** Specification review (findings, severities, disposition, downstream gates)
**Status:** **Closed** — findings carried into [`TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md`](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md)
**Reviews:** [`TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1.md`](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1.md) (superseded)
**Recorded in-repo:** 2026-08-15
**Related:** [`README.md`](./README.md) · [`TRONIXMESH_COGNITIVE_ARCHITECTURE_DIRECTIVE_v0.9.md`](./TRONIXMESH_COGNITIVE_ARCHITECTURE_DIRECTIVE_v0.9.md)

---

## 0. Verdict

The **concept is strong**; the **v0.1 specification is not safe to implement**. v0.1 mixed three
categories as though software can treat them equivalently — things a computer can (1) prove
deterministically, (2) estimate probabilistically, (3) cannot know without trusting something external.
Blocking contradictions and two incorrect core numeric mechanisms mean two conforming implementations
could legally behave differently, which falsifies v0.1's own claim that state transitions are
deterministic.

**Disposition:** all findings are resolved in **v0.2**. This record preserves the *why* and defines the
**downstream gate**: the state-space and confidence-arithmetic findings must land before the
Reconciliation Protocol is drafted (they change what the protocol would encode).

Severity legend: **Blocking** (spec is internally inconsistent / computes the wrong thing) ·
**High** (unsound or unimplementable as written) · **Medium** (correctness/robustness) ·
**Low** (clarity / hygiene).

---

## 1. What the spec gets right (do not sand these off)

The repair must preserve the genuinely good decisions. These survive the review intact and are retained
in v0.2:

- **`UNKNOWN` is first-class and non-collapsible** — not silently coerced to 0.5.
- **Governance / observation decoupling as intent** — the system may believe "X maximizes revenue" while
  X is prohibited; governance constrains action, not observation.
- **Prediction-driven calibration** — beliefs must face reality through checkable predictions.
- **Evidence lineage matters more than model count** — correlated agreement is not independent
  confirmation.
- **Evidence is preserved; belief revisions are auditable.**
- **Execution consumes epistemic state but remains constitutionally governed.**

The errors below come mainly from trying to turn epistemology into deterministic database semantics too
early — not from the underlying architecture.

---

## 2. Findings (chat review) — severity, fix, gate

Labels match the disposition table in `..._v0.2.md` §16.

### R1 — Governance gates belief commit (contradicts the spec's own principle) · **Blocking**

v0.1 required "governance not breached" to commit to CURRENT_STATE while §10 mandated that
governance-contradicting beliefs remain accepted — the exact "contaminating epistemic state" failure it
prohibits. The same semantics appear a third time as a quarantine trigger.

**Fix.** Governance gates only the **execution** boundary. Strike governance from belief-commit
conditions and from quarantine triggers entirely. Quarantine fires only when the *process* tries to
mutate, reinterpret, or execute around governance. → v0.2 §11, invariant `G1`.

### R2 — State machine and status enum disagree; transitions not total · **Blocking**

The enum and the diagram describe different state spaces; `PROPOSED`/`UNKNOWN` appear in one but not the
other; several transitions (exit from `QUARANTINED`/`REJECTED`, `PROPOSED→CONTESTED`) are undefined.

**Fix.** Split status into four orthogonal dimensions and make outcome assignment a **total** function.
→ v0.2 §9.1 (epistemic/admission/integrity/lifecycle), §9.2 total outcome set, invariant `T1`.

### R3 — Threshold bands inconsistent; a dead zone · **Blocking**

`contested = 0.40–0.60` in one place, `0.40–0.70` in another, and the contested transition also required
contradiction — so a 0.65 claim with no contradictions matched **no** rule and was stuck in `PROPOSED`
forever. Not total over the input space.

**Fix.** Contestation is a **graph property** (an unresolved materially-incompatible active path), not a
confidence band. Confidence is carried *alongside* status. The dead zone disappears. → v0.2 §9.1.

### R4 — Dependence discount computes the wrong thing · **Blocking**

`adjusted_posterior = posterior × (1 − discount)`. Counterexample: prior `0.60`, fully redundant
evidence (`d = 1`) → `0`. Redundant evidence should leave you **at your prior**, not certain the claim is
false. Also, "aggregated dependence" was arithmetic on an undefined quantity.

**Fix — corrected log-odds form.** Dampen the *evidence weight* (the likelihood ratio) toward 1, then
update:

```
odds form:      posterior_odds = prior_odds × LR^(1 − d)
log-odds form:  logit(posterior) = logit(prior) + (1 − d) · log(LR)

d = 0  → full update (LR^1)
d = 1  → LR^0 = 1 → posterior_odds = prior_odds → posterior = prior   (0.60 → 0.60)
```

Worked check: prior `0.60` (odds `1.5`), `LR = 4`. Independent (`d=0`): odds `6.0` → `0.857`. Fully
redundant (`d=1`): odds `1.5` → `0.60` (unchanged). Half-dependent (`d=0.5`): odds `1.5 × 4^0.5 = 3.0` →
`0.75`. Dependence is an **assessment**, and a numeric `d` exists only when a defined estimator produced
it. → v0.2 §8.2, §7.3.

### R5 — `calibration_score` is accuracy, not calibration · **High**

`P(correct | domain, task)` rewards confident guessers (0.99-on-everything, right 80% → scores 0.80).
`sample_count ≥ 3` to publish is noise.

**Fix.** Store confidence-conditional metrics — Brier, reliability/calibration error, confidence bins,
resolution/discrimination, uncertainty interval, scoring-rule version — per **cognitive-process-version**.
Downstream consumers use **shrinkage** toward a conservative prior and the **CI lower bound**, not a
point estimate; no magic sample-count threshold. → v0.2 §12.

### R6 — Mandatory six-float dependency nobody can produce · **High**

v0.1 made a six-float `dependency_classification` MANDATORY while conceding dependency measurement is
unsolved — false precision laundered through schema.

**Fix.** Dependence is an assessment `{class: LOW|MODERATE|HIGH|UNKNOWN, estimate: float|null, interval,
evidence_basis, estimator_version}`; numbers exist only from a defined estimator. → v0.2 §7.3.

### R7 — Prediction-pending deadlock · **High**

"Every accepted claim spawns a prediction" + "block mutation while a prediction is pending" compose into
a months-long freeze regardless of new evidence.

**Fix.** No commit-freeze on pending predictions; invalidated commits are **re-evaluated forward** from
the log. → v0.2 §9.4.

### R8 — Mutable evidence vs. append-only audit chain · **High**

`mutable_fields` with in-place `revision_history` breaks RR-0056 tamper-evidence, and cache invalidation
of citing claims was unspecified.

**Fix — supersedes pattern.** Evidence is immutable. A correction is a **new** evidence object that
references its predecessor; the chain includes both; citing claims are flagged for re-evaluation:

```
ev_old  (immutable, hash-chained)
   ▲  supersedes
ev_new  { ..., "supersedes": "ev_old", "content_hash": "sha256:…", "ledger_sequence": n }
   │
   └── on append: all claims whose relation-closure cites ev_old → marked for re-evaluation;
       CURRENT_STATE recomputes forward (never restores a snapshot)
```

→ v0.2 §5 (invariant `E1`), §9.4.

### R9 — "Rollback" isn't rollback · **Medium**

The WAL carried `prior_belief_state` snapshots and a `rolled_back` status, but the process recomputed
forward (correct epistemics) — so the vocabulary invited implementers to build snapshot restoration.

**Fix.** Rename to **re-evaluation**; delete snapshot-restore implication and the `rolled_back` status.
→ v0.2 §9.4.

### R10 — Normative claims are schema'd but unhandled · **High** *(gates Reconciliation)*

`claim_type` included "preference," yet nothing in confidence/prediction/calibration applies to
non-factual claims. §10's defense works for descriptive beliefs ("X would maximize revenue") but is
shaky for "we should do X" sitting accepted in CURRENT_STATE.

**Fix.** Split claims into FORMAL / SEMANTIC / **NORMATIVE**; normative claims are authenticated and
attributed but receive **no** confidence, prediction, or calibration and never sit as Bayesian-true.
→ v0.2 §6.3.

---

## 3. Additional structural findings — severity, fix

Labels match `..._v0.2.md` §16 (`S#`).

| # | Finding | Severity | Fix (v0.2) |
|---|---------|----------|------------|
| S1 | `status` overloads epistemic / admission / integrity / lifecycle | **Blocking** | Four orthogonal dimensions — §9.1 |
| S2 | `UNKNOWN` cannot be both a number and a state | **Blocking** | Confidence `{status: ESTIMATED\|UNAVAILABLE, …}`; UNKNOWN ≠ 0.5 — §8.1 |
| S3 | "Contested" as a confidence band | **Blocking** | Contestation defined on the graph — §9.1 |
| S4 | Dual authority (evidence↔claim each store relations) | **High** | Immutable relation edges; both sides derived — §7.1 |
| S5 | "Machine-readable" claim with nullable formal representation | **High** | FORMAL (deterministic) vs SEMANTIC (estimated) — §6.1/§6.2 |
| S6 | A record authenticates data, not reality | **High** | `CR-1`; integrity vs content — §1, §4.1 |
| S7 | `source_identity: string` is security theater | **High** | Credential binding + registry verification — §4.1 |
| S8 | Timestamps overtrusted (`ts ≤ admitted_at` "proves" ordering) | **Medium** | Three clocks; order from `ledger_sequence` — §4.3 |
| S9 | WAL is not a transactional guarantee; concurrent split-brain | **High** | Serializable CAS (`expected`/`new` version); one writer/partition — §3.1 |
| S10 | Append-only ≠ tamper-proof | **Medium** | Layered external anchoring; "tamper-evident" — §4.2 |
| S11 | Model independence can't be known precisely | **High** | Dependence assessment; estimator-gated numbers — §7.3 |
| S12 | Model-generated confidence is false metrology | **High** | Method provenance or `UNAVAILABLE` — §8.1/§8.3, `K1` |
| S13 | Bayes assumed universally available | **High** | Registered confidence methods; Bayes is one — §8.3 |
| S14 | `min_evidence = 2` is epistemically unsound | **Medium** | Claim-class evidence policy on independent weight — §13 |
| S15 | `REJECTED` swallows `UNKNOWN` (absence → false) | **High** | Absence → `UNDERDETERMINED`; `REFUTED` needs negation evidence — §9.1 |
| S16 | Dependency graphs need cycle semantics (self-confirmation) | **High** | DAG + SCC detection; no self-confirming inference — §7.2 |
| S17 | Predictions need pre-registration (anti-gaming) | **High** | Frozen, signed; resolver ≠ predictor — §10.1 |
| S18 | Observation failure ≠ prediction failure | **High** | Channel coverage; `UNRESOLVABLE` — §10.2 |
| S19 | Calibration needs process-version identity | **Medium** | `process_version_id` bundle — §12.1 |

Minor / hygiene: wrong cross-reference ("Section 3" → §10); "should" used inside an invariant (invariants
are MUST); missing `UNBOUND` evidence state; escalation deadlines with no fail-open/closed default;
three inconsistent match-quality representations on one object; and WMD/intelligence examples — all
addressed in v0.2 (§9.3 escalation default, §5 `UNBOUND`, §14 MUST-only, construction/finance examples).

---

## 4. The two constitutional additions

The review's deepest point is that the substrate should stop pretending model consensus equals truth.
Two rules bulletproof the design and are carried into the Directive (§1.3) and the substrate (§1.1):

> **CR-1.** Cryptographic integrity, provenance, consensus, repetition, model agreement, or schema
> validity SHALL NOT be interpreted as proof that an external-world assertion is true.

> **CR-2.** Every epistemic conclusion SHALL expose the trust assumptions, inference method, unresolved
> uncertainty, and evidence lineage upon which it depends.

---

## 5. Disposition and downstream gates

All findings are **Resolved in v0.2**. The gate column records which downstream artifact a finding must
precede — because it changes the structures that artifact would encode.

| Finding(s) | Status | Must land **before** |
|------------|--------|----------------------|
| **R1, R2, R3, R4, R10** | Resolved (v0.2) | **Reconciliation Protocol spec** — they define the state space (R1/R2/R3/R10) and confidence arithmetic (R4) the protocol encodes |
| S1, S2, S3, S4, S15, S16 | Resolved (v0.2) | **Reconciliation Protocol spec** — same reason: they redefine the status model / belief graph the protocol operates over |
| R5, R6, R7, R8, R9, remaining S# | Resolved (v0.2) | v0 experiment / implementation |

**Gate status:** the blocking set (**R1–R4, R10**, plus the state-space structural findings) has landed
in **v0.2**. The Reconciliation Protocol spec may therefore be drafted **against v0.2 only** — never on
top of v0.1.

> **Do not draft the Reconciliation Protocol on v0.1.** Its state space and confidence arithmetic are
> exactly what these findings change.

---

## 6. Bottom line

- v0.1 concept: **strong**.
- v0.1 mathematics: **not safe** (R4, R5).
- v0.1 state semantics: **internally contradictory** (R1–R3, S1–S3).
- v0.1 audit/security model: **directionally right but underspecified** (R8, S6–S11).
- v0.1 claim of "machine-readable and implementation-testable": **false as written** (S5).

No fatal flaw in the architecture itself. One serious specification pass — delivered as **v0.2** — makes
the substrate internally total, mathematically coherent, trust-boundary-explicit, and mechanically
testable, which is the prerequisite for reconciliation.

---

*End of Epistemic Substrate Spec v0.1 Review Record.*
