# TronixMesh Actual-State Reconciliation v1.0

**Artifact type:** Evidence-backed inventory (fulfils Activation Directive §14 / §21, immediate-execution steps 5–6)
**Governing authority:** `TRONIXMESH_ACTIVATION_DIRECTIVE_v1.0` (FINAL RC LOCKED)
**Prepared:** 2026-08-16
**Method discipline:** RC-007 (two-dimensional status) · RC-009 (evidence-only; `UNKNOWN` when uncertain) · RC-010 (authoritative artifacts first) · RC-011 (verify key behavior; never expose key material) · §20 (no time estimates)

---

## 1. Scope of inspection (search domain)

**Accessible search domain:** this Git repository (`BuildTronixAI/tronixmesh`) at `origin/main` — repository
structure, Git history, source, and the Phase B test suite.

**NOT accessible from here (external search domain — do not conclude `MISSING`):** the BOB **Canonical
Manifest** system, the deployed **BOB/OpenClaw runtime**, any **RR-0056 PostgreSQL** deployment, the
**Runtime Specification** documents, and migration artifacts. Per RC-009, components that plausibly live
in those external systems are classified **`UNKNOWN`** ("search domain not sufficiently inspected"), **not
`MISSING`**. Only positive, in-repo findings are asserted as evidence-backed.

**Runtime evidence:** `cd python && pytest` → **15 passed** (also **15 passed** with
`TRONIX_VERIFY_SIGNATURES=1`), Python 3.12.3, pytest 9.1.1. Phase B primitives commit of record:
`51485d4`. No private key material exists in the repository (Ed25519 keys are generated at runtime by
`signing.py`); key **behavior** is verified via tests, key **material** is neither present nor exposed
(RC-011).

**Status legend.** Implementation ∈ {COMPLETE, PARTIAL, MISSING, DEFECTIVE, SUPERSEDED, UNKNOWN};
Verification ∈ {UNVERIFIED, STATIC-VERIFIED, TEST-VERIFIED, SHADOW-VERIFIED, PRODUCTION-VERIFIED}. No
component is `SHADOW-VERIFIED` or `PRODUCTION-VERIFIED` (no shadow/production environment exists yet).

---

## 2. Dependency-sequenced implementation table

Rows are ordered by Track A dependency sequence (A1→A13). Cells are terse; §3 holds extended evidence.

| Seq | Component | Canonical Authority | Impl | Verif | Evidence | Repo Location | Discovered Defects | Missing Evidence | Remaining Work | Dependency | Acceptance Gate | Blocks Cutover? | Owner | Next Gate |
|----|-----------|---------------------|------|-------|----------|---------------|--------------------|------------------|----------------|------------|-----------------|-----------------|-------|-----------|
| A1 | Runtime blocker closure | Runtime Spec (ext.) | UNKNOWN | UNVERIFIED | none in repo | — | none observed | External BOB runtime not accessible | Identify/close runtime blockers | — | Blockers closed | YES | External (BOB) | A1 closure |
| A1′ | Runtime Specification v1.1 | Runtime Spec / Manifest (ext.) | UNKNOWN | UNVERIFIED | not in repo | — | none observed | v1.1 doc not in repo; RC-003 keeps v1.0 normative until v1.1 hashed+entered | Identify + lock v1.1 requirements (separate approval) | A1 | v1.1 approved/hashed/entered | YES (before A9) | Chairman / Runtime Spec owner | v1.1 lock |
| A2 | Actual-state inventory | Activation Directive §14/§21 | COMPLETE | STATIC-VERIFIED | this document | `docs/activation/` | n/a | n/a | Chairman review of this table | A1 | Table produced + reviewed | (gate) | This agent → Chairman | Review this table |
| A3a | Coordinate addressing (`MeshCoordinate`) | Design Doctrine / Arch v2 (coordinate-native) | COMPLETE | TEST-VERIFIED | `test_coordinate.py` (3); `51485d4` | `python/tronixmesh/coordinate.py` | none observed | no shadow/prod exercise | Wire into Governance Gate | A1 | A9 | NO (support) | Track A | A6 |
| A3b | Envelope + Ed25519 signature (ADR-0004) | ADR-0004; Arch v2 | COMPLETE | TEST-VERIFIED | `test_envelope_adr0004.py` (sign/verify, tamper-fails, frozen fields) | `envelope.py`, `signing.py` | none observed | no shadow/prod exercise | Use in authorization-envelope path | A1 | A9 | NO (support) | Track A | A6 |
| A3c | Ed25519 signing key (behavior) | Arch v2 crypto layer | COMPLETE | TEST-VERIFIED | sign/verify/tamper via envelope tests; RC-011 behavior-only | `signing.py` | none observed | key **registry**/rotation/revocation/epoch not in repo (see A3d) | none for primitive | A1 | A9 | NO (support) | Track A | A3d |
| A3d | Key registry / identity system | Arch v2 identity; A3 | UNKNOWN | UNVERIFIED | not in repo | — | none observed | Registry/ownership/rotation/revocation/epoch live in ext. BOB runtime; not accessible. Presence of a key ≠ correct identity system (RC-011) | Verify (not rebuild) registry, rotation, revocation, epoch | A3c | Acceptance test of identity | YES | External (BOB) / Track A | A9 |
| A3e | Nonce ledger / replay protection | Design Doctrine (nonce ledger target); A6/A10 | UNKNOWN | UNVERIFIED | not in repo (all 11 modules inspected) | — | none observed | External BOB runtime not accessible; may exist there | Verify or implement nonce/replay ledger | A3d | A10 fault matrix (duplicate nonce, replay) pass | YES | External (BOB) / Track A | A10 |
| A3f | PostgreSQL store / `pg_store` | RR-0056; A3/A4 | PARTIAL | TEST-VERIFIED | SQLite chain in `provenance.py`; `test_provenance.py` (chain, tamper) | `python/tronixmesh/provenance.py` | Backend is SQLite (Phase B primitive), not Postgres | Postgres/`pg_store` deployment not in repo | Provide Postgres backend per RR-0056 | A1 | A4 property set | YES | Track A / External | A4 |
| A3g | Authorization-envelope validation | Arch v2; A6 | PARTIAL | TEST-VERIFIED | signature verify in `handoff.py` (flag-gated); bootstrap grants in `authority.py`; `test_handoff.py` | `handoff.py`, `authority.py`, `envelope.py` | Full authorization envelope (AUTHORIZE→INTENT, RC-005) not present; Decision Tokens deferred (Phase C per Phase B Slice) | RC-005/RC-006 wrapper absent (see A7) | Build authorization-envelope + INTENT path | A3b,A3c | A9 | YES | Track A | A6/A7 |
| A4 | RR-0056 Evidence Authority (hardened) | RR-0056; Arch v2 §12; A4 | PARTIAL | TEST-VERIFIED | append-only + `verify_chain` in `provenance.py`; `test_provenance.py` (2) | `python/tronixmesh/provenance.py` | SQLite hash-chain only; no SECURITY-DEFINER RPC, tenant chains, external anchoring, monotonic transactional commit at scale | Hardened Postgres RR-0056 not in repo | Harden per A4 property list (append-only, hash chain, attributable, signed-where-required, monotonic order, transactional, tamper-evident, replay/reconstruct) | A3f | A4 properties demonstrated | YES | Track A | A5 |
| A5 | Canonical state registry / CURRENT_STATE | Activation Directive A5; Manifest | UNKNOWN | UNVERIFIED | `registry.py` is a *coordinate/endpoint* registry, **not** a canonical state store | `python/tronixmesh/registry.py` (different component) | `registry.py` does not implement CURRENT_STATE | Canonical Manifest + CURRENT_STATE store live in ext. BOB system; not accessible | Provide README-FIRST → Manifest → derived CURRENT_STATE per A5 | A4 | Fail-closed on unknown/stale/conflicting authority | YES | Track A / External | A6 |
| A6 | Governance Gate (wired) | Activation Directive A6; Doctrine | PARTIAL | TEST-VERIFIED | fail-closed state machine `governance.py` (`transition`, `may_execute`); `test_governance.py` (happy path, illegal-transition fail-closed, reviewers-cannot-execute) | `python/tronixmesh/governance.py` | Kernel only; not assembled into a gate evaluating identity/policy/scope/delegation/expiry/capabilities/resources/nonce/state | Wired gate not in repo; ext. BOB execution-gate status UNKNOWN | Assemble Governance Gate over the A6 evaluation set | A3d,A3e,A5 | No component self-authorizes; gate enforces all A6 inputs | YES | Track A | A7 |
| A7 | Predictive Execution Wrapper (INTENT/RESULT) | Activation Directive A7; RC-005/RC-006 | UNKNOWN | UNVERIFIED | not in repo | — | none observed | INTENT/RESULT wrapper not in repo; ext. runtime not accessible | Build AUTHORIZE→DURABLE COMMIT(INTENT)→ACK→INVOKE→RESULT(5-type)→evidence | A6 | RC-005 ordering + RC-006 RESULT distinction | YES | Track A | A8 |
| A8 | One reversible production adapter | Activation Directive A8 | UNKNOWN | UNVERIFIED | not in repo | — | none observed | No adapter in repo; ext. not accessible | Build one narrow reversible adapter (idempotency, timeout, crash recovery, bounded compensation) | A7 | A10.5 real reversible effects pass | YES | Track A | A9/A10.5 |
| A9 | Acceptance tests | Activation Directive A9; Acceptance Test Plan (ext.) | PARTIAL | TEST-VERIFIED | **15** pytest tests pass (`python/tests/`); `51485d4` | `python/tests/` | **Directive A9 cites a "12-test" plan; repo has 15 passing tests** — reconcile canonical acceptance plan (flag for §25 final review) | v1.1-required tests not yet defined; no activation acceptance harness | Reconcile canonical plan; add v1.1 + safety-invariant tests | A1′,A4,A6,A7,A8 | Safety invariants pass, no waiver | YES | Track A / Chairman | A10 |
| A10 | Shadow production + fault injection | Activation Directive A10 | UNKNOWN | UNVERIFIED | not in repo | — | none observed | No shadow harness; ext. production traffic not accessible | Build shadow harness w/ synthetic/adversarial injection; freeze A10 threshold (Chairman) | A9 | RC-013 frozen exit gate | YES | Track A | A10.5 |
| A10.5 | Governed staging effect trial | Activation Directive A10.5 | UNKNOWN | UNVERIFIED | not in repo | — | none observed | No staging effect harness | Real reversible effects w/ crash-boundary + compensation tests | A10 | A10.5 exit gate | YES | Track A | Cutover |
| — | Channel + minimal-authority handoff | Phase B Slice; ADR-0001 | COMPLETE | TEST-VERIFIED | `test_handoff.py` (4: authority-gated increase, denied w/o grant, UNROUTABLE, same-sensitivity) | `channel.py`, `authority.py`, `handoff.py`, `registry.py` | none observed | Decision Tokens deferred (Phase C) | none for primitive | A1 | A9 | NO (support) | Track A | A6 |
| — | Coordinate registry (endpoint/health) | Phase B Slice | COMPLETE | TEST-VERIFIED | exercised via `test_handoff.py` (UNROUTABLE) | `python/tronixmesh/registry.py` | none observed | not a CURRENT_STATE store (see A5) | none | A1 | A9 | NO (support) | Track A | A6 |
| — | Feature flags | Phase B Slice | COMPLETE | TEST-VERIFIED | `TRONIX_VERIFY_SIGNATURES` exercised (handoff verify path) | `python/tronixmesh/flags.py` | none observed | none | none | A1 | A9 | NO (support) | Track A | A6 |
| — | BOB / OpenClaw production runtime | Operating Doctrine / Migration Plan (ext.) | UNKNOWN | UNVERIFIED | not in repo | — | none observed | External; not accessible | Inventory via BOB Canonical Manifest access | — | Migration Plan | YES | External (BOB) | A2 (ext.) |
| — | Canonical Manifest | Activation Directive A5 (ext.) | UNKNOWN | UNVERIFIED | not in repo | — | none observed | External BOB system; not accessible | Access + inspect | — | — | YES | External (BOB) | A2 (ext.) |
| — | Migration artifacts / OpenClaw Migration Plan | Migration Plan (ext.) | UNKNOWN | UNVERIFIED | not in repo | — | none observed | External; keep fallback language exactly as written therein | Access + inspect | — | — | YES | External (BOB) | A11 |

---

## 3. Extended evidence notes

- **`51485d4`** ("Phase B Gate 0 signed + T0 runtime (envelope, handoff, provenance)") is the commit of
  record for the Phase B primitives inventoried above.
- **Provenance store (`provenance.py`).** Append-only SQLite ledger with `prev_hash`/`entry_hash`
  chaining and `verify_chain`; `test_provenance.py` proves chain integrity and tamper detection. This is
  a Phase B **primitive**, not the hardened RR-0056 Postgres Evidence Authority (A4).
- **Governance (`governance.py`).** 12-state vocabulary; `transition` raises on illegal edges
  (fail-closed); `may_execute` restricts execution to `AUTHORIZED`/`EXECUTING`. This is the kernel for
  A6, not a wired Governance Gate.
- **Signing (`signing.py`).** Ed25519 (+ HMAC-SHA256) generate/sign/verify. Per RC-011, only **behavior**
  is reported; **no key material is present in the repository or exposed here.**
- **Acceptance-test discrepancy (defect flagged).** The directive's A9 references an "existing 12-test
  acceptance plan," but the repository currently has **15** passing tests. This is an
  evidence-vs-document discrepancy for the §25 frozen final review / Chairman disposition — **not**
  silently reconciled here.

---

## 4. Cutover-blocking summary

**Blocks BOB cutover (must reach passing evidence):** A1 runtime blockers · A1′ Runtime Spec v1.1 lock ·
A3d identity/key registry · A3e nonce/replay · A3f Postgres store · A4 RR-0056 hardening · A5 canonical
state registry · A6 Governance Gate · A7 Predictive Execution Wrapper · A8 reversible adapter · A9
acceptance tests · A10 shadow · A10.5 staging effects.

**Does not block (verified supporting primitives):** coordinate addressing, envelope+signature, signing
behavior, channel/authority handoff, coordinate registry, feature flags.

**Largest evidence gaps are external** (UNKNOWN pending BOB Canonical Manifest / runtime access), not
in-repo. The in-repo Phase B primitives are `TEST-VERIFIED`; none is `SHADOW-`/`PRODUCTION-VERIFIED`.

---

## 5. Next required gate

Per §21, the next step is **Chairman review of this table**. No new implementation (Epistemic v0.2,
Reconciliation engine, Cognitive Mesh, Track A rewrite, production adapter, architectural substitution)
begins until this inventory is reviewed and defect assessment is complete (RC-008). **No time estimates**
are provided (§20); remaining work is expressed as verified tasks and dependencies only. Access to the
BOB Canonical Manifest / deployed runtime is required to convert the `UNKNOWN` external rows into
evidence-backed status.

---

*End of Actual-State Reconciliation v1.0.*
