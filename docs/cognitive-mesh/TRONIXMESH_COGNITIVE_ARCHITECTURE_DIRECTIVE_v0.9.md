# TronixMesh Cognitive Architecture Directive

**Artifact ID:** `TRONIXMESH_COGNITIVE_ARCHITECTURE_DIRECTIVE_v0.9`
**Document type:** Architectural doctrine
**Status:** **v0.9 — DOCTRINE, NOT NORMATIVE IMPLEMENTATION LAW** (pending)
**Authority:** Christopher C. Leiser, Chairman (direction approved; not yet canonical)
**Recorded in-repo:** 2026-08-15
**Becomes canonical when:** the Cognitive Mesh v0 experiment is internally executable (then, and only
then, this is reissued as **v1.0 canonical**)
**Related:** [`README.md`](./README.md) · [`TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md`](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md) · [`../architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../architecture/TRONIXMESH-DESIGN-DOCTRINE.md)

---

## 0. Status and scope of authority

This directive is **doctrine**, not implementation law. It frames the cognitive-mesh architecture and
records approved decisions of direction. It does **not** authorize any change to the frozen
bootstrap/governance spec, and it does **not** define normative behavior that the runtime must enforce.
Normative machinery is deferred to the specifications it points to (starting with the Epistemic
Substrate Spec), and canonicalization is gated on a working v0 experiment.

Version discipline is deliberate:

- **v0.9 (this document):** architectural doctrine. Shapes what we build and in what order.
- **v1.0 (future):** canonical. Issued only after the epistemic contracts are locked and the v0
  experiment demonstrates the heterogeneous architecture is internally coherent and adds measurable
  value over a strong single-model + tools baseline.

---

## 1. Thesis

TronixMesh is evolving from a governance runtime over a small set of agents into a **cognitive mesh**:
a heterogeneous collection of cognitive channels whose outputs are reconciled into an **auditable
belief state**. The mesh is valuable precisely because it is heterogeneous — deliberately including
methods *outside* the transformer family — so that correlated failure across similar models can be
detected and defeated rather than averaged into false confidence.

The governance posture is unchanged: **agents reason, the runtime governs, humans retain ultimate
authority.** Cognition is added *below* governance in the trust stack, never inside it.

### 1.1 The narrower, defensible claim

The architecture does **not** need to solve epistemology, and it must not pretend to. It does **not**
make epistemic *truth* deterministic. Its claim is narrower and achievable:

> TronixMesh makes epistemic **processing** **accountable, bounded, reproducible, corrigible, and
> tamper-evident** — and it never treats model consensus, repetition, or cryptographic integrity as
> proof of external-world truth.

That is a stronger position than most "multi-agent reasoning" systems precisely because it stops
pretending model agreement equals truth.

### 1.2 Three categories of knowledge

Every epistemic value the mesh produces is tagged with the category of knowledge it belongs to. The
substrate spec carries the machinery; the doctrine is that these are **never** silently mixed:

| Category | Meaning |
|----------|---------|
| **Digitally guaranteed** | Provable inside the trusted digital substrate (schema, signatures, hashes, ledger order, formal-claim contradiction, audit replay) |
| **Estimated** | Producible only as a probabilistic estimate by a defined procedure (source/model reliability, semantic contradiction, empirical likelihood, model dependence) |
| **Fundamentally unknowable to the substrate alone** | Requires trusting something outside the substrate (human honesty, that a sensor measured the right thing, a proprietary model's true lineage, that all evidence has been found) |

### 1.3 Constitutional rules

Two rules bulletproof the entire design and become normative when this area is canonical:

> **CR-1 (Digital ≠ external truth).** TronixMesh SHALL distinguish facts established by the trusted
> digital substrate from assertions about the external world. Cryptographic integrity, provenance,
> consensus, repetition, model agreement, or schema validity SHALL NOT be interpreted as proof that an
> external-world assertion is true.

> **CR-2 (Exposed assumptions).** Every epistemic conclusion SHALL expose the trust assumptions,
> inference method, unresolved uncertainty, and evidence lineage upon which it depends.

### 1.4 Five separations

v0.2 of the substrate is organized around five separations the first draft conflated. They are doctrine,
not merely schema choices:

1. **Truth state ≠ admission state ≠ integrity/quarantine state ≠ lifecycle state.**
2. **Observation/evidence ≠ claim/inference ≠ normative preference.**
3. **Digitally verified fact ≠ externally asserted fact.**
4. **Probability estimate ≠ UNKNOWN** (UNKNOWN is a state, not the number 0.5).
5. **Epistemic acceptance ≠ execution authorization.**

---

## 2. Sequencing principle (the hard part first)

> Do **not** lock the Cognitive Architecture Directive as v1.0 before the belief graph and
> reconciliation contracts are concrete enough to prove the architecture is internally coherent.

The belief graph is the **interface contract between cognition and epistemic reality**. A vague
contract makes everything above it hand-waving. Therefore the build order is:

1. **Freeze** the bootstrap/governance spec — do not contaminate the trust root with speculative
   cognitive mechanics.
2. Issue **this directive at v0.9** — doctrine, not law.
3. Define the **epistemic substrate**: belief graph schema, evidence object, provenance/dependency
   metadata, confidence semantics, status model, calibration ledger, prediction/observation objects,
   and the trust boundaries. See [`TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md`](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md)
   (v0.1 superseded). Reconciliation is gated on this substrate being **total, coherent,
   trust-boundary-explicit, and mechanically testable**.
4. Define the **reconciliation protocol** against those schemas — exactly how a proposed belief
   transition is *accepted, rejected, quarantined, abstained, or escalated*. **Do not** build it on
   v0.1.
5. Write **Cognitive Mesh v0** as an experiment with strong baselines; measure whether the whole
   heterogeneous architecture beats a strong single-model + tools baseline.
6. **Only then** promote this directive to **v1.0 canonical**.

---

## 3. Normative / epistemic separation

The system keeps a strict separation between *what makes a belief valid* (normative, canonical) and
*what is presently believed* (epistemic, derived). This preserves the normative/epistemic boundary
already established in the design doctrine.

```
CANONICAL
   ↓   "What constitutes a valid belief transition?"
EVIDENCE
   ↓   "What has actually been observed?"
CURRENT_STATE
   ↓   "What does TronixMesh presently have reason to believe?"
```

- **CANONICAL / manifest** owns the *schema, rules, reconciliation protocol, admissibility
  requirements, and authority structure*. It does not own beliefs.
- **EVIDENCE** is the append-only record of what has been observed (already a first-class concept in
  the evidence model and provenance hash chain).
- **CURRENT_STATE** holds the **belief graph** — but it is **not** the source of epistemic truth. The
  authoritative store is the **immutable evidence/relation/transition log**; CURRENT_STATE is a
  **derived, reproducible materialized view** of that log. If it is lost or suspect, it is discarded and
  rebuilt by deterministic replay. **The belief graph belongs in CURRENT_STATE, not the canonical
  manifest** — and CURRENT_STATE is never a second, mutable authority.

Rule of thumb: the manifest is stable and rarely changes; the authoritative log is append-only; the
belief graph is a rebuildable projection that changes only through the reconciliation protocol the
manifest defines. Making CURRENT_STATE mutable *authority* is exactly what creates reconciliation and
rollback nightmares — so it is derived, not authoritative.

---

## 4. Governance vs. belief (constrain action, not observation)

A belief that contradicts governance is **not inherently invalid**. The system may legitimately hold:

> "Executing X would maximize profit."

while governance says:

> "X is prohibited."

The epistemic belief can remain true while execution is denied. Therefore:

> **Governance constrains action, not permitted observation of reality.**

Operational rule:

- Do **not** delete or distort a valid belief merely because its implications conflict with policy.
- **Quarantine the cognitive process only** if it attempts to (a) mutate governance, (b) falsely
  reinterpret governance, or (c) execute around governance.
- Acting on any belief still flows through the existing governance state machine and Decision Token
  path. A prohibited action is *blocked at the authority layer*, with the belief left intact and
  auditable.

This distinction matters enormously: it keeps the epistemic layer honest (it can model reality even
when reality is inconvenient) while keeping the authority layer strict.

---

## 5. Cognitive delegation (one principal, attributable operations)

A spawned cognitive loop does **not** receive a full independent bootstrap identity. **BOB remains the
persistent principal.** Each spawned loop instead receives a **cryptographically attributable delegated
cognitive capability** — a *Cognitive Delegation Token* — so there is one identity while every
cognitive operation is individually attributable.

```
BOB
 └── Cognitive Delegation Token
       ├── loop_id
       ├── parent_loop
       ├── purpose
       ├── allowed_state_reads
       ├── allowed_proposal_types
       ├── resource_budget
       ├── recursion_depth
       ├── expiry
       └── signature
```

| Field | Meaning |
|-------|---------|
| `loop_id` | Unique id of this cognitive loop |
| `parent_loop` | The loop (or root principal) that requested this one — establishes the delegation chain |
| `purpose` | The task/question this loop exists to serve |
| `allowed_state_reads` | Which parts of CURRENT_STATE / EVIDENCE this loop may read |
| `allowed_proposal_types` | Which kinds of epistemic proposals it may submit (never direct writes) |
| `resource_budget` | Compute / token / time budget |
| `recursion_depth` | Current depth; bounds runaway self-spawning |
| `expiry` | Hard expiry after which the capability is invalid |
| `signature` | Cryptographic attribution binding the above to BOB's principal |

**Authority rule:** a loop **may propose** epistemic changes; it **must not** have direct write
authority over canonical belief state. All writes to CURRENT_STATE occur only through the reconciliation
protocol. Whether a loop `may request subordinate loops` is itself a delegated permission, bounded by
`recursion_depth` and `resource_budget`.

This is the cognitive analogue of Decision Tokens: the same "attributable, scoped, expiring, signed"
discipline the runtime already applies to *action* is applied to *cognition*.

---

## 6. The cognitive mesh: channels, not a single fabric

The multichannel transformer is **not** the entire TronixMesh workspace. It is **one advanced cognitive
fabric implementation** that can host several channels internally. Making the transformer synonymous
with the mesh would defeat the point: we deliberately need methods **outside the transformer family** to
defeat correlated failure.

```
TRONIXMESH COGNITIVE MESH
│
├── Multichannel Transformer
│    ├── evidence channel
│    ├── memory channel
│    ├── hypothesis channel
│    ├── critique channel
│    └── community-data channel
│
├── Independent frontier LLM
├── Open / community model
├── Deterministic solver
├── Retrieval engine
├── Simulator
├── Sensor / API evidence
└── Human evidence
```

The mesh should be able to reason not merely *"Claude says X and GPT says X,"* but:

> "Channel A and Channel B share likely corpus dependence; Channel C is an independently trained open
> model using a separately curated domain corpus; deterministic solver D confirms the numerical
> premise; retrieved primary evidence E contradicts one subclaim."

That is far closer to an actual epistemic system: it reasons about **independence and provenance of
sources**, not just their surface agreement.

### 6.1 Transparent Cognitive Channel (research axis)

Community data plus transparent models is elevated to its own research axis:

> **Transparent Cognitive Channel** — a model/channel whose training lineage, datasets (where legally
> available), fine-tuning history, evaluations, calibration, failure record, and inference
> configuration are **substantially observable** to TronixMesh.

This gives TronixMesh something frontier APIs cannot fully provide: **cognitive provenance**. A
transparent channel's agreement or disagreement can be weighted with knowledge of *why* it believes
what it believes and *how independent* it is from other channels — directly feeding the confidence and
independence semantics of the epistemic substrate.

---

## 7. Answers to the four open questions

Recorded here as approved direction (non-normative until v1.0):

1. **Loop identity.** No per-loop bootstrap identity. One persistent principal (BOB) + Cognitive
   Delegation Tokens (§5). Loops propose; they never write canonical belief state directly.
2. **Where the belief graph lives.** In **CURRENT_STATE**, not the canonical manifest. The manifest
   defines schema, rules, reconciliation protocol, admissibility, and authority; beliefs are derived,
   mutable, reconcilable state (§3).
3. **Beliefs vs. governance.** A belief contradicting governance is not inherently invalid. Governance
   constrains action, not observation. Quarantine only on attempts to mutate/reinterpret/bypass
   governance (§4).
4. **Transformer vs. mesh.** The multichannel transformer is one cognitive fabric among many channels,
   not the mesh itself. Heterogeneity (including non-transformer methods) is a requirement, and the
   Transparent Cognitive Channel is a first-class research axis (§6).

---

## 8. Path to v1.0 (canonicalization gates)

This directive is promoted to **v1.0 canonical** only when all of the following hold:

| Gate | Condition |
|------|-----------|
| C1 — Substrate precise | The Epistemic Substrate Spec is mechanically precise: every object in the pipeline has a concrete schema and admissibility rules |
| C2 — Reconciliation defined | The reconciliation protocol specifies exact accept / reject / quarantine / abstain / escalate semantics against those schemas |
| C3 — Delegation defined | Cognitive Delegation Tokens are specified and enforceable, with loops unable to write canonical belief state directly |
| C4 — v0 executable | Cognitive Mesh v0 is internally executable as an experiment with strong baselines |
| C5 — Measurable value | The v0 experiment shows the heterogeneous mesh adds measurable value over a strong single-model + tools baseline (or the architecture is revised) |

Until every gate is met, this remains **v0.9 doctrine** and must not be recorded as settled operational
truth.

---

*End of Cognitive Architecture Directive v0.9.*
