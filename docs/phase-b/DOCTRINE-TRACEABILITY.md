# Phase B — Doctrine / Spec Traceability Matrix

**Purpose:** Map production concerns to **existing** doctrine and specs before inventing new gates or docs.  
**Rule:** Prefer pointer + verification test over duplicate specification.  
**Updated:** 2026-07-16

Status legend:

| Status | Meaning |
|--------|---------|
| **Covered** | Existing doctrine/spec is sufficient; Phase B implements/tests against it |
| **Partial** | Spec exists but needs a Phase B-scoped note or verification |
| **Open** | Genuinely missing; Phase B must add a short artifact |
| **Verify** | Believed covered; confirm against runtime before freeze |

---

## Matrix

| Concern | Existing source (corpus) | Status | Phase B action |
|---------|--------------------------|--------|----------------|
| Fail-closed authorization | Doctrine Bundle v1.1 (constitutional fail-closed); v1.1 Architecture §8.5 | Covered | Test F3/F7/F10; do not rewrite doctrine |
| Audit / provenance trail | Doctrine audit chain; v1.1 Provenance Trail; Peer Review proof integrity | Covered | Implement hash chain + A1–A4 |
| Signed artifacts | Doctrine signer authority; Eng Guide ProofPackage; v1.1 envelope signatures | Partial | **Schema now** (signature blocks + proof refs); full Doctrine-1B verify later |
| Proof / governance identity in execution | Whitepaper/v2.3; Peer Review Claims 3–4; Eng Guide | Partial | Proof-native envelope fields (§1.2 plan); enable MeshResolver later |
| Channel / boundary default-deny | v1.1 Isolation topology; Flowchart | Covered | Channel rule engine + F7 |
| Network partition / node isolation | Doctrine runtime / halt-recovery sections | Verify | Confirm behavior for single-node Vultr pilot; document assumed model |
| Halt / kill switch | Doctrine HALTED / RECOVERY state machine | Partial | Pilot kill switch maps to halt semantics; dual-ADMIN recovery **not** required in B |
| Rollback (app deploy) | Migration / ops practice (weak in corpus) | Partial | Image pin + kill switch; ledger never rolled back |
| Rollback (governance / tx) | Doctrine quorum / atomicity notes | Verify | Out of B hot path; do not invent parallel rules |
| Observability | Named in Phase B draft / v1.1 perf; weak operational runbooks in corpus | Open | Short pilot observability note: metrics, traces, alert route |
| Disaster recovery / backups | Doctrine recovery procedure (crypto-era); Eng Guide HA sketch | Partial | Postgres backup/restore drill (A5); full dual-ADMIN recovery deferred |
| Clock trust | Doctrine Clock Trust | Partial | Single NTP + envelope skew reject for pilot |
| Replay prevention | Doctrine Replay; Decision Token nonces (Phase C) | Partial | Idempotency keys + F9 in B; full nonce doctrine with Decision Tokens in C |
| Secrets / key handling | Doctrine Signer Authority; Eng Guide KMS notes | Partial | Pilot secrets path + rotation runbook; hardware ceremony later |
| Soft-launch ACL / multi-user isolation | Thin in corpus | Open | Short ACL note + S5 test |
| Prompt injection at sensitivity boundary | Thin in corpus | Open | S2 adversarial suite (test artifact, not new doctrine) |
| Capacity / portfolio displacement | Absent | Open | Gate 0.5 table in plan |
| IP / patent disclosure boundary | IP Framing Memo; Patent Brief; Provisional 64/072,487 | Partial | Gate 0.6 decisions; counsel as needed |
| Address model (v1.1 vs v2.3 8-tuple) | v1.1 Architecture vs Eng Guide / Peer Review | Partial | Freeze v1.1 dotted form for pilot; optional alias field in schema (T3 Q11) |
| Classifier / routing SLOs | v1.1 H-ROUTE-1; Phase B draft P1 | Partial | Split P1a/P1b in plan |
| Operator surface | Deferred dashboard in draft | Open | Minimal CLI acceptance (O1) |

---

## Implications for Gate Design

1. **Do not** create a parallel “security doctrine” for Phase B — S-series tests bind to existing fail-closed / audit / signer concepts.  
2. **Do** freeze proof-native schema even where verification is Partial.  
3. **Do** write only the Open rows as short pilot artifacts (observability note, ACL note, injection suite, capacity table, IP boundary).  
4. **Verify** network partition and governance rollback assumptions against single-node Vultr reality before claiming Covered.

---

## Next Pass (Optional)

When private eng repo is available, replace “corpus PDF” citations with stable doc IDs (e.g. RR-####) and link commit SHAs. Until then, this matrix uses the uploaded May 2026 document set as the authority snapshot.
