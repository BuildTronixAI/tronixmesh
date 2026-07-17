# Phase B Plan — Validation Report

**Document type:** Adversarial validation of *Tronix Mesh — Phase B Inner-First Build Plan* (Draft)  
**Validated against:** v1.1 Architecture, Engineering Integration Guide v1.0, Peer Review Final v1.0, Doctrine Bundle v1.1, Whitepaper/v2.3, Flowchart v1.0  
**Date:** 2026-07-16  
**Status:** Draft not execution-ready; production plan updated through **v1.2** after founder refinement  
**Plan:** [`PHASE-B-BUILD-PLAN-v1.1.md`](./PHASE-B-BUILD-PLAN-v1.1.md) · Traceability: [`DOCTRINE-TRACEABILITY.md`](./DOCTRINE-TRACEABILITY.md)

---

## Verdict

Mission, workflow, out-of-scope discipline, and M/F/A priority are sound. The May draft is not kickoff-ready (stale calendar, underspecified authority, unmeetable classifier SLO, missing ops/IP/capacity).

**Refinement accepted (Chris, 2026-07-16):** generic big-company process was over-weighted; proof fields are **not** orthogonal to the data model; doctrine should be mapped before new gates; capacity displacement and IP posture are first-class.

---

## What Holds

| Item | Why |
|------|-----|
| Inner-first handoff mission | v1.1 §6; RTP pressure |
| Competitive intel 3-agent + one boundary | Real value, representative, repeatable |
| Hard out-of-scope | Protects ship |
| M/F/A primary; P secondary within 2× | Correct ordering |
| Fail-closed + provenance survives failure | Doctrine + v1.1 §8.5 |
| Eval set as contract | Measurability |
| Clear accountability | Valid — **implementation lightened** for founder-scale |

---

## Critical Defects (Original Draft)

### C1 — Schedule stale
May 30, 2026 target vs validation date 2026-07-16 → rebaselined to T0+30.

### C2 — Substrate dualism → **refined disposition**
v1.1 envelope/grid vs v2.3 MeshResolver/ProofPackage remain distinct **behaviors**, but proof is **not** safely deferred if it is part of the data model.

**Wrong recommendation (earlier pass):** “defer ProofPackage entirely / v1.1-only.”  
**Corrected recommendation:** **proof-native schema now, proof-enabled behavior later.**

| Design now | Enable later |
|------------|--------------|
| Envelope schema | Proof verification |
| Proof fields / refs | Mesh resolution hot path |
| Signature blocks | Distributed enforcement |
| Versioning | Cross-node consensus |

Narrow claim: if patentable differentiation depends on proof and governance, preserve those capabilities in schema/interfaces from the outset — without implementing every verification path in Phase B.

### C3 — Ownership → **refined disposition**
Unassigned owners remain a blocker. **Rejected:** four owners/component, architecture board, formal committees.  
**Adopted:** Chris (architecture + ops), Robert (runtime), peer/council security review before release.

### C4 — Authority at public→confidential underspecified
Still requires Phase B minimal authority (bootstrap/static grant). Decision Tokens stay Phase C.

### C5 — Classifier latency vs Haiku
Split P1a (rules) / P1b (LLM escalate).

### C6 — “No new infra” vs proposed stack
Inventory Vultr first; document downgrades.

---

## High Gaps — Disposition After Refinement

| Gap | Disposition |
|-----|-------------|
| Idempotency / delivery semantics | Kept in plan §3.3 / F9 |
| Security / threat model | Prefer doctrine map; add only Open rows (injection suite, ACL, secrets path) |
| Observability | Open in traceability → short pilot note, not new doctrine |
| Runbooks / kill switch | Kept; map halt semantics to doctrine where possible |
| Eval contract | Kept |
| CI / restore drill | Kept |
| Cost reconcile | Gate 0.7 |
| Repo / packaging | Folded into Gate 0.6 IP + private eng default for RTP |
| **IP posture** | **Added** — disclosure vs non-provisional, trade secret, private repos |
| **Capacity displacement** | **Added** — Robert/TronixMesh vs Pre-Con, Clover, AMS, FedTronix, Carl’s Wine Vault |
| **Doctrine-first gates** | **Added** — traceability matrix before new S/O paperwork |

---

## Process Corrections

| Heavyweight advice | Founder-scale substitute |
|--------------------|---------------------------|
| Architecture board | Chris freezes schemas (Gate 0.1) |
| Multi-owner RACI matrix | Single owner per subsystem |
| Standing security committee | Peer/council review before release |
| Long Q1–Q10 wall | Streamlined **Gate 0** (8 decisions) |
| “Embedded enforcement proof is the product” | Preserve proof/governance capability in schema; phase enablement |

---

## Recommended Disposition

1. Keep mission, workflow, M/F/A structure.  
2. Execute against plan **v1.2** (proof-native, Gate 0, capacity, IP).  
3. Close Gate 0 before counting build days.  
4. Use [`DOCTRINE-TRACEABILITY.md`](./DOCTRINE-TRACEABILITY.md) to avoid duplicate docs.  
5. Do not market Phase B as Doctrine-1B crypto-certified.

---

*End of validation report.*
