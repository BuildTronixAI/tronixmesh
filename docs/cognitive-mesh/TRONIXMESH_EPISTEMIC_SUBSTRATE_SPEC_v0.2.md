# TronixMesh Epistemic Substrate Spec

**Artifact ID:** `TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2`
**Document type:** Specification (schema-level)
**Status:** **v0.2 — ACTIVE BUILD TARGET** (pre-normative; canonicalization gated with the Directive)
**Supersedes:** [`TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1.md`](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1.md) (retained for history)
**Authority:** Christopher C. Leiser, Chairman (direction approved)
**Recorded in-repo:** 2026-08-15
**Scope:** Defines the epistemic machinery and its trust boundaries. It does **not** define the
reconciliation protocol (still the next artifact, now gated on this v0.2), delegation mechanics
(Directive §5), or any governance change.
**Related:** [`TRONIXMESH_COGNITIVE_ARCHITECTURE_DIRECTIVE_v0.9.md`](./TRONIXMESH_COGNITIVE_ARCHITECTURE_DIRECTIVE_v0.9.md) · [`README.md`](./README.md) · [`../architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../architecture/TRONIXMESH-DESIGN-DOCTRINE.md) · [`../phase-b/adr/0001-proof-native-envelopes.md`](../phase-b/adr/0001-proof-native-envelopes.md)

---

## 0. Why v0.2 exists (the reframed claim)

v0.1 tried to make **epistemic truth** behave like deterministic database semantics. That claim is not
achievable and, worse, it hid three fundamentally different categories inside one data model:

1. things a computer can **prove deterministically**,
2. things a computer can **estimate probabilistically**,
3. things a computer **cannot know** without trusting something outside itself.

v0.2 abandons the false claim and adopts a narrower, defensible one:

> The substrate does not make epistemic truth deterministic. It makes epistemic **processing**
> **accountable, bounded, reproducible, corrigible, and tamper-evident** — and it labels, for every
> conclusion, which of the three categories above it belongs to.

Everything below is organized so that a conforming implementation is *total* (every input has a defined
outcome), *coherent* (no rule contradicts another), *trust-boundary-explicit* (digital fact is never
silently promoted to external truth), and *mechanically testable*.

This version is written against construction / finance / industrial examples on purpose (e.g. a pump
pressure reading, a project schedule variance). Do not use WMD/intelligence examples in this document.

---

## 1. Epistemic honesty: the three categories and the constitutional rules

Every quantity, relation, and status in this spec is tagged with the category of knowledge it represents:

| Category | Tag | Meaning | Examples |
|----------|-----|---------|----------|
| Digitally guaranteed | `DIGITAL` | Provable inside the trusted digital substrate | schema validity, signature verification, content hash equality, ledger ordering, deterministic contradiction among **formal** claims, audit replay |
| Estimated | `ESTIMATED` | Producible only as a probabilistic estimate by a defined procedure | source reliability, semantic contradiction, likely truth of an empirical claim, model dependence, prediction reliability |
| Fundamentally unknowable to the substrate alone | `UNKNOWABLE` | Requires trusting something outside the substrate | whether a human told the truth, whether a sensor measured the correct physical thing, a proprietary model's true training lineage, that all relevant evidence has been discovered |

### 1.1 Constitutional rules (normative once this area is canonical)

> **CR-1 (Digital ≠ external truth).** TronixMesh SHALL distinguish facts established by the trusted
> digital substrate from assertions about the external world. Cryptographic integrity, provenance,
> consensus, repetition, model agreement, or schema validity SHALL NOT be interpreted as proof that an
> external-world assertion is true.

> **CR-2 (Exposed assumptions).** Every epistemic conclusion SHALL expose the trust assumptions,
> inference method, unresolved uncertainty, and evidence lineage upon which it depends.

These are the load-bearing invariants of the whole substrate; all schemas below carry the fields needed
to satisfy them.

---

## 2. The five separations (design axioms)

v0.2 is built on five separations that v0.1 conflated. Each dissolves a class of the reported bugs.

| # | Separation | Consequence |
|---|------------|-------------|
| A1 | **Truth state ≠ admission state ≠ integrity/quarantine state ≠ lifecycle state** | Status is four orthogonal dimensions (§8), not one overloaded enum |
| A2 | **Observation/evidence ≠ claim/inference ≠ normative preference** | Preferences leave the truth-confidence calculus entirely (§6.3) |
| A3 | **Digitally verified fact ≠ externally asserted fact** | Integrity is `DIGITAL`; content truth is `ESTIMATED`/`UNKNOWABLE` (§1, §4) |
| A4 | **Probability estimate ≠ UNKNOWN** | Confidence has an explicit `UNAVAILABLE` status; `UNKNOWN` is never encoded as 0.5 (§7) |
| A5 | **Epistemic acceptance ≠ execution authorization** | Governance constrains action, not observation (§11); belief commit never depends on governance |

---

## 3. Authoritative store vs. derived view

**The immutable evidence/relation/transition log is authoritative. CURRENT_STATE is a derived,
reproducible materialized view of that log.** If CURRENT_STATE is lost or suspect, it is discarded and
rebuilt by deterministic replay. CURRENT_STATE is never a second source of truth.

```
AUTHORITATIVE (append-only, hash-chained)          DERIVED (rebuildable)
┌───────────────────────────────────────┐          ┌────────────────────────┐
│ EVIDENCE objects        (§4)           │          │ CURRENT_STATE          │
│ RELATION edges          (§5)           │  fold →  │  = belief graph        │
│ TRANSITION log          (§9)           │          │  materialized view     │
│ PREDICTION registrations(§10)          │          │  (throw away & rebuild)│
│ OBSERVATIONS            (§10)          │          └────────────────────────┘
│ CALIBRATION ledger      (§12)          │
└───────────────────────────────────────┘
```

- **Invariant V1 (Reproducibility).** `CURRENT_STATE = fold(deterministic_reducer, authoritative_log)`.
  Given the same log and the same reducer version, the materialized view is bit-for-bit identical.
- **Invariant V2 (No canon in the view).** CURRENT_STATE holds beliefs only. Schema, rules,
  reconciliation protocol, admissibility, and authority live in the canonical manifest (Directive §3).
- **Invariant V3 (Reducer versioning).** The reducer carries a `reducer_version`; a rebuild records
  which version produced the view, so historical views are reconstructable.

### 3.1 Concurrency (compare-and-swap; no split brain)

CURRENT_STATE mutation is not implied by "write to the WAL." It requires an explicit, serializable
commit:

- Every transition (§9) carries `expected_state_version` and `new_state_version` for its target
  partition.
- The commit is a **serializable compare-and-swap**: it applies only if the target's current version
  equals `expected_state_version`; otherwise the transition is `REJECTED` with reason
  `VERSION_CONFLICT` and must be re-proposed against the new version.
- There is **one authoritative writer per claim partition** (or an explicit consensus protocol); two
  reconcilers may not both advance the same claim from the same version.
- WAL entries are not committed facts. A crash between `pending_commit` and the CAS success leaves the
  transition *uncommitted*; recovery replays the authoritative log, never a half-applied view.

---

## 4. Identity, integrity, and time

### 4.1 Source identity is a credential binding, not a string

A `source_identity: string` is security theater — anyone who can write a record can write
`"trusted_sensor_04"`. Identity is a verifiable binding:

```json
{
  "principal_id": "prn_...",
  "credential_id": "cred_...",
  "signature": "…",
  "signature_algorithm": "ed25519 | ecdsa-p256 | …",
  "attestation_chain": ["…"],
  "key_epoch": 3
}
```

Admission verifies the credential against the identity registry. Note the boundary (`CR-1`): a verified
credential proves **possession of a key**, not real-world honesty. It is `DIGITAL` that sensor_04's key
signed these bytes; it is `UNKNOWABLE` from the substrate alone that the physical pressure was truly
92 psi.

### 4.2 Integrity is tamper-evident, not tamper-proof

The authoritative log is hash-chained (RR-0056 direction) and layered:

```
immutable event records → hash chain → signed checkpoints
→ checkpoint anchored outside the primary trust domain → independent WORM/backup
```

Rewriting history then requires compromising multiple independent domains. The spec uses the phrase
**tamper-evident**; it never claims metaphysical immutability. If one administrator controls database,
audit store, keys, and backups, history can be rewritten — a stated `UNKNOWABLE` boundary, not a defect.

### 4.3 Time semantics (three clocks, one order)

A single `timestamp` cannot prove "created before admission." v0.2 records:

| Field | Category | Meaning |
|-------|----------|---------|
| `source_claimed_time` | `ESTIMATED`/`UNKNOWABLE` | When the source says the event occurred |
| `system_received_time` | `DIGITAL` (local) | When TronixMesh received it |
| `ledger_sequence` | `DIGITAL` | Total order **inside** TronixMesh |
| `trusted_timestamp_attestation` | `DIGITAL` (if present) | External RFC-3161-style attestation, where available |

Ordering and "happened-before" **inside** the substrate derive from `ledger_sequence`, never from wall
clocks. The substrate does not claim to know exactly when an external physical event occurred.

---

## 5. Evidence object

Evidence records *what was received/observed*. It is immutable and append-only.

```json
{
  "id": "ev_...",
  "kind": "observation | retrieval | model_output | solver_result | sensor | human | simulation",
  "channel_id": "chan_...",
  "identity": { "…": "credential binding, §4.1" },
  "asserted_content": { "…": "channel-specific payload (an assertion about the world)" },
  "content_hash": "sha256:…",
  "integrity": { "verified": true, "category": "DIGITAL" },
  "produced_by": "loop_...",
  "time": { "source_claimed_time": "…", "system_received_time": "…", "ledger_sequence": 100421 },
  "dependence": { "…": "assessment, §6.2" },
  "binding_status": "BOUND | UNBOUND",
  "supersedes": "ev_… | null",
  "provenance_ref": "prov_…"
}
```

- **Integrity vs content (`CR-1`).** `integrity` is a `DIGITAL` fact about the bytes. `asserted_content`
  is an assertion about the world and is never promoted to truth by integrity alone.
- **Append-only revisions.** Evidence is never edited in place. A correction is a **new** evidence object
  with `supersedes` pointing at its predecessor, preserving the hash chain (fixes v0.1 mutable-fields vs
  audit-chain conflict). Claims citing a superseded evidence object are flagged for re-evaluation (§9.4).
- **UNBOUND evidence.** Evidence may be admitted `UNBOUND` — not yet mapped to any claim — so anomalous
  raw observations can be stored for later claim-mining. (Removes v0.1's invariant that forbade storing
  unmapped observations.)

**Invariant E1.** Evidence objects are immutable; the only "change" is a superseding append.

---

## 6. Claims: three kinds, three treatments

"Machine-readable" is only real if the machine can compute the claim's meaning. v0.2 splits claims:

### 6.1 FORMAL claim

A typed predicate with defined semantics; contradiction/support among formal claims is a `DIGITAL`
computation.

```json
{
  "id": "cl_...",
  "class": "FORMAL",
  "predicate": "schedule_variance_days(project_123) > 30",
  "ontology_ref": "ont_...",
  "derived_from": ["rel_…"],
  "content_hash": "sha256:…"
}
```

- Contradiction detection between formal claims is deterministic given the predicate algebra and known
  facts (e.g. `x > 30` contradicts `x <= 10`). This is the only place "deterministic contradiction" is
  claimed.

### 6.2 SEMANTIC claim

A natural-language assertion. Support/contradiction is **model-estimated** and must carry provenance.

```json
{
  "id": "cl_...",
  "class": "SEMANTIC",
  "statement": "The project is substantially behind schedule.",
  "relation_estimates_are": "ESTIMATED",
  "content_hash": "sha256:…"
}
```

- A machine can store `"The project is substantially behind schedule"`, but it cannot *prove* whether
  that contradicts `"Project schedule remains recoverable."` — an LLM can only **estimate** it. Every
  such relation is `ESTIMATED` and carries `{estimator, method, model_version, confidence, review_status}`
  (§7). Never pretend a semantic relation is `DIGITAL`.

### 6.3 NORMATIVE / PREFERENCE claim (outside the truth calculus)

A preference or normative assertion — e.g. `"We should accelerate procurement despite budget policy."`

```json
{
  "id": "cl_...",
  "class": "NORMATIVE",
  "assertion": "We should accelerate procurement despite budget policy.",
  "asserted_by": "prn_...",
  "authority_basis": "…",
  "content_hash": "sha256:…"
}
```

- Normative claims are **authenticated and attributed** but receive **no confidence, no prediction, and
  no calibration** — there is no ground truth or observable to calibrate against. They may inform action
  (through governance), but they never sit in CURRENT_STATE as if Bayesian-true. (Resolves the v0.1
  "preference in the truth calculus" gap and the shaky "we should do X" case.)

**Invariant C1.** A `FORMAL`/`SEMANTIC` claim's relation closure (§5→§7) must terminate in admissible
evidence; an unevidenced factual claim is a *hypothesis*, not a claim. `NORMATIVE` claims are exempt from
the evidence-closure requirement but must carry an attributed `asserted_by`.

---

## 7. Relations (single source of truth) and dependence

### 7.1 Immutable relation edges

Evidence and claims do **not** each store their own copies of who-supports-whom (that dual authority
lets `E-12` claim it supports `C-8` while `C-8` disagrees). Instead, relations are **immutable edges**,
and both sides are *derived* from them.

```json
{
  "relation_id": "rel_...",
  "source": "ev_… | cl_...",
  "target": "cl_...",
  "relation_type": "SUPPORTS | CONTRADICTS | DERIVES_FROM | ASSUMES | USES_METHOD",
  "strength": 0.0,
  "category": "DIGITAL | ESTIMATED",
  "method": "confidence-method-id, §8.3",
  "estimator": "prn_… | null",
  "estimator_version": "process-version-id, §12.1 | null",
  "created_by": "loop_...",
  "ledger_sequence": 100422,
  "signature": "…"
}
```

- For `FORMAL↔FORMAL`, `category = DIGITAL`. For anything involving a `SEMANTIC` claim,
  `category = ESTIMATED` and `estimator`/`estimator_version` are required.
- The same normalization applies to predictions/observations (§10): one authoritative edge, both sides
  derived — never three copies of the result.

### 7.2 Cycles and epistemic laundering

- **Invariant D1 (DAG).** `DERIVES_FROM`/`ASSUMES`/`USES_METHOD` form a DAG. Cycle detection runs on
  every proposed edge; strongly-connected components are rejected.
- **Invariant D2 (No self-confirmation).** A derived inference MUST NOT increase confidence in an
  ancestor it (transitively) depends on. Evidence lineage is traversed; a result that "returns through
  another model" to its own ancestor is inadmissible as new support.

### 7.3 Dependence / independence (estimated, never fabricated precision)

True causal dependence between opaque models (shared corpora, RLHF overlap, provider routing,
post-training lineage) is `UNKNOWABLE` to six decimals. So dependence is an **assessment**, not a bare
float:

```json
{
  "class": "LOW | MODERATE | HIGH | UNKNOWN",
  "estimate": 0.0,
  "interval": { "low": 0.0, "high": 0.0 },
  "evidence_basis": ["…"],
  "estimator_version": "…"
}
```

A numeric `estimate` exists **only** when produced by a defined estimator; otherwise `class` carries the
information and `estimate` is `null`. (Removes v0.1's mandatory six-float dependency vector — false
precision — and the undefined "aggregated_dependence" quantity.)

---

## 8. Confidence semantics

### 8.1 Confidence is a structured object, not a bare float

`UNKNOWN` is a *state*, not the number 0.5. 0.5 means "my model puts equal posterior on true/false";
`UNAVAILABLE` means "I cannot responsibly assign a probability."

```json
{
  "status": "ESTIMATED | UNAVAILABLE",
  "point_estimate": 0.0,
  "interval": { "low": 0.0, "high": 0.0 },
  "method": "BAYESIAN_LR | FREQUENTIST_ESTIMATE | EMPIRICAL_CALIBRATION | DETERMINISTIC | EXPERT_ASSESSMENT | QUALITATIVE | UNAVAILABLE",
  "model_version": "process-version-id, §12.1 | null",
  "scoring_rule_version": "…",
  "computed_at": "…"
}
```

- **When `status = UNAVAILABLE`**, `point_estimate` and `interval` are `null`. Fail-closed handling
  treats `UNAVAILABLE` as "not established," never as 0.5.
- **Method provenance (`CR-2`).** Every confidence records the reproducible procedure that produced it.
  A number with no method is not admissible; use `UNAVAILABLE`. An LLM emitting `0.72` with no calibrated
  procedure is `QUALITATIVE` at best and should usually be `UNAVAILABLE`.

### 8.2 Correct dependence-aware update

Dependence dampens the **evidence weight**, it does not multiply the posterior. For a Bayesian update
with likelihood ratio `LR` and dependence `d ∈ [0,1]`:

```
LR_effective = LR^(1 − d)
posterior_odds = prior_odds × LR_effective
```

- At `d = 0` (independent): `LR_effective = LR` (full update).
- At `d = 1` (fully redundant): `LR_effective = 1` → **posterior returns to the prior** (redundant
  evidence adds nothing), instead of v0.1's `posterior × (1 − d)` which drove belief toward *false*.
- Correlated sources are grouped by dependence assessment (§7.3) and updated once per group, not once per
  member. Adding a correlated source never inflates confidence as if independent.

### 8.3 Confidence methods are registered, Bayes is not universal

`P(E|H)` and `P(E|¬H)` are usually unknown for arbitrary real-world evidence; an LLM fabricating both
yields "mathematically precise nonsense." Bayes is therefore **one registered method**, not the default.
Every confidence names its `method` (enum in §8.1); `DETERMINISTIC` is reserved for `DIGITAL` relations
(e.g. formal contradiction), and `UNAVAILABLE` is always a legal outcome.

---

## 9. Status model and belief-state transitions

### 9.1 Four orthogonal status dimensions (total assignment)

Status is not one enum. It is four independent dimensions, each a **total function** of the
authoritative log:

```
epistemic_status:  SUPPORTED | REFUTED | UNDERDETERMINED | CONTESTED
admission_status:  PROPOSED  | ADMITTED | INADMISSIBLE
integrity_status:  VERIFIED  | DEGRADED | QUARANTINED
lifecycle_status:  ACTIVE    | SUPERSEDED | RETIRED
```

A claim can be, e.g., *epistemically SUPPORTED but integrity QUARANTINED* (evidence chain failed
verification), or *UNDERDETERMINED but ADMITTED*. These no longer fight for one variable.

Assignment rules (total; no dead zone):

- **`epistemic_status`** is derived from the relation graph and confidence, **not** from a confidence
  band:
  - `CONTESTED` ⇔ there exists a **materially incompatible, active** claim/evidence path that is
    unresolved under the reconciliation rules. *Contestation is a graph property, not an interval.*
  - `REFUTED` ⇔ admissible evidence supports the **negation**. Absence of support is **never** `REFUTED`.
  - `UNDERDETERMINED` ⇔ insufficient admissible evidence to support or refute (this is the home of
    "not enough evidence," replacing v0.1's rule that swallowed it into `REJECTED`).
  - `SUPPORTED` ⇔ net admissible support, no unresolved material contradiction.
  - Confidence (§8) is carried **alongside** epistemic_status, not used to define it. A 0.65 claim with
    no contradiction is `SUPPORTED` with a mid interval — never stuck.
- **`admission_status`**: `INADMISSIBLE` is the home of "rejected because it violates admissibility"
  (bad credential, DAG violation, missing method). It is distinct from `REFUTED` (probably false).
- **`integrity_status`**: `QUARANTINED` is a **trust/control** condition (process fault, integrity
  failure, or an attempt to mutate/reinterpret/bypass governance — Directive §4). It is **never** set
  because a valid belief's implications conflict with policy.
- **`lifecycle_status`**: `SUPERSEDED`/`RETIRED` retain history without deletion.

### 9.2 Transition object (interface to reconciliation)

Loops propose transitions; they never write CURRENT_STATE directly (Directive §5). The reconciliation
protocol (next artifact) decides each proposal. v0.2 defines only the interface and its totality.

```json
{
  "id": "txn_...",
  "proposed_by": "loop_...",
  "op": "ADMIT_EVIDENCE | ADD_RELATION | ADD_CLAIM | RECOMPUTE_CONFIDENCE | SET_EPISTEMIC | SET_INTEGRITY | SUPERSEDE | RETIRE",
  "target": "cl_… | belief_… | ev_…",
  "expected_state_version": 7,
  "new_state_version": 8,
  "delta": { "…": "op-specific" },
  "justification": "…",
  "ledger_sequence": 100430
}
```

Every proposal maps to exactly one **outcome**, and the outcome set is total over the input space:

| Outcome | When |
|---------|------|
| `ACCEPTED` | Admissible, CAS matches, invariants preserved → applied and logged |
| `REJECTED` | Inadmissible (bad credential, DAG/cycle violation, `VERSION_CONFLICT`, missing required method) → logged with reason; sets `admission_status = INADMISSIBLE` where applicable |
| `QUARANTINED` | Integrity/process fault or governance-boundary tampering → `integrity_status = QUARANTINED` |
| `ABSTAINED` | Insufficient basis to decide → target remains/So becomes `UNDERDETERMINED`; no state change |
| `ESCALATED` | Referred upward per authority structure (§9.3) |

- **Invariant T1 (Totality).** The decision function is total: every well-formed transition yields
  exactly one outcome. Malformed transitions are `REJECTED` (never undefined).
- **Invariant T2 (Determinism of *process*, not truth).** Given the same authoritative log, reducer
  version, and reconciliation-rule version, the *outcome and resulting view are reproducible*. This is a
  claim about process, not about the truth of the underlying belief.
- **Invariant T3 (Log-then-commit).** Each proposal produces exactly one append-only transition-log
  entry `{txn_id, outcome, reason, decided_by, decided_at, expected_state_version, applied_version}`.
  CURRENT_STATE changes only on `ACCEPTED` via the §3.1 CAS.

### 9.3 Escalation has a mandatory default disposition

For a governance substrate, "no human answered" cannot be undefined. Every escalation carries:

```json
{ "deadline": "…", "on_timeout": "FAIL_CLOSED | HOLD_UNDERDETERMINED", "notified": ["prn_…"] }
```

- `on_timeout` MUST be set. Default is `FAIL_CLOSED` (consistent with the runtime's fail-closed
  doctrine): on no response the transition does not apply and the target is held `UNDERDETERMINED`, with
  mandatory notification. (Closes the v0.1 gap of escalation deadlines with no default.)

### 9.4 Re-evaluation, not rollback

There is no snapshot restoration. When a commit is invalidated (e.g. a cited evidence object is
superseded, §5), the affected claims are flagged and the view is **recomputed forward** from the
authoritative log — you never restore a stale belief. The vocabulary is **re-evaluation**; the word
"rollback" and any `rolled_back` status are removed to prevent implementers building snapshot restore.

---

## 10. Predictions and observation

### 10.1 Pre-registered, signed predictions (anti-gaming)

Prediction-driven calibration is only trustworthy if predictions are frozen before resolution. Before
the observation window opens, the following is hashed and signed and appended to the authoritative log:

```json
{
  "id": "pred_...",
  "from_belief": "belief_...",
  "proposition": "structured, adjudicable statement",
  "stated_confidence": { "…": "§8 object" },
  "observation_window": { "opens": "…", "closes": "…" },
  "observation_channel": "chan_...",
  "resolution_criteria": "exact CORRECT/INCORRECT condition",
  "resolver": "prn_…",
  "scoring_rule": "brier | log | …",
  "registration_hash": "sha256:…",
  "signature": "…"
}
```

- **Invariant P1 (Resolver independence).** `resolver` MUST NOT be the predictor. The predictor cannot
  adjudicate its own prediction.
- **Invariant P2 (Frozen criteria).** `resolution_criteria` must be precise enough to adjudicate without
  re-litigating the belief. Vague "some consistent evidence will emerge" predictions are inadmissible.

### 10.2 Observation-channel coverage (missing ≠ false)

An observation that did not occur is not disconfirmation if the channel could not have seen it. Each
resolution models detection probability:

```json
{
  "id": "obs_...",
  "resolves": "pred_...",
  "outcome": "CORRECT | INCORRECT | PARTIAL | UNRESOLVABLE",
  "detection_prob_if_event": 0.0,
  "channel_available": true,
  "evidence_ref": "ev_...",
  "ledger_sequence": 100440
}
```

- If `channel_available = false` or `detection_prob_if_event` is low, the outcome is `UNRESOLVABLE`, and
  it does **not** feed a negative calibration update. (Sensor outage, retrieval/API failure, censorship,
  or incomplete monitoring never masquerade as disconfirmation.)

---

## 11. Governance / observation / execution decoupling

Restating A5 as a hard rule the substrate enforces:

- A belief that contradicts governance is **not** inherently invalid and is **not** blocked from
  CURRENT_STATE. `"Accelerating procurement would cut cost by 12%"` may be `SUPPORTED` while the action
  is prohibited.
- **Belief commit never depends on a governance check.** Nothing in §9 gates `ACCEPTED` on "governance
  not breached." (Removes the v0.1 contradiction where §6 commit conditions and quarantine triggers
  fought §10's own principle.)
- `integrity_status = QUARANTINED` fires **only** when the *process* tries to mutate governance,
  falsely reinterpret governance, or execute around it — never for a policy-inconvenient belief.
- **Execution** consumes CURRENT_STATE but is authorized independently, through the existing governance
  state machine and Decision Token path. Epistemic acceptance ≠ execution authorization.

---

## 12. Calibration ledger

### 12.1 Calibration attaches to a cognitive-process-version, not a model name

"GPT model X has calibration 0.84" is not meaningful. The unit is the whole process:

```json
{
  "process_version_id": "pv_...",
  "model": "…",
  "model_version": "…",
  "system_prompt_hash": "sha256:…",
  "toolset_version": "…",
  "retrieval_policy": "…",
  "sampling_config": "…",
  "workflow_version": "…",
  "runtime_version": "…"
}
```

Changing any of these yields a **different** process; calibration from `pv_1` is never silently attached
to `pv_7`.

### 12.2 The ledger stores calibration, not accuracy

Accuracy (`P(correct)`) rewards confident guessers; a process that says `0.99` and is right 80% of the
time is badly miscalibrated. Each resolved, pre-registered prediction appends:

```json
{
  "id": "cal_...",
  "prediction": "pred_...",
  "observation": "obs_...",
  "process_version_id": "pv_...",
  "claim_class": "FORMAL | SEMANTIC",
  "stated_confidence": 0.0,
  "outcome_correct": true,
  "scoring_rule_version": "…",
  "ledger_sequence": 100450
}
```

Derived, versioned metrics (per `process_version_id` and per dependence group) include at least:

| Metric | Purpose |
|--------|---------|
| Brier score | Proper scoring of probabilistic predictions |
| Reliability / calibration error | Do 0.7-stated predictions resolve true ~70% of the time? |
| Confidence bins | Reliability curve inputs |
| Sample count | Volume (not a trust threshold on its own) |
| Uncertainty interval | CI around each metric |
| Resolution / discrimination | Does it separate true from false cases? |
| Scoring-rule version | Reproducibility |

### 12.3 Downstream weighting uses shrinkage, not a magic sample count

- There is **no** hard "trust at n≥10" rule. `n=3` is noise; `n=10` is better but not a threshold of
  truth. Downstream confidence weighting uses **shrinkage** toward a conservative prior and consumes the
  **CI lower bound**, not the point estimate, so trust grows smoothly with evidence.
- Calibration is tracked per dependence group so a jointly-miscalibrated correlated cluster is discounted
  as a group. (Fixes v0.1's `calibration_score = accuracy` and `sample_count ≥ 3` publish floor.)

---

## 13. Evidentiary sufficiency (no generic minimum count)

Two evidence objects are not intrinsically better than one: one signed meter reading may suffice; ten
agents repeating the same hallucination are worthless. There is **no generic `min_evidence = 2`**.
Sufficiency is a **claim-class-specific evidence policy** evaluated against *independent* evidentiary
weight (§7.3, §8.2), not a raw count. Absence of sufficient evidence yields `UNDERDETERMINED` (§9.1),
never `REFUTED`.

---

## 14. Invariants (summary; all MUST)

| ID | Invariant |
|----|-----------|
| CR-1 | Digital integrity/consensus/agreement is never proof of external-world truth |
| CR-2 | Every conclusion exposes trust assumptions, method, uncertainty, and lineage |
| V1 | CURRENT_STATE is a reproducible fold of the authoritative log |
| V2 | CURRENT_STATE holds beliefs only; no canon |
| V3 | Reducer/rule versions are recorded for reconstructable views |
| E1 | Evidence is immutable; corrections are superseding appends |
| C1 | Factual claims' relation closure terminates in admissible evidence; normative claims are attributed and excluded from the truth calculus |
| D1 | Dependency relations form a DAG (cycle detection enforced) |
| D2 | No self-confirming inference raises confidence in an ancestor |
| T1 | The transition decision function is total |
| T2 | Process (outcome + view) is reproducible; truth is not asserted deterministic |
| T3 | Exactly one append-only transition-log entry per proposal; commit only on ACCEPTED via serializable CAS |
| P1 | A prediction's resolver is not its predictor |
| P2 | Prediction criteria are frozen and adjudicable |
| G1 | Belief commit never depends on a governance check; QUARANTINE is process/integrity only |
| K1 | Every quantitative epistemic value names the reproducible procedure that produced it, or is UNAVAILABLE |

Note: this section uses MUST throughout; no invariant uses "should."

---

## 15. What is digitally possible, probabilistic, or impossible

### 15.1 Strongly possible (`DIGITAL` — make these exceptionally strong)

Schema validation; cryptographic identities; signatures; content hashing; evidence lineage; append-only
history; provenance recording; transition authorization; state-version enforcement; deterministic
contradiction for **formal** claims; write ordering in the authoritative ledger; access control;
immutable prediction registration; deterministic scoring once outcome rules are formal; audit replay;
bounded delegation; fail-closed `UNAVAILABLE` handling; governance enforcement at execution;
evidence/version preservation; reproducible deterministic computations.

### 15.2 Possible only probabilistically (`ESTIMATED` — require explicit uncertainty)

Source reliability; LLM reliability; semantic contradiction/relevance; likely truth of empirical claims;
model dependence; causal relationships; prediction reliability; calibration outside observed samples;
whether two opaque sources are substantively independent; external-event interpretation; anomaly
classification.

### 15.3 Not provable by the substrate alone (`UNKNOWABLE` — declare, do not pretend to eliminate)

That a human told the truth; that a sensor measured the correct physical thing; a proprietary model's
true training lineage; that all relevant evidence has been discovered; that unseen evidence does not
exist; that future events will happen; that an external timestamp reflects real physical time; that two
opaque models are truly independent; ground truth when it is inaccessible; semantic correctness of
arbitrary natural language; correctness of a human governance interpretation; correctness after every
root of trust is compromised.

These are hard limits. The architecture becomes sound by **declaring** them (CR-1/CR-2), not by
pretending to remove them.

---

## 16. Disposition of review findings

Every finding from the v0.1 review (the ten-point review and the twenty structural points) maps to a
v0.2 resolution. Severities, per-finding fixes, and the downstream gate are recorded in the
[v0.1 Review Record](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1_REVIEW.md); the gate is that findings
**R1–R4 and R10** (plus the state-space structural findings) must land before the Reconciliation
Protocol — and they have, here.

| Finding | Resolution in v0.2 |
|---------|--------------------|
| R1 §6 breaks §10 (governance gates commit) | §11, G1 — belief commit never depends on governance; QUARANTINE is process/integrity only |
| R2 state machine ≠ enum; non-total | §9.1 four total status dimensions; §9.2 total outcome set; T1 |
| R3 threshold dead zone | §9.1 — contestation is a graph property, not a confidence band; confidence carried alongside status |
| R4 dependence discount pushes to false | §8.2 — `LR_effective = LR^(1−d)`; d=1 returns to prior |
| R5 calibration_score = accuracy; n≥3 | §12.2 Brier/reliability set; §12.3 shrinkage + CI lower bound, no magic n |
| R6 mandatory six-float dependence | §7.3 dependence assessment (class + optional estimator-produced estimate) |
| R7 prediction-pending deadlock | §9.4 re-evaluation forward; no commit freeze on pending prediction |
| R8 mutable evidence vs audit chain | §5, E1 — immutable evidence; corrections are superseding appends; citing claims re-evaluated |
| R9 "rollback" isn't rollback | §9.4 — renamed re-evaluation; snapshot restore removed |
| R10 normative claims unhandled | §6.3 — NORMATIVE class excluded from confidence/prediction/calibration |
| S1 status overloaded | §9.1 — epistemic/admission/integrity/lifecycle split |
| S2 UNKNOWN as number vs state | §8.1 — confidence `status: ESTIMATED|UNAVAILABLE`; UNKNOWN ≠ 0.5 |
| S3 contested as confidence band | §9.1 — CONTESTED defined on the graph |
| S4 dual authority (evidence↔claim) | §7.1 — immutable relation edges; both sides derived |
| S5 machine-readable claims | §6.1/§6.2 — FORMAL (deterministic) vs SEMANTIC (estimated) |
| S6 record authenticates data not reality | §1 CR-1; §4.1 integrity vs content |
| S7 source_identity string | §4.1 — credential binding + registry verification |
| S8 timestamps overtrusted | §4.3 — three clocks; order from ledger_sequence |
| S9 WAL not transactional | §3.1 — serializable CAS; single writer/partition or consensus |
| S10 append-only ≠ tamper-proof | §4.2 — layered anchoring; "tamper-evident" |
| S11 model independence unknowable | §7.3 — dependence assessment, estimator-gated numbers |
| S12 model-generated confidence | §8.1/§8.3, K1 — method provenance or UNAVAILABLE |
| S13 Bayes not universal | §8.3 — registered methods; Bayes is one of them |
| S14 min_evidence=2 unsound | §13 — claim-class evidence policy on independent weight |
| S15 REJECTED swallows UNKNOWN | §9.1 — UNDERDETERMINED for absence; REFUTED needs negation evidence |
| S16 dependency cycles | §7.2, D1/D2 — DAG, SCC detection, no self-confirmation |
| S17 prediction pre-registration | §10.1, P1/P2 — frozen, signed, resolver ≠ predictor |
| S18 observation ≠ prediction failure | §10.2 — channel coverage; UNRESOLVABLE |
| S19 calibration process-version | §12.1 — process-version identity |
| Minor: cross-ref, "should" in invariant, UNBOUND evidence, escalation default, §8 match-quality, examples | §9.3 escalation default; §5 UNBOUND; §14 MUST-only; construction/finance examples throughout |

---

## 17. What attaches next

Reconciliation is still the next artifact — now gated on this v0.2 being **total, coherent,
trust-boundary-explicit, and mechanically testable**. The reconciliation protocol will define the exact
decision function over §9 transitions (admissibility, independence/confidence thresholds, quarantine
triggers, escalation routing) against these schemas. It is **not** to be written on top of v0.1.

The blocking review gate — findings **R1–R4 and R10** (state space + confidence arithmetic), plus the
state-space structural findings (`S1`–`S4`, `S15`, `S16`) — is **satisfied** by this version, so the
Reconciliation Protocol spec may be drafted against v0.2. See the
[v0.1 Review Record](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1_REVIEW.md) §5 for the gate.

---

*End of Epistemic Substrate Spec v0.2.*
