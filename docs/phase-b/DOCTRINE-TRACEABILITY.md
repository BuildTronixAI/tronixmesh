# Phase B — Doctrine-to-Gate Traceability Matrix

**Artifact role:** Gate 1 — highest-leverage remaining governance artifact  
**Purpose:** Authoritative map so every production requirement answers: *missing, or already specified?*  
**Rule:** Prefer pointer + test over new documentation. One matrix; no parallel checklists.  
**Plan state contribution:** Required to exit **Conditionally Ready** → **Architecture Complete** / **Production Ready**  
**Updated:** 2026-07-17

## Status legend

| Status | Meaning | Gap column |
|--------|---------|------------|
| **Covered** | Source specifies the requirement; Phase B implements/tests against it | No |
| **Partial** | Source exists; Phase B scope or enablement incomplete | Partial |
| **Pending** | Decision/source exists but not accepted yet | Yes |
| **Verify** | Believed covered; confirm against runtime before freeze | Verify |
| **Missing** | No authoritative source | Yes |

---

## Matrix

| Requirement | Source | Section / ID | Status | Gap |
|-------------|--------|--------------|--------|-----|
| Fail closed | Doctrine Bundle v1.1 (“Doctrine 8” / constitutional fail-closed); v1.1 Architecture | Fail-closed design; §8.5 Recovery Principles | Covered | No |
| Audit trail / provenance | Doctrine audit chain; v1.1 Provenance Trail; Peer Review (“RR-0056”-class audit/proof integrity) | Audit ledger; proof integrity tests | Covered | No |
| Signed evidence — **schema** | **ADR-0004** (Accepted); Doctrine Signer Authority; Eng Guide ProofPackage | Envelope signature block fields | Covered | No |
| Signed evidence — **verify behavior** | Doctrine-1B; Eng Guide proof.verify | Feature-flagged in Phase B | Partial | Partial |
| Proof-native envelope fields | ADR-0001; Whitepaper/v2.3; Peer Review Claims 3–4 | Schema + flags | Covered | No |
| Channel default-deny | v1.1 Isolation topology; Flowchart | Channel rules | Covered | No |
| Network partition | Doctrine runtime / halt-recovery | Single-node Vultr assumptions | Verify | Verify |
| Halt / kill switch | Doctrine HALTED → RECOVERY | Pilot kill switch maps; dual-ADMIN recovery deferred | Partial | Partial |
| Rollback (deploy) | Migration / ops practice; Phase B plan §12 | Image pin + kill switch; ledger append-only | Partial | Partial |
| Rollback (governance tx) | Doctrine quorum / atomicity | Out of Phase B hot path | Verify | Verify |
| Monitoring / observability | Operations (thin in corpus); Phase B O5 | Correlation IDs required; full runbook | Missing | Yes |
| Disaster recovery / backups | Doctrine recovery; Eng Guide HA; Phase B A5 | Postgres restore drill in B; full dual-ADMIN later | Partial | Partial |
| Clock trust | Doctrine Clock Trust | NTP + envelope skew reject | Partial | Partial |
| Replay prevention | Doctrine Replay; Decision Token nonces (Phase C); Phase B F9 | Idempotency in B; full nonce doctrine in C | Partial | Partial |
| Secrets / key handling | Doctrine Signer Authority; ADR-0004 key_id model | Pilot secrets path + rotation runbook | Partial | Partial |
| Soft-launch ACL | Phase B S5 (no prior doctrine ID) | Short ACL note + test | Missing | Yes |
| Boundary prompt injection | Phase B S2 (no prior doctrine ID) | Adversarial suite (tests, not new doctrine) | Missing | Yes |
| Capacity / what stops | Phase B Gate 0.5 | Displacement table | Missing | Yes — fill at Gate 0 |
| IP disclosure boundary | IP Framing Memo; Patent Brief; Provisional 64/072,487; Gate 0.6 | Counsel-aware decisions | Partial | Partial — close Gate 0.6 |
| Address model | v1.1 Architecture (dotted); Eng Guide (8-tuple) | Freeze v1.1 for pilot; optional alias | Partial | Partial |
| Classifier FP/FN | v1.1 H-ROUTE-1; Phase B §4.1a | Objectives defined | Covered | No |
| Operator surface | Phase B O1 | CLI required; full UI deferred | Partial | Partial |
| Staged rollout | Phase B §9 | R1→R4 defined | Covered | No |
| Technology registry | `registry/TECHNOLOGY.md` | Approved/rejected/experimental | Covered | No |
| Irreversible architecture decisions | `adr/` (ADR status is sole lifecycle source) | Gate 0.9 | Covered | No |
| Decision Log (separate table) | — | **Rejected** — would duplicate ADR status | Covered (by rejection) | No |

---

## Genuine gaps (Gap = Yes) — ordered work

| # | Gap | Artifact to add (keep short) | Owner |
|---|-----|------------------------------|-------|
| 1 | Monitoring / observability | Pilot observability note: metrics, traces, alert route | Chris |
| 2 | Soft-launch ACL | ACL note + S5 test cases | Robert / Chris |
| 3 | Boundary prompt injection | S2 adversarial suite (tests) | Robert |
| 4 | Capacity / what stops | Fill Gate 0.5 displacement table | Chris |
| 5 | IP disclosure (Partial→close) | Gate 0.6 answers + counsel as needed | Chris |

**Verify rows** (network partition, governance rollback): confirm against single-node Vultr before claiming Covered — do not write new doctrine.

---

## Implications

1. **Signed evidence schema** is Covered via ADR-0004 Accepted — not Pending.  
2. **Signed evidence verify** remains Partial (feature-flagged) — intentional.  
3. Do **not** create a separate Decision Log; ADR `Status` field is the only lifecycle source.  
4. Complete Gap rows above before additional architectural invention.  
5. When private eng IDs (Doctrine 8, RR-0056, etc.) are linked in-repo, replace corpus aliases in the Source column with those stable IDs — do not fork a second matrix.

---

## Exit criterion

This matrix is **complete for Gate 1** when:

- [x] Requirement → Source → Status → Gap columns exist for all Phase B production gates  
- [x] ADR-0004 schema decision reflected as Covered (not Pending)  
- [ ] Gate 0.5 / 0.6 filled (operational, not architectural)  
- [ ] Missing-row short artifacts drafted or explicitly deferred with owner  

Architectural Gate 1 (matrix + ADR-0004) can close independently of Gate 0.5/0.6 fill-in.
