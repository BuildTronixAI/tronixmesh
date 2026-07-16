# Phase B Plan — Validation Report

**Document type:** Adversarial validation + critique evolution  
**Date:** 2026-07-16  
**Plan version:** Production **v1.3**  
**Artifacts:** [`PHASE-B-BUILD-PLAN-v1.1.md`](./PHASE-B-BUILD-PLAN-v1.1.md) · [`DOCTRINE-TRACEABILITY.md`](./DOCTRINE-TRACEABILITY.md) · [`adr/`](./adr/) · [`registry/`](./registry/)

---

## Meta-assessment (stronger critique)

**Rating (founder review): 9.5/10** — evaluates recommendations against actual architecture and operating model, not generic enterprise practice.

Three architectural issues with real downstream cost if ignored:

1. **Schema evolution risk** — proof model precedes envelope/storage/interfaces.  
2. **Organizational mismatch** — capacity/scheduling beats invented governance.  
3. **IP / governance risk** — implementation visibility is an IP decision.

Highest ROI process fix: **map existing doctrine** before new checklists.

---

## Verdict on original Phase B draft

Mission, workflow, out-of-scope, and M/F/A priority are sound. Draft was not kickoff-ready (stale calendar, underspecified authority, unmeetable classifier SLO as written, missing ops/IP/capacity).

---

## Disposition of recommendations

### Proof-native schema (most important)

| Wrong framing | Correct framing |
|---------------|-----------------|
| Envelope → later add proof | Proof model → Envelope schema → Storage → Interfaces → Behavior |

- Schema is proof-native.  
- Behavior is feature-flagged.  
- Narrow claim only: preserve proof/governance capability in schema; do not require every verify path in v1.

### Organization / capacity

Enterprise drift (architecture board, four owners, SBOM as Gate 0) rejected for Phase B.  
**Primary question:** Who builds this, and what stops while they do? → Gate 0.5 scheduling table.

### IP posture (legal nuance)

Distinguish:

- **Patent rights** — disclosure timing/content; U.S. vs international; coordinate with counsel.  
- **Trade secrets** — public implementation detail generally destroys protection for that detail.

Operational default: keep implementation-specific material private until counsel approves.  
**Avoid categorical legal claims** beyond that without attorney input.

### Doctrine mapping

Traceability matrix separates Covered / Partial / Verify / Gap. Duplicate documentation discouraged.

### Kept from original review

- FP/FN classifier objectives (§4.1a)  
- Approved / rejected / experimental technology registry  
- Staged rollout R1→R4 (synthetic → internal → trusted → production)  
- Gate 0 as decision point  

### Added

- **ADR Gate 0.9** — irreversible decisions (Ed25519, proof-native, LangGraph, Postgres, cell memory) without a formal board.

---

## Final disposition

Treat this critique lineage as the stronger review. Plan **v1.3** encodes it:

- Architecturally: proof into the schema, not only the implementation.  
- Operationally: founder-led team, not large-eng process.  
- Strategically: implementation visibility as IP decision (counsel-aware).  
- Practically: doctrine map before new requirements; smaller Gate 0; higher signal.

**Next:** Close Gate 0 (especially 0.5 capacity, 0.6 IP with counsel as needed, 0.9 ADRs 0004/0005).

---

*End of validation report.*
