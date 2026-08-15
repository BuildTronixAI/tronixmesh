# TronixMesh Cognitive Mesh — Research Direction

**Document type:** Research-direction index (non-normative)
**Status:** **APPROVED RESEARCH DIRECTION / PENDING ARCHITECTURE** — *not* settled operational truth
**Authority:** Christopher C. Leiser, Chairman (direction approved); architecture not yet canonical
**Recorded in-repo:** 2026-08-15
**Related:** [`../architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../architecture/TRONIXMESH-DESIGN-DOCTRINE.md) · [`../architecture/TRONIXMESH-ARCHITECTURE-v2.md`](../architecture/TRONIXMESH-ARCHITECTURE-v2.md) · [`../phase-b/README.md`](../phase-b/README.md)

---

## What this area is

TronixMesh is becoming a **cognitive mesh**: not one model wrapped in tools, but a heterogeneous
set of cognitive channels whose outputs are reconciled into an auditable belief state, under the
same governance runtime that already treats the LLM as untrusted compute.

This directory captures that direction **as doctrine and specification under construction**. It is
deliberately *sequenced* so that the hard part — the epistemic contract between cognition and
reality — is made mechanically precise **before** anything above it is locked as canonical.

> The belief graph is not merely another component. It is the **interface contract between
> cognition and epistemic reality**. If that contract is vague, everything above it is hand-waving.

### The claim we are actually making

The mesh does **not** try to make epistemic *truth* deterministic — that is not achievable, and
pretending otherwise is how "multi-agent reasoning" systems fool themselves. The defensible claim is
narrower:

> Epistemic **processing** is **accountable, bounded, reproducible, corrigible, and tamper-evident**,
> and every conclusion is labelled as **digitally guaranteed**, **estimated**, or **fundamentally
> unknowable** to the substrate alone. Model consensus, repetition, and cryptographic integrity are
> never treated as proof of external-world truth.

---

## Status discipline (read before editing)

1. **The bootstrap / governance spec is frozen for this work.** Do not contaminate the trust root
   with speculative cognitive mechanics. Cognitive-mesh artifacts live here, reference the existing
   normative doctrine, and never edit it. See the existing trust stack in
   [`../architecture/TRONIXMESH-DESIGN-DOCTRINE.md`](../architecture/TRONIXMESH-DESIGN-DOCTRINE.md).
2. **Nothing here is canonical yet.** The Cognitive Architecture Directive is intentionally issued
   at **v0.9** (doctrine, not normative implementation law). It becomes **v1.0 canonical only after**
   the v0 experiment (below) is internally executable.
3. **Do not record this as settled architecture in `MEMORY.md`** (or any store functioning as
   durable operational truth). Record it as an *approved research direction / pending architecture*
   until the epistemic contracts are locked.

---

## The sequence (and why this order)

The ordering minimizes architecture theater and tests the actual hard part first:

```
freeze bootstrap
      ↓
epistemic substrate          ← the hard part, made mechanically precise first
      ↓
reconciliation protocol      ← how a belief transition is accepted/rejected/quarantined/abstained/escalated
      ↓
cognitive-loop delegation    ← attributable delegated capability, not a new principal
      ↓
v0 experiment                ← does the heterogeneous mesh beat a strong single-model+tools baseline?
      ↓
lock Cognitive Architecture v1.0 (canonical)
```

| # | Step | Rationale |
|---|------|-----------|
| 1 | **Freeze** the current bootstrap/governance spec | Keep the trust root clean; cognition attaches *under* governance, never inside it |
| 2 | Issue **Cognitive Architecture Directive v0.9** (doctrine, non-normative) | Frame the architecture without granting it the force of implementation law |
| 3 | Define the **epistemic substrate** (schemas) | Belief graph, evidence, provenance/dependency, confidence, contradiction, calibration, prediction/result |
| 4 | Define the **reconciliation protocol** against those schemas | The critical part — exact admission/rejection/quarantine/abstain/escalate semantics |
| 5 | Write **Cognitive Mesh v0** as an experiment | Test measurable value vs a strong single-model + tools baseline |
| 6 | **Only then** lock **Cognitive Architecture v1.0** canonical | Coherence must be demonstrable, not asserted |

---

## Artifacts

| Artifact | Version | Status | File |
|----------|---------|--------|------|
| Cognitive Architecture Directive | v0.9 | Doctrine (non-normative) | [`TRONIXMESH_COGNITIVE_ARCHITECTURE_DIRECTIVE_v0.9.md`](./TRONIXMESH_COGNITIVE_ARCHITECTURE_DIRECTIVE_v0.9.md) |
| Epistemic Substrate Spec | v0.2 | **Active — the current build target** | [`TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md`](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.2.md) |
| Epistemic Substrate Spec | v0.1 | **Superseded** (history only; do not implement) | [`TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1.md`](./TRONIXMESH_EPISTEMIC_SUBSTRATE_SPEC_v0.1.md) |
| Reconciliation Protocol | — | **Next artifact** (blocked on substrate v0.2 being total, coherent, trust-boundary-explicit, and mechanically testable) | *not yet produced* |
| Cognitive Mesh v0 experiment | — | Pending | *not yet produced* |
| Cognitive Architecture Directive | v1.0 | **Do not lock yet** | *pending experiment* |

The **next artifact to produce is the reconciliation protocol**, and only once the substrate spec is
total and mechanically testable (not on top of v0.1). It must define exactly how a proposed belief
transition is *accepted, rejected, quarantined, abstained, or escalated* against the substrate schemas.

**Why v0.1 was superseded:** a full review found blocking internal contradictions (governance gating
belief commit, a non-total state machine, threshold dead zones) and two incorrect core numeric
mechanisms (the dependence discount pushed belief toward *false*; the calibration score measured
*accuracy*, not calibration). v0.2 resolves all of these; see its §16 for a point-by-point disposition.

---

## Relationship to existing doctrine

Nothing here weakens the established trust model. Cognition sits **below** governance in the trust
stack, exactly where the LLM already sits:

```
Human → Governance → Runtime → Evidence → Policies → Cognition (mesh) → individual models/channels
```

- A cognitive loop is **not** a new principal; it is a delegated, attributable capability of an
  existing principal (see the Directive, §"Cognitive delegation").
- The belief graph is **derived state** (CURRENT_STATE), not canon; the manifest owns the *rules*,
  the graph owns the *beliefs* (see the Directive, §"Normative / epistemic separation").
- **Governance constrains action, not observation.** A belief may remain valid even when acting on
  it is prohibited (see the Directive, §"Governance vs. belief").

---

*End of Cognitive Mesh research-direction index.*
