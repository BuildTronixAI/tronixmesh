# TronixMesh Epistemic Substrate Spec

**Artifact ID:** `TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1`
**Document type:** Specification (schema-level)
**Status:** **SUPERSEDED by [`TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md`](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md)** — retained for history; **do not implement**
**Authority:** Christopher C. Leiser, Chairman (direction approved)
**Recorded in-repo:** 2026-08-15
**Superseded:** 2026-08-15 — review found blocking internal contradictions (governance gating belief commit, non-total state transitions, threshold dead zone) and two incorrect core numeric mechanisms (dependence discount, calibration-as-accuracy). v0.2 rewrites the substrate to be total, trust-boundary-explicit, and mechanically testable. See v0.2 §16 for a point-by-point disposition of the findings.

> **Superseded notice.** This document is kept only to preserve the design history. All active work
> targets [`TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md`](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md).
> The findings that retired it — with severities, per-finding fixes, and the downstream gate — are
> recorded in [`TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1_REVIEW.md`](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1_REVIEW.md).
**Scope:** Defines **only** the epistemic machinery below. It does **not** define the reconciliation
protocol (the next artifact), the delegation mechanics (see the Directive §5), or any governance change.
**Related:** [`TRONIXMESH_COGNITIVE_ARCHITECTURE_DIRECTIVE_v0.9.md`](./TRONIXMESH_COGNITIVE_ARCHITECTURE_DIRECTIVE_v0.9.md) · [`../architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../architecture/TRONIXMESH-DESIGN-DOCTRINE.md) · [`../phase-b/adr/0001-proof-native-envelopes.md`](../phase-b/adr/0001-proof-native-envelopes.md)

---

## 0. Purpose and boundary

This spec makes the epistemic contract mechanically precise. Once these objects and their admissibility
rules are concrete, the reconciliation protocol and the rest of the cognitive mesh have something real
to attach to.

It defines **only** the machinery in this pipeline:

```
Evidence
   ↓
Claim
   ↓
Dependency / provenance
   ↓
Support + contradiction
   ↓
Confidence semantics
   ↓
Belief-state transition        ← interface to the reconciliation protocol (next artifact)
   ↓
CURRENT_STATE (belief graph)
   ↓
Prediction
   ↓
Observation
   ↓
Calibration
```

Out of scope for v0.1 (deliberately): the full reconciliation decision algorithm, delegation token
verification, and any product/UX surface. Those attach *to* this substrate; they are not part of it.

---

## 1. Conventions

- **Identifiers.** Every object has a stable `id` (ULID/UUID). Objects that participate in provenance
  also carry a `content_hash` (SHA-256 over canonicalized content), consistent with the existing
  evidence model ("evidence is hashed before approval") and provenance hash chain.
- **Coordinates.** Every object is addressable by a TronixMesh coordinate, so authority scope and
  isolation are inherited from coordinate-native governance rather than re-invented here.
- **Time.** `*_at` fields are RFC 3339 UTC timestamps.
- **Attribution.** `produced_by` / `asserted_by` reference a `loop_id` from a Cognitive Delegation
  Token (Directive §5), so every epistemic object is attributable to the persistent principal.
- **Append-only where noted.** EVIDENCE, the calibration ledger, and the transition log are
  append-only; CURRENT_STATE is mutable **only** through accepted belief-state transitions.
- **Confidence.** All confidences are in `[0.0, 1.0]` with the semantics defined in §6. A confidence is
  meaningless without its `basis`.

---

## 2. Evidence object

Evidence is a record of *what has actually been observed*. It is the ground floor of the pipeline and
lives in the append-only **EVIDENCE** store.

```json
{
  "id": "ev_...",
  "kind": "observation | retrieval | model_output | solver_result | sensor | human | simulation",
  "channel_id": "chan_...",
  "independence_class": "string",
  "content": { "…": "channel-specific payload" },
  "content_hash": "sha256:…",
  "produced_by": "loop_...",
  "observed_at": "2026-08-15T00:00:00Z",
  "provenance_ref": "prov_…",
  "signature": "ed25519:…"
}
```

| Field | Meaning | Admissibility |
|-------|---------|---------------|
| `kind` | The mechanism that produced the evidence | Required; must be a known kind |
| `channel_id` | The cognitive channel that produced it (Directive §6) | Required |
| `independence_class` | A label used to detect correlated sources (e.g. shared base model / corpus). Two evidence items sharing an `independence_class` are **not** treated as independent | Required (may be `"unknown"`) |
| `content_hash` | Hash of canonicalized `content` | Required; must verify |
| `produced_by` | `loop_id` of the delegated capability that emitted it | Required |
| `provenance_ref` | Link into the provenance hash chain | Required |
| `signature` | Cryptographic attribution | Required for admissibility |

**Invariant E1.** Evidence is immutable. Corrections are new evidence items that reference the prior one;
nothing in EVIDENCE is edited or deleted.

---

## 3. Claim object

A claim is a *proposition asserted from evidence*. Claims are the unit that beliefs are formed about.

```json
{
  "id": "cl_...",
  "statement": "canonical proposition text or structured predicate",
  "claim_type": "empirical | derived | normative-observation | predictive | meta",
  "subject_coordinate": "…",
  "derived_from": ["ev_…", "cl_…"],
  "asserted_by": "loop_...",
  "created_at": "2026-08-15T00:00:00Z",
  "content_hash": "sha256:…"
}
```

| Field | Meaning |
|-------|---------|
| `statement` | The proposition. Structured predicates preferred over free text where possible |
| `claim_type` | `empirical` (about the world), `derived` (inferred from other claims), `normative-observation` (an observation *about* policy, e.g. "X is prohibited" — an observation, not an enforcement), `predictive`, `meta` (a claim about the epistemic process itself) |
| `subject_coordinate` | What the claim is about, in the coordinate space |
| `derived_from` | The evidence and/or claims this claim rests on (its immediate dependencies) |

**Invariant C1.** A claim's `derived_from` closure must terminate in admissible evidence. A claim with no
evidence closure is inadmissible (it is a hypothesis, not a claim — hypotheses live in the hypothesis
channel until evidenced).

---

## 4. Dependency / provenance metadata

Dependencies are typed edges that record **why** a claim holds and **how independent** its support is.
This is what lets the mesh reason about correlated failure rather than counting votes.

```json
{
  "id": "dep_...",
  "from": "cl_...",
  "to": "ev_… | cl_...",
  "relation": "derives_from | assumes | uses_method",
  "independence_note": "shared-corpus | independent | unknown",
  "weight": 0.0
}
```

- **Independence tracking.** Dependency metadata carries the `independence_class` lineage so that two
  claims resting on the same underlying source are not double-counted as corroboration.
- **Method dependence.** `uses_method` records that a claim depends on a particular method (e.g. a
  specific solver or retrieval index), so a method-level fault can invalidate everything downstream.

**Invariant D1.** The dependency graph over claims/evidence is a DAG. Cycles are inadmissible and are a
reconciliation error (a claim may not, transitively, depend on itself).

---

## 5. Support and contradiction

Support and contradiction are typed, weighted edges between epistemic objects. They are the raw material
the confidence layer consumes.

```json
{
  "id": "rel_...",
  "type": "SUPPORTS | CONTRADICTS",
  "source": "ev_… | cl_...",
  "target": "cl_...",
  "strength": 0.0,
  "rationale": "why this source supports/contradicts the target",
  "asserted_by": "loop_..."
}
```

- `strength ∈ [0,1]` is the *edge-local* strength of support/contradiction, before independence
  adjustment.
- Contradiction is first-class: the substrate never silently drops a contradicting source. A
  contradiction edge is retained and surfaces in the belief's contradiction state (§7).

---

## 6. Confidence semantics

Confidence is a **calibrated degree of belief**, not a vote tally and not a raw model logit.

A belief's confidence is a function of:

1. its supporting and contradicting edges (§5),
2. the **independence** of those sources (§4) — correlated sources contribute sub-additively,
3. the **historical calibration** of the contributing channels/claim-types (§11).

```json
{
  "value": 0.0,
  "basis": {
    "support": ["rel_…"],
    "contradiction": ["rel_…"],
    "independent_source_count": 0,
    "correlated_groups": [["chan_a", "chan_b"]],
    "calibration_ref": "cal_…"
  },
  "method": "aggregation-method-id@version",
  "computed_at": "2026-08-15T00:00:00Z"
}
```

Requirements (v0.1):

- **R6.1 — Meaning fixed.** `value` is the substrate's calibrated probability that the claim is true
  given current evidence. Any aggregation `method` must be documented and versioned in `method`.
- **R6.2 — No naïve averaging.** Sources sharing an `independence_class` are aggregated as a group, not
  independently; adding a correlated source must not increase confidence as if it were independent.
- **R6.3 — Contradiction cannot be hidden.** A high `value` with unresolved contradiction edges is only
  admissible if the belief's contradiction state (§7) is explicitly `TENSION` or `CONTESTED`, never
  `COHERENT`.
- **R6.4 — Calibration-aware.** `value` is adjusted by the calibration record of its contributing
  channels/claim-types (§11); a chronically over-confident channel is discounted.
- **R6.5 — Confidence ≠ authority.** A high-confidence belief confers **no** authority to act; action is
  governed independently (Directive §4).

---

## 7. Contradiction states

Every belief in CURRENT_STATE carries an explicit contradiction state describing the coherence of its
support, independent of its confidence `value`.

| State | Meaning |
|-------|---------|
| `COHERENT` | Support present; no material contradiction edges |
| `TENSION` | Support and contradiction both present but reconcilable at current evidence |
| `CONTESTED` | Material contradiction unresolved; the belief is held but flagged |
| `UNDECIDED` | Insufficient evidence to form a belief (candidate only) |
| `QUARANTINED` | Set aside pending review — used when the *process* is suspect (see Directive §4), not because the belief is inconvenient |

**Invariant Q1.** `QUARANTINED` applies to a belief or process because of an epistemic/process fault
(e.g. an attempt to mutate or reinterpret governance, a detected method fault, a broken dependency), and
**never** because a valid belief's implications conflict with policy.

---

## 8. Belief-state transition (interface to reconciliation)

A belief-state transition is a **proposed** change to CURRENT_STATE. Cognitive loops emit transition
proposals; they never write CURRENT_STATE directly (Directive §5). The **reconciliation protocol** (the
next artifact) decides each proposal's outcome. This section defines the *interface* only.

```json
{
  "id": "txn_...",
  "proposed_by": "loop_...",
  "op": "ADD_BELIEF | UPDATE_CONFIDENCE | ADD_SUPPORT | ADD_CONTRADICTION | RETRACT | MERGE | SPLIT",
  "target": "cl_… | belief_…",
  "evidence_delta": ["ev_…"],
  "relation_delta": ["rel_…"],
  "proposed_confidence": { "…": "see §6" },
  "justification": "why this transition is warranted",
  "created_at": "2026-08-15T00:00:00Z"
}
```

The reconciliation protocol must map every proposal to exactly one **outcome**:

| Outcome | Meaning (to be fully specified by the reconciliation protocol) |
|---------|----------------------------------------------------------------|
| `ACCEPTED` | Transition applied to CURRENT_STATE; logged |
| `REJECTED` | Transition denied (e.g. inadmissible evidence, DAG violation); logged with reason |
| `QUARANTINED` | Transition and/or its originating process set aside for review (process fault, not policy conflict) |
| `ABSTAINED` | Insufficient basis to decide; belief remains `UNDECIDED`; no state change |
| `ESCALATED` | Referred upward (to another loop, the principal, or a human) per authority structure |

**Invariant T1.** Every transition proposal produces exactly one outcome and one append-only
**transition log** entry `{txn_id, outcome, reason, decided_by, decided_at}`. CURRENT_STATE changes only
on `ACCEPTED`.

**Invariant T2.** Applying an `ACCEPTED` transition must preserve the substrate invariants (E1, C1, D1,
Q1) or the transition is a reconciliation error and must not be applied.

> The precise decision function — admissibility checks, independence/confidence thresholds, quarantine
> triggers, and escalation routing — is deliberately **not** defined here. It is the subject of the
> reconciliation protocol, which is the next artifact and depends on these schemas being precise.

---

## 9. CURRENT_STATE (the belief graph)

CURRENT_STATE is the belief graph: *what TronixMesh presently has reason to believe.* It is **derived,
mutable, reconcilable state** and lives outside the canonical manifest (Directive §3).

A **belief** node:

```json
{
  "id": "belief_...",
  "claim": "cl_...",
  "confidence": { "…": "see §6" },
  "contradiction_state": "COHERENT | TENSION | CONTESTED | UNDECIDED | QUARANTINED",
  "support_closure": ["rel_…"],
  "evidence_closure": ["ev_…"],
  "last_transition": "txn_...",
  "version": 7,
  "updated_at": "2026-08-15T00:00:00Z"
}
```

- Edges of the belief graph are the support/contradiction (§5) and dependency (§4) edges.
- **Invariant S1 — Auditability.** Every belief cites its `evidence_closure`; a belief that cannot trace
  to admissible evidence is inadmissible in CURRENT_STATE.
- **Invariant S2 — Provenanced mutation.** Every version increment references the `txn_id` that caused
  it; the history of a belief is reconstructable from the append-only transition log.
- **Invariant S3 — No canon here.** CURRENT_STATE contains beliefs only. Rules, schemas, and authority
  structure live in the canonical manifest, never here.

---

## 10. Prediction and observation

Predictions are what make the substrate *testable*: a belief that never yields a checkable prediction
cannot be calibrated.

**Prediction:**

```json
{
  "id": "pred_...",
  "from_belief": "belief_...",
  "predicted_observable": "structured description of what should be observed",
  "resolution_criteria": "exact condition that counts as correct/incorrect",
  "stated_confidence": 0.0,
  "horizon": "2026-09-01T00:00:00Z",
  "created_by": "loop_...",
  "created_at": "2026-08-15T00:00:00Z"
}
```

**Observation / result** (resolves a prediction; is itself admissible evidence):

```json
{
  "id": "obs_...",
  "resolves": "pred_...",
  "outcome": "CORRECT | INCORRECT | PARTIAL | UNRESOLVABLE",
  "evidence_ref": "ev_...",
  "resolved_at": "2026-08-20T00:00:00Z"
}
```

**Invariant P1.** A prediction must carry `resolution_criteria` precise enough that an observation can be
adjudicated `CORRECT`/`INCORRECT` without re-litigating the belief. A prediction with `stated_confidence`
resolves into the calibration ledger (§11).

---

## 11. Calibration ledger

The calibration ledger is the append-only record that closes the loop: it compares stated confidences
against observed outcomes so the substrate can learn *how much to trust each channel and claim-type.*

```json
{
  "id": "cal_...",
  "prediction": "pred_...",
  "observation": "obs_...",
  "channel_id": "chan_...",
  "claim_type": "empirical | derived | …",
  "stated_confidence": 0.0,
  "correct": true,
  "recorded_at": "2026-08-20T00:00:00Z"
}
```

Derived calibration metrics (per `channel_id` and per `claim_type`) — e.g. reliability curves and Brier
scores — are computed from the ledger and consumed by the confidence layer (R6.4). Requirements:

- **R11.1 — Append-only.** Ledger entries are never edited; recomputed metrics are versioned artifacts.
- **R11.2 — Feedback.** A channel's demonstrated over/under-confidence adjusts the weight of its future
  contributions to confidence (§6), giving the mesh a memory of *who has been right and how sure they
  said they were.*
- **R11.3 — Provenance-aware.** Calibration is tracked per channel *and* per `independence_class`, so a
  correlated cluster that is jointly miscalibrated is discounted as a group.

---

## 12. End-to-end invariants (summary)

| ID | Invariant |
|----|-----------|
| E1 | Evidence is immutable and append-only |
| C1 | Every claim's dependency closure terminates in admissible evidence |
| D1 | The dependency graph is a DAG (no self-dependence) |
| Q1 | Quarantine is for process/epistemic faults, never for policy-inconvenient valid beliefs |
| T1 | Every transition proposal yields exactly one outcome + one transition-log entry |
| T2 | Applying an accepted transition preserves all substrate invariants |
| S1 | Every belief cites its evidence closure (auditable) |
| S2 | Every belief version references the transition that produced it |
| S3 | CURRENT_STATE holds beliefs only; no canon |
| P1 | Predictions carry adjudicable resolution criteria |

---

## 13. What attaches next

Once this substrate is mechanically precise, the **reconciliation protocol** (next artifact) defines the
decision function over §8 transitions: admissibility, independence/confidence thresholds, the exact
triggers for `QUARANTINED`, the basis for `ABSTAINED`, and the routing for `ESCALATED`. Only after that
is executable does Cognitive Mesh v0 have a real epistemic system to run its experiment against.

---

*End of Epistemic Substrate Spec v0.1.*
