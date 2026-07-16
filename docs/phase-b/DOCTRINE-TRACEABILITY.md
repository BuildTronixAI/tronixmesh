# Phase B — Doctrine / Spec Traceability Matrix

**Purpose:** Map production gates to **existing** doctrine before inventing new docs.  
**Rule:** Prefer pointer + verification test over duplicate specification.  
**Updated:** 2026-07-16 (aligned to production-gate view)

| Status | Meaning |
|--------|---------|
| **Covered** | Existing source sufficient; implement/test against it |
| **Partial** | Spec exists; needs Phase B note or incomplete enablement |
| **Verify** | Believed covered; confirm against runtime |
| **Gap** | Genuinely missing; add a short pilot artifact only |

---

## Matrix

| Production gate | Existing source | Status |
|-----------------|-----------------|--------|
| Fail closed | Doctrine Bundle (constitutional fail-closed); v1.1 §8.5 | Covered |
| Audit log / provenance | Doctrine audit chain; v1.1 Provenance Trail; Peer Review proof integrity | Covered |
| Signed evidence | Doctrine signer authority; Eng Guide ProofPackage; v1.1 signatures | Partial — schema now; Doctrine-1B verify later |
| Proof / governance in execution identity | Whitepaper/v2.3; Peer Review Claims 3–4 | Partial — proof-native schema; behavior flagged |
| Channel default-deny | v1.1 Isolation; Flowchart | Covered |
| Network partition | Doctrine runtime / halt-recovery | Verify — single-node Vultr assumptions |
| Halt / kill switch | Doctrine HALTED / RECOVERY | Partial — pilot kill switch; dual-ADMIN recovery not in B |
| Rollback (deploy) | Ops/migration practice (thin in corpus) | Partial — image pin + kill switch |
| Rollback (governance tx) | Doctrine quorum/atomicity | Verify — out of B hot path |
| Monitoring / observability | Named in drafts; weak runbooks | Gap — short pilot observability note |
| Disaster recovery / backups | Doctrine recovery; Eng Guide HA sketch | Partial — Postgres restore drill (A5) |
| Clock trust | Doctrine Clock Trust | Partial — NTP + skew reject |
| Replay prevention | Doctrine Replay; Decision Token nonces (C) | Partial — idempotency + F9 in B |
| Secrets / keys | Doctrine Signer Authority | Partial — pilot secrets path |
| Soft-launch ACL | Thin in corpus | Gap — ACL note + S5 |
| Boundary prompt injection | Thin in corpus | Gap — S2 suite (tests, not new doctrine) |
| Capacity / what stops | Absent | Gap — Gate 0.5 |
| IP disclosure boundary | IP Framing Memo; Patent Brief; Provisional 64/072,487 | Partial — Gate 0.6 + counsel |
| Address model v1.1 vs v2.3 | v1.1 Architecture vs Eng Guide | Partial — freeze dotted form; optional alias |
| Classifier FP/FN | v1.1 H-ROUTE-1; Phase B eval | Partial — §4.1a objectives |
| Operator surface | Draft deferred dashboard | Gap — CLI (O1) |
| ADRs for irreversible choices | Absent as practice | Gap — Gate 0.9 / `adr/` |

---

## Implications

1. Do not create parallel doctrine for Covered rows — write tests.  
2. Freeze proof-native schema even where Signed evidence / Proof rows are Partial.  
3. Only Gap rows get new short artifacts.  
4. Verify network partition and governance rollback against single-node reality before claiming Covered.

When private eng docs with stable IDs (e.g. RR-####, Doctrine 8) are available, replace corpus citations with those IDs.
