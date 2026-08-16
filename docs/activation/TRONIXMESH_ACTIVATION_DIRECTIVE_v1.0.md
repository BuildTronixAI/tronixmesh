# TRONIXMESH ACTIVATION DIRECTIVE v1.0 — FINAL RC LOCKED

**Status:** READY FOR CANONICAL HASH & MANIFEST ENTRY
**Version:** 1.0 (28 RC patches integrated)
**Lock Authority:** Chris Leiser (Chairman)
**Lock Timestamp:** 2026-08-16 01:49 UTC
**Hash Domain Definition:** All content EXCEPT this Document Hash field
**Document Hash:** [COMPUTED AT MANIFEST ENTRY]

---

## EXECUTIVE SUMMARY

**Program Principle (Locked):** Get governance alive first. Make it intelligent second.

**Three Parallel Tracks:**
- **Track A — Production Critical Path:** Controls TRONIXMESH ALIVE milestone while permitting authorized parallel Track B and Track C work
- **Track B — Cognitive Mesh / Epistemic Development:** Proceeds without blocking Track A (except genuine safety/governance defects)
- **Track C — IP / Commercialization:** Calendar-constrained (May 22, 2027), proceeds independently

**Definition of TRONIXMESH ALIVE:**

BOB performs real production work through TronixMesh execution substrate such that:
1. Every governed external effect requires valid authorization under canonical policy
2. Authorization is durable (recorded as binding INTENT before external effect)
3. Every external effect is attributable (which authorization, which principal, which policy)
4. Result evidence is recorded after effect execution
5. The complete action chain is reconstructable from authoritative evidence without relying on BOB's self-report
6. **[RC-001] Interrupted or ambiguous executions are deterministically recoverable or escalated under canonical recovery policy without unauthorized re-execution**

**Recovery Questions (All Must Answer from Evidence):**
1. Who requested the effect?
2. Under what identity and authority?
3. Which policy/runtime versions governed it?
4. Was authorization valid?
5. Was INTENT durably committed before external execution began?
6. What external effect was attempted?
7. What evidence exists that it occurred or did not occur?
8. If execution stopped between INTENT and RESULT, is retry permitted?
9. What recovery or escalation state now applies?
10. Can all of this be established without trusting BOB's narrative?

If those questions cannot be answered from authoritative evidence, the execution is not cleanly governed.

---

## SECTION 1: PROGRAM DIRECTION — APPROVED

Overall direction approved. Do not reopen the program into another general architecture cycle.

The remaining work before canonical lock is:
- Finite precision and authority patch (this RC lock)
- Actual-state reconciliation (evidence-backed inventory)
- Gated implementation following dependency order

---

## SECTION 2: DEFINITION OF TRONIXMESH ALIVE — WITH RECOVERY (RC-001)

TRONIXMESH ALIVE occurs when:

**BOB performs real production work** through the TronixMesh execution substrate such that:

1. **Every governed external effect requires valid authorization** under canonical policy
2. **Authorization is durable** (recorded as binding INTENT before external effect)
3. **Every external effect is attributable** (which authorization, which principal, which policy)
4. **Result evidence is recorded** after effect execution
5. **Complete action chain is reconstructable** from authoritative evidence without relying on BOB's self-report
6. **Interrupted or ambiguous executions are deterministically recoverable** or escalated under canonical recovery policy without unauthorized re-execution

**Reconstructability Test:**

Given:
- Immutable authorization records
- Execution intent log
- Effect result evidence
- Policy version and governance rules

Can an independent observer reconstruct:
- What BOB proposed?
- Why it was authorized/denied?
- What actually happened?
- Why the outcome occurred?

If yes, TronixMesh is alive for that workload.

**Recovery Requirements:**

**[RC-001] Requirement:** System must answer from evidence alone:
1. Who requested the effect?
2. Under what identity and authority?
3. Which policy/runtime versions governed it?
4. Was authorization valid?
5. Was INTENT durably committed before external execution began?
6. What external effect was attempted?
7. What evidence exists that it occurred or did not occur?
8. If execution stopped between INTENT and RESULT, is retry permitted?
9. What recovery or escalation state now applies?
10. Can all of this be established without trusting BOB's narrative?

---

## SECTION 3: TRACK STRUCTURE (CONFIRMED)

### Track A — Production Critical Path

Sequence:
1. Runtime blocker closure (A1)
2. Actual-state inventory (A2)
3. Verify existing components (A3)
4. Harden RR-0056 Evidence Authority (A4)
5. Canonical state registry (A5)
6. Governance Gate (A6)
7. Predictive Execution Wrapper (A7)
8. One reversible production adapter (A8)
9. Acceptance tests (A9)
10. Shadow production + fault injection (A10)
11. Real reversible staging effects (A10.5)
12. Pre-cutover adversarial suite
13. Cutover-scope approval
14. BOB production cutover
**→ TRONIXMESH ALIVE**
15. Production attack phase (A12)
16. 30-day pre-registered proof (A13)
17. Hardening / scope expansion

**[RC-003] Dependency:** Runtime Specification v1.1 lock is on critical path (before A9)

### Track B — Epistemic / Cognitive Development (Parallel)

Sequence:
1. Epistemic Substrate v0.2
2. Executable acceptance tests
3. Four proof gates
4. Freeze v0.2
5. Reconciliation Protocol
6. Reconciliation Implementation
7. Belief graph / CURRENT_STATE integration
8. Calibration ledger
9. Single-model baseline establishment
10. Bounded Cognitive Mesh experiment

**Track B Does Not Block Track A** except for genuine defects affecting governance, authorization, identity, evidence integrity, execution safety, effect-commit semantics, or recovery.

**[RC-015] Propagation Rule:** Blocking findings propagate per dependency graph, not across entire program.

### Track C — IP / Commercialization (Calendar-Constrained)

**[RC-016] Hard Constraint:** May 22, 2027 (non-negotiable for non-provisional/PCT)

Sequence:
1. Prior-art/collision analysis (complete before claim drafting)
2. Counsel timeline (target: counsel actively drafting by Jan 2027)
3. Production evidence collection (Track A 30-day run provides reference)
4. Non-provisional/PCT filing (before May 22, 2027)
5. Commercialization positioning (after demonstrated operation + IP protection)

**[RC-016] Decoupling Rule:**
- Track A production evidence is desirable but NOT required for Track C filing
- Track C SHALL NOT relax Track A gate or delay IP deadline to obtain additional production evidence
- Do NOT rush production to create patent evidence
- Do NOT delay filing waiting for production

---

## SECTION 4: AUTHORITY MODEL — LOCKED (RC-002, RC-003)

Maintain two-stack distinction.

### Normative Authority (Non-Epistemic, Constitutional)

Governs:
- What actions permitted/denied
- Who may authorize
- What evidence required
- How effects commit
- Recovery semantics

### Epistemic Authority (Derived)

Governs:
- What TronixMesh believes true
- Confidence in propositions
- Observational evidence
- Prediction outcomes
- Calibration records

### Critical Separations (LOCKED)

1. Epistemic conclusions cannot grant execution permission
2. Governance cannot alter observed reality merely because observation conflicts with policy
3. Belief does not create authority. Governance does.

---

## SECTION 5: CANONICAL HASH RULE (RC-002)

**[RC-002] Adopted Rule:**

The canonical artifact hash SHALL be computed over the final locked content with the `Document Hash` field EXCLUDED from the hash domain.

The resulting hash SHALL be stored in the Canonical Manifest / authoritative artifact registry.

Any hash rendered inside a human-readable copy is informational and is NOT itself part of the authenticated hash domain.

**Hash-Domain Specification:**

Document exactly what bytes/content representation constitute the canonical hash domain before hashing.

BOB SHALL NOT improvise hashing semantics.

---

## SECTION 6: RUNTIME SPECIFICATION v1.0 → v1.1 AUTHORITY (RC-003)

**[RC-003] Adopted Rule:**

Runtime Specification v1.0 remains normative until Runtime Specification v1.1 is separately approved, authenticated, hashed, and entered into the Canonical Manifest.

This Directive may identify required v1.1 changes but SHALL NOT itself make those superior-specification changes normative.

No production gate dependent upon unresolved v1.1 semantics may be crossed until v1.1 is canonical.

**[RC-003] Critical Path Impact:**

Because A9 (Acceptance Tests) depends on v1.1 fixes:
- **Runtime Specification v1.1 lock is explicitly on Track A critical path**
- Critical path diagram MUST show this dependency (not prose only)

---

## SECTION 7: CHAIRMAN UNAVAILABILITY / FAIL CLOSED (RC-004)

**[RC-004] Adopted Rule:**

Chairman non-response SHALL NOT convert a blocking finding into approval.

**Escalation Timeline:**
- 24 hours: re-notification
- 72 hours: enter PENDING_CHAIRMAN_ESCALATION
- Affected scope: remains FAIL CLOSED throughout

No person or agent may acquire waiver authority merely because Chairman unavailable.

Delegated or successor authority is valid only if established canonically BEFORE relevant finding or emergency.

**Critical Rule:**
Do not invent emergency authority during an emergency. If future business-continuity succession desired, create it calmly and canonically in advance.

---

## SECTION 8: EPISTEMIC SUBSTRATE v0.1 VERDICT (UNCHANGED)

**Conceptual skeleton:** Coherent and merits continuation.

**Validation status:** NOT YET SOUND.

**Preferred characterization:**
> The conceptual skeleton is coherent and merits continuation. No fatal architectural defect has been identified in this review. The architecture is not considered validated as sound until repaired semantics survive executable acceptance testing.

**Adversarial review:** Authoritative for remediation.

---

## SECTION 9: CRITICAL EPISTEMIC REPAIRS (UNCHANGED)

### 9.1: Four Independent Claim Dimensions

```yaml
epistemic_status: SUPPORTED | REFUTED | UNDERDETERMINED | CONTESTED
admission_status: PROPOSED | ADMITTED | INADMISSIBLE
integrity_status: VERIFIED | DEGRADED | QUARANTINED
lifecycle_status: ACTIVE | SUPERSEDED | RETIRED
```

Do not overload one status enum.

### 9.2: Observation/Evidence ≠ Claim/Inference ≠ Normative Preference

Do not apply confidence semantics universally.

### 9.3: Digitally Verified Fact ≠ Externally Asserted Fact

**Constitutional Rule (LOCKED):**
> TronixMesh SHALL distinguish facts established by the trusted digital substrate from assertions about the external world. Cryptographic integrity, provenance, consensus, repetition, model agreement, or schema validity SHALL NOT be interpreted as proof that an external-world assertion is true.

### 9.4: Probability Estimate ≠ UNKNOWN

UNKNOWN is not 0.50. Use typed confidence with explicit method.

### 9.5: Epistemic Acceptance ≠ Execution Authorization

Governance gates execution. Governance must not suppress observations merely because implications conflict with governance.

---

## SECTION 10: GOVERNANCE-CONTRADICTION DEFECT (FINDING #1) (UNCHANGED)

**Exact Defect (Preserved):**

v0.1 simultaneously:
1. Requires governance not to be breached before CURRENT_STATE commit
2. Says governance constrains action rather than observation
3. Permits governance-conflicting beliefs
4. Treats governance contradiction as a quarantine condition

This is contradictory.

**Repair:**

1. **Governance-conflicting belief content remains epistemically admissible.**
2. **Governance system prevents execution.**
3. **Quarantine applies only to governance breaches, not conflicts.**

---

## SECTION 11: INTENT COMMITMENT BOUNDARY (RC-005)

**[RC-005] Required Ordering (PRECISE):**

```
AUTHORIZE
  ↓
DURABLE COMMIT(INTENT)
  ↓
ACKNOWLEDGE COMMIT
  ↓
INVOKE EFFECT
```

**Requirement:** Asynchronous write queued before effect is NOT sufficient.

**Failure Condition:** If system can crash after effect invocation while INTENT remains uncommitted, the design fails the evidence requirement.

---

## SECTION 12: RESULT SEMANTICS (RC-006)

**[RC-006] RESULT must distinguish:**

1. Invocation/transport return
2. Provider acknowledgement
3. Independently observed postcondition
4. Inferred outcome
5. Unresolved outcome

**Critical Rule:**
Never collapse "call succeeded" (HTTP 200) into "intended consequence occurred."

Provider returning HTTP 200 proves acceptance of request—NOT necessarily the ultimate real-world outcome.

---

## SECTION 13: ACTUAL-STATE INVENTORY TAXONOMY (RC-007)

**[RC-007] Do NOT use combined enum:** COMPLETE/VERIFIED

**Use Two Independent Dimensions:**

### Implementation Status
- COMPLETE
- PARTIAL
- MISSING
- DEFECTIVE
- SUPERSEDED
- UNKNOWN

### Verification Status
- UNVERIFIED
- STATIC-VERIFIED (code inspection, commit history)
- TEST-VERIFIED (acceptance tests pass)
- SHADOW-VERIFIED (shadow mode observation)
- PRODUCTION-VERIFIED (live operation)

**Valid combinations:**
- COMPLETE + UNVERIFIED
- PARTIAL + TEST-VERIFIED
- UNKNOWN + UNVERIFIED

**Critical distinction: MISSING vs UNKNOWN**
- MISSING: Evidence-backed conclusion component does not exist
- UNKNOWN: Search domain not yet sufficiently inspected

Failure to immediately find component does NOT establish it is MISSING. Use UNKNOWN.

---

## SECTION 14: INVENTORY MUST PRECEDE IMPLEMENTATION (RC-008)

**[RC-008] Locked Rule:**

After canonical activation, first executable work is:
**Actual-State Reconciliation**

**NO new implementation:**
- Epistemic v0.2
- Reconciliation engine
- Cognitive Mesh
- Track A rewrite
- Production adapter
- Architectural substitution

Until:
1. Dependency-sequenced inventory produced
2. Evidence reviewed
3. Defect assessment complete

**Inventory Must Include (Evidence-Backed):**
- Component name
- Required function
- Implementation status
- Verification status
- Repository location
- Commit/hash evidence
- Test evidence
- Runtime/deployment evidence
- Documentation evidence
- Acceptance-test evidence
- Dependencies
- Discovered defects
- Missing evidence
- Next required gate

Every COMPLETE claim must have evidence attached.

---

## SECTION 15: INVENTORY INTEGRITY (RC-009, RC-010, RC-011)

### RC-009: Do Not Contaminate with Inference

**Forbidden labels in formal state table:**
- "suspected MISSING"
- "probably complete"
- "appears implemented"

**Separate clearly:**
- Observed evidence
- Derived status
- Unresolved evidence
- Verification level

**Rule:** If you do not know, say UNKNOWN.

Evidence supersedes self-report. Unknown states fail closed.

### RC-010: Chairman Memory Not Evidence Source of First Resort

**Resolve from (in order):**
1. README-FIRST / bootstrap artifacts
2. Canonical Manifest
3. Repository structure
4. Git history
5. Deployment configuration
6. Registered runtime evidence
7. Authenticated records

Only escalate when those sources fail.

Human recollection may help locate evidence. It does NOT substitute for evidence.

### RC-011: Secrets and Key Material

**FORBIDDEN:**
- Expose private key material
- Print / copy / summarize / inventory / transmit key material

**VERIFY INSTEAD:**
- Key existence
- Algorithm
- Public-key correspondence
- Ownership
- Permission boundaries
- Signing behavior
- Registry state
- Rotation behavior
- Revocation behavior
- Key epoch/version
- Provenance

Presence of key is NOT evidence identity system is correct.

---

## SECTION 16: TRACK A — PRODUCTION / CRITICAL PATH

### A1: Close Runtime Blockers

Resolve remaining runtime invariants necessary for governed production execution.

**Particularly:**
- Effect-commit boundary (INTENT → effect → RESULT)
- INTENT-before-effect guarantee
- RESULT-after-effect recording
- Crash recovery semantics
- Provider-contract violations
- Compensation semantics
- Authorization failure behavior

Adopt Runtime Spec v1.1 when those resolved.

**Do NOT reopen unrelated architecture.**

### A2: Actual-State Inventory

**IMMEDIATE PRIORITY:** Before coding, inspect:

- Canonical manifest
- Repository structure
- Currently deployed BOB/OpenClaw runtime
- RR-0056 implementation status
- Identity/key infrastructure
- Nonce ledger implementation
- pg_store implementation
- Execution gate (partial?)
- Transport/security (partial?)
- Migration artifacts
- Acceptance tests (existing)

**[RC-007] For every component, classify using two independent dimensions:**
- Implementation Status (COMPLETE | PARTIAL | MISSING | DEFECTIVE | SUPERSEDED | UNKNOWN)
- Verification Status (UNVERIFIED | STATIC-VERIFIED | TEST-VERIFIED | SHADOW-VERIFIED | PRODUCTION-VERIFIED)

**Return:** Dependency-sequenced implementation table

### A3: Verify Existing Security Components

Verify rather than rebuild:
- Ed25519 identity
- Key registry
- Nonce/replay protection
- PostgreSQL store
- Authorization-envelope validation

Acceptance tests determine whether remediation required.

### A4: Harden RR-0056 Evidence Authority

Required properties:
- Append-only event semantics
- Hash chaining
- Attributable principals
- Signed records (where required)
- Monotonic authoritative ordering
- Transactional commits
- Tamper detection
- Replay/reconstruction capability

**Terminology:** Tamper-evident, NOT metaphysically "tamper-proof."

### A5: Canonical State Registry

**Architecture:**
- README-FIRST: non-normative bootloader (reads from Canonical Manifest)
- Canonical Manifest: identifies authenticated normative artifacts
- CURRENT_STATE: derived/reconciled, never self-declared
- Runtime: must reject or fail closed on unknown/stale/conflicting authority

### A6: Governance Gate

**Gate evaluates:**
- Identity
- Canonical policy
- Action scope
- Delegation
- Expiry
- Capabilities
- Resources
- Nonce/replay status
- Relevant state requirements

**Rule:** No model, reconciler, cognitive process, or epistemic component may grant itself execution authority.

### A7: Predictive Execution Wrapper

**[RC-005, RC-006] Sequence:**
```
1. Proposal arrives
2. Belief/context → prediction → expected observables → failure signals
3. Governance Gate evaluates authorization (canonical policy)
4. If authorized: [RC-005] AUTHORIZE → DURABLE COMMIT(INTENT) → ACKNOWLEDGE COMMIT → INVOKE EFFECT
5. External effect executed
6. [RC-006] RESULT distinguished (invocation | provider ack | observed postcondition | inferred | unresolved)
7. Evidence appended to Evidence Authority
8. Reconciliation updates epistemic state
```

### A8: One Production Adapter

Start deliberately narrow. Choose one useful, reversible digital execution domain.

**Required flow:**
```
proposal → authorization → INTENT → execute → RESULT → evidence
```

Support:
- Idempotency
- Timeout handling
- Crash recovery
- Provider-contract violation recording
- Bounded compensation

### A9: Acceptance Tests

Run existing 12-test acceptance plan + tests required by newly adopted Runtime v1.1 fixes.

**No waivers for safety-critical invariants:**
- Authorization enforced
- INTENT precedes effect
- RESULT recorded
- Recovery works
- Evidence reconstructable

### A10: Shadow Production (RC-009, RC-012, RC-013)

**[RC-012] Clarification:** Runtime observation during inventory is permitted where authorized.

DO NOT CONFUSE observation with A10 shadow execution.

**[RC-012] A10 Requirements:**
- Shadow proposal/execution testing occurs only at its designated gate
- A10 must support synthetic/adversarial proposal injection
- Normal traffic may not naturally produce: denied actions, escalations, replays, malformed authority, expired capability
- Shadow test suite observing ONLY normal traffic cannot prove denial behavior

**[RC-013] A10 Exit Gate (Frozen Threshold):**

```
100% coverage of every declared workload class
AND completion of every mandatory denial/escalation/adversarial scenario
AND either (≥100 representative effect-bearing requests OR ≥3 consecutive operating days)
AND Chairman approval of frozen A10 protocol before shadow begins
```

**Locked Rule:** Threshold pre-registered BEFORE shadow begins. Do NOT change denominator after observing results.

**Workload Coverage:**
- Every BOB workload class intended for initial cutover
- Representative allowed actions
- Representative denied actions
- Representative escalated actions
- Representative state-dependent actions
- Representative failure cases

**Decision Comparison:**
Every production external effect observed must have corresponding TronixMesh authorization disposition.

Every disagreement classified and dispositioned.

For safety-critical authorization: zero unresolved disagreement = cannot proceed.

**Fault-Injection Completion:**
- Verifier unavailable
- Stale canonical state
- Conflicting canonical state
- Duplicate nonce
- Replay attempt
- Malformed authorization envelope
- Invalid signature
- Expired delegation
- Excessive delegation scope
- Database interruption
- Evidence Authority unavailable
- Adapter timeout
- Provider response ambiguity
- Crash after INTENT before effect
- Crash after effect before RESULT
- Duplicate execution attempt
- Failed compensation
- Unresolved human escalation

### A10.5: Governed Staging Effect Trial

Before production cutover, run TronixMesh against real but isolated reversible execution environment.

**This SHALL execute actual effects.**

**Path:**
```
proposal
→ canonical-state verification
→ Governance Gate
→ authorization envelope
→ durable INTENT
→ actual external effect
→ RESULT
→ evidence append
→ reconstruction/reconciliation
```

**Test actual:**
- Successful execution
- Denied execution
- Duplicate request
- Crash after INTENT but before effect
- Crash after effect but before RESULT
- Restart/recovery
- Timeout
- Uncertain provider result
- Idempotent retry
- Compensation
- Failed compensation
- Human escalation

**A10.5 Exit Gate:**
Production cutover prohibited until:
- Actual reversible effects execute correctly
- No unauthorized effect occurs
- INTENT/RESULT reconstruction succeeds
- Incomplete-effect recovery per Runtime Spec
- Duplicate execution protection passes
- Compensation remains bounded
- Failed compensation escalates (not recursion)

### A11: BOB Production Cutover

When A10, A10.5, and adversarial gates pass:

Cut BOB over to TronixMesh.

**This event is: TRONIXMESH ALIVE**

OpenClaw remains controlled fallback during migration per approved Migration Plan.

**[RC-021, RC-022] Cutover Authorization:**

Cutover must be governed artifact with explicit allowlist/denylist.

**[RC-022] Cutover Scope Document must identify:**
- Allowed principals
- Allowed agents
- Allowed adapters
- Allowed effect classes
- Prohibited effect classes
- Consequence/value limits
- Capability boundaries
- Rollback/compensation availability
- Escalation conditions
- Policy/runtime versions
- Start/revision conditions

**Default v1 Posture:** Explicit allowlist; everything undeclared denied.

### A12: Production Attack Phase (RC-004, RC-012)

Post-cutover red-team comprehensive attack.

**Pre-Cutover Adversarial Suite (runs in A10/A10.5):**
- Prompt injection
- Policy-confusion attacks
- Attempted governance reinterpretation
- Forged principal identity
- Invalid credential
- Replay
- Nonce reuse
- Stale authorization
- Expired authorization
- Excessive delegation
- Poisoned evidence
- Forged provenance
- Circular evidence/self-confirmation
- Fabricated tool-result claims
- Model falsely claiming execution occurred
- Compromised/malicious adapter responses
- Contradictory state
- Unavailable authority
- Deliberate timing races
- Crash-boundary attacks
- Attempted compensation recursion

**Post-Cutover A12:**
Rerun applicable attack suite against actual production configuration.

Add attacks requiring live infrastructure characteristics.

Production attack testing respects blast-radius limits and doesn't deliberately create uncontrolled external harm.

### A13: 30-Day Pre-Registered Proof Period (RC-014, RC-025)

**[RC-025] A13 is NOT merely telemetry collection.**

Before 30-day run begins, create:
**TRONIXMESH_30_DAY_PROOF_PROTOCOL_v1.0**

Freeze evaluation criteria BEFORE observing final results.

#### Zero-Tolerance Criteria

**[RC-014] Unauthorized External Effects: 0**
- No governed external effect may occur without valid authorization under applicable canonical policy

**Evidence Reconstruction: 100%**
- Every sampled governed action must reconstruct successfully through authorization → INTENT → effect/result → evidence chain
- Sampling procedure declared before proof period
- Any action that cannot be reconstructed is a defect

**Unresolved Denials/Escalations: 0**
- Every denial and escalation must have final disposition or explicitly documented still-open state with accountable ownership
- No silent disappearance

**Evidence-Chain Integrity: 0 Known Undetected Mutations**
- No unexplained ledger discontinuity
- No unaccounted authoritative-state divergence

#### Operational Metrics (Pre-Registered)

Also measure:
- Runtime availability
- False-positive denial rate
- Human-intervention rate
- Mean escalation latency
- Failed execution rate
- Recovery success
- Adapter errors
- Provider ambiguity
- Latency overhead introduced by governance
- Evidence-writing overhead

**[RC-014, RC-025] Rule:** Either pre-register thresholds before proof period, OR explicitly label first 30 days as baseline measurement and use to establish prospective thresholds for next period.

Do NOT post-select success criteria.

---

## SECTION 17: TRACK B — EPISTEMIC / COGNITIVE DEVELOPMENT (RC-016, RC-017, RC-018, RC-020)

### B1: Epistemic Substrate v0.2

Rewrite v0.1 against adversarial review (locked).

**Traceability required:**
```
Finding → v0.2 Requirement → Schema/Algorithm → Acceptance Test
```

A finding is not closed because prose changed. It closes when repaired behavior is testable.

### B2: Executable Tests

Write tests before declaring substrate complete.

Test:
- State-space totality
- UNKNOWN as first-class state (non-collapsible)
- Governance-conflicting descriptive beliefs
- Immutable evidence with supersession
- Circular evidence detection/prevention
- Dependence behavior
- Calibration semantics
- Concurrency handling
- Failure closure
- Replay determinism

### B3: Proof Gates

Run four proof gates:
1. State-space totality
2. Authority uniqueness
3. Failure closure
4. Replay determinism

Only then freeze v0.2.

### B4: Reconciliation Protocol

Draft Reconciliation against v0.2 (never v0.1).

**Rule:** Reconciliation must NOT become a new governance authority. It derives epistemic state, period.

### B5: Reconciliation Implementation

Implement:
- Claim/evidence relationships
- Deterministic digital transitions
- Semantic-estimation boundaries
- Confidence methods
- Dependency handling
- Contradiction handling
- Concurrency semantics
- Evidence supersession propagation

### B6: Belief Graph / CURRENT_STATE Integration

Integrate derived epistemic state into CURRENT_STATE under canonical authority model.

**Rule:** No component self-declares CURRENT_STATE. Only reconciliation engine (under governance authority) produces authoritative mutations.

### B7: Calibration Ledger (RC-017)

Implement process-versioned calibration and immutable prediction/observation lineage.

**[RC-017] For calibration-bearing predictions: independent resolution is REQUIRED**

If independent resolution cannot be obtained:
- Retain prediction record
- Mark outcome accordingly
- Exclude from calibration statistics

Self-resolution cannot validate the predictor being measured.

Low-sample calibration may display but MUST be labeled provisional.

Do NOT let tiny sample size become strong-performance claim.

### B8: Single-Model Baseline

Establish null hypothesis before claiming collective intelligence value.

One strong model + same tools + same governance + same tasks.

Measure:
- Task success
- Accuracy
- Calibration
- Cost
- Latency
- Reliability
- Human intervention

### B9: Bounded Cognitive Mesh Experiment

Only after baseline established.

Test heterogeneous cognition with multiple channels providing genuinely different information or failure modes.

Compare against single-model baseline.

**Cognitive Kill Criterion (LOCKED):**
Heterogeneous TronixMesh cognition must materially outperform best single-model+tools baseline accounting for:
- Accuracy
- Calibration
- False confidence
- Latency
- Compute/API cost
- Reliability
- Human intervention
- Operational complexity

If not: stop or shelve Cognitive Mesh development.

Do NOT reinterpret failed experiment as success.

TronixMesh governance infrastructure has standalone commercial value. Cognitive Mesh must earn its complexity.

### B Epistemic Repairs (RC-013, RC-016)

**[RC-013] Quarantined Evidence:**

Quarantined evidence contributes zero epistemic weight in either direction until released.

Recompute epistemic status using admissible evidence only.

A claim may remain SUPPORTED while evidence item is QUARANTINED only if sufficient independent admissible evidence still supports belief.

**Add A12 adversarial test:**
Deliberately corrupt, taint, or attack contradictory evidence to force quarantine and artificially increase preferred claim support.

**Rule:** Quarantine cannot become evidence-laundering mechanism.

### B Work Authorization (RC-020)

**[RC-020] Clarify Anti-Churn Rule:**

Work expressly mandated by this Directive remains authorized.

Prohibition applies only to work OUTSIDE Directive's approved tracks, gates, repairs, tests, and required subordinate specifications.

**Do NOT refuse:**
- B1 / Epistemic v0.2
- B4 / Reconciliation Protocol
- Dependence-calculus work

By misreading the architecture freeze.

---

## SECTION 18: TRACK C — IP / COMMERCIALIZATION (RC-016, RC-018, RC-019)

### C1: Filing Deadline (Hard)

May 22, 2027 is non-negotiable for non-provisional/PCT strategy.

Do not allow engineering work to obscure unrecoverable filing deadline.

### C2: Prior-Art / Collision Work

Complete claim-by-claim collision analysis (including Provenact, other material prior art) sufficiently early to influence claim drafting.

Do NOT wait until filing week.

### C3: Counsel Timeline

Target counsel actively drafting by January 2027.
- Claim mapping: complete beforehand
- Collision analysis: substantially developed beforehand
- Filing strategy: counsel-controlled

### C4: Production Evidence

Track A 30-day production evidence becomes strategically valuable.

**[RC-016] Decoupling Rule:**
- Track A production evidence is desirable but NOT required for Track C filing
- Track C SHALL NOT relax Track A gate or delay IP deadline to obtain additional production evidence
- Do NOT rush production to create patent evidence
- Do NOT delay filing waiting for production

### C5: Commercialization & Disclosure (RC-018, RC-019)

TronixMesh may remain infrastructure.

Expose customer-facing outcomes:
- Provable audit trail
- Governed AI execution
- Attributable decisions
- Controlled delegation
- Recoverable execution
- Evidence-backed automation

**[RC-019] Public Disclosure Discipline:**

Until patent-coverage review complete, do NOT publish newer Cognitive Mesh details merely because abstract.

**Potentially claimable August concepts:**
- Shared epistemic state architecture
- Reconciliation engine mechanics
- Calibration of cognitive strategies
- Predictive execution/reconciliation loop
- Dependence-aware cognition
- Recursive cognition with non-recursive governance

**Assumption:** May filings cover governance and governed-collective-agent material, but do NOT assume they provide support for every later cognitive-architecture refinement.

**Rule:** External disclosure is an IP action. Treat accordingly.

Public strategic statements remain approval-required.

---

## SECTION 19: ARCHITECTURE DECISIONS

### Raft: Not Automatic v1 Requirement

Do NOT put Raft automatically on critical path.

Requirement is authoritative coordination/commit model, not particular consensus algorithm.

Determine whether PostgreSQL/RR-0056 can provide v1 requirements:
- Serialized authoritative writes
- Transactional transitions
- Monotonic ordering
- CAS/version enforcement
- Sufficient failover
- Fail-closed behavior when authority unavailable

If yes: use it.

Raft justified when architecture requires independently operating nodes to establish distributed consensus without relying on that authority.

Do NOT implement distributed-systems complexity merely to demonstrate sophistication.

### Kubernetes: Not v1 Requirement

Horizontal scaling not required for initial production TronixMesh.

Start with:
- Single reconciliation engine instance
- PostgreSQL backend
- One narrow execution adapter
- Basic monitoring

Kubernetes becomes justified when throughput/availability requirements cannot be met with simpler infrastructure.

---

## SECTION 20: SCHEDULING RULES

**Do NOT produce estimates** such as:
- "3–4 hours"
- "12–16 hours"
- "70–95 hours"
- "three developers for two weeks"

Until repository inspection identifies actual remaining work.

Those numbers represent **false schedule precision**.

After inventory, estimate only:
- Verified remaining tasks
- Dependencies
- Responsible owner
- Credible range
- Uncertainty
- Blocking risk

---

## SECTION 21: IMMEDIATE NEXT ACTIONS — AFTER RC LOCK

**Do NOT immediately start writing Epistemic v0.2.**
**Do NOT immediately build Reconciliation.**
**Do NOT create another high-level architecture roadmap.**

### First: Actual-State Reconciliation

Inspect repository and canonical manifest.

Return one **dependency-sequenced implementation table** containing:

| Field | Required |
|-------|----------|
| Component Name | |
| Canonical Authority | Governing spec/document |
| Implementation Status | COMPLETE \| PARTIAL \| MISSING \| DEFECTIVE \| SUPERSEDED \| UNKNOWN |
| Verification Status | UNVERIFIED \| STATIC-VERIFIED \| TEST-VERIFIED \| SHADOW-VERIFIED \| PRODUCTION-VERIFIED |
| Evidence | Commit/test/runtime evidence supporting status |
| Repository Location | Where to find it |
| Discovered Defects | What doesn't work |
| Missing Evidence | What can't be verified yet |
| Remaining Work | Exact work required |
| Dependency | What must exist first |
| Acceptance Gate | Objective pass/fail condition |
| Blocks BOB Cutover? | YES/NO |
| Owner | Responsible process/person |
| Next Required Gate | What's the next milestone |

**Rule:** No component is complete because:
- A file exists
- BOB remembers implementing it
- A previous report called it complete

Evidence supersedes self-report.

---

## SECTION 22: CHAIR TECHNICAL FINDING vs PROGRAM DISPOSITION (RC-023)

**[RC-023] Separate:**
- **Technical finding state:** Pass/fail from evidence (immutable)
- **Chairman program disposition:** Remediate/accept/restrict/stop (human decision)

**Rule:** Chairman governs DISPOSITION, not reality.

Failed replay-protection test remains failed even if program decision is to continue unrelated work.

Example:
- Technical finding: Replay-protection test FAILED
- Program disposition: CONTINUE unrelated work (where dependent only on other gates)

Do NOT say technical finding changed because disposition changed.

---

## SECTION 23: "DO NOT RESTART" MEANS VERIFY (RC-024)

**[RC-024] Clarify:** Existing components are presumed neither good nor bad.

**Rebuild only when evidence shows:**
- Canonical contradiction
- Governance/security defect
- Failed acceptance criterion
- Demonstrated implementation impossibility
- Explicitly authorized requirement demands replacement

**Do NOT rebuild because:**
- Different design cleaner
- Newer library exists
- Agent prefers another architecture
- Documentation imperfect

---

## SECTION 24: CHANGE MANIFEST FOR LOCK PATCH (RC-025)

**[RC-025] Lock patch SHALL ship with change manifest.**

For every authorized change provide:
- Change ID
- Affected section
- Original semantics
- New semantics
- Reason
- Source finding/review
- Expected dependency impact

**Verification:**
Authorized change list → actual diff → no unexplained edits.

No opportunistic cleanup riding inside lock patch.

---

## SECTION 25: FINAL REVIEW SCOPE — FROZEN (RC-026)

**[RC-026] After RC patch, exactly ONE final contradiction/integrity review.**

**Scope frozen BEFORE review begins.**

Checks ONLY:
- Internal contradictions
- Broken references
- Authority conflicts
- Undefined failure behavior
- Dependency inconsistency
- Terminology/status inconsistency
- Hash/manifest integrity
- Unauthorized patch drift

**NOT:** Another architecture ideation cycle

Do NOT use final review as opportunity to invent features.

---

## SECTION 26: POST-LOCK ARCHITECTURE RULE (RC-027)

**[RC-027] After lock:**

No discretionary architecture work authorized.

Work expressly mandated by Directive remains authorized.

Changes to canonical architecture require evidence of:
- Canonical contradiction, OR
- Governance/security defect, OR
- Failed acceptance criterion, OR
- Demonstrated implementation impossibility

AND SHALL proceed through canonical change control.

**Reopening triggers:**
- Contradiction
- Defect
- Failure
- Impossibility

**NOT:**
- Preference
- Elegance
- Curiosity
- New model suggesting alternative

---

## SECTION 27: TRACK A HEADING — CLARIFY PARALLELISM (RC-021)

**[RC-021] Track A heading:**

"Track A — Production Critical Path: controls the TRONIXMESH ALIVE milestone while permitting authorized parallel Track B and Track C work."

**Clarification:** Track A is critical to ALIVE but does not serially prohibit unrelated parallel work.

---

## SECTION 28: CHAIRMAN TECHNICAL FINDING vs DISPOSITION (RC-023)

**[RC-023] Authority Semantics:**

Chairman may decide:
- Remediate
- Accept defined risk where governance permits
- Restrict scope
- Stop
- Continue unrelated work

**The Chairman does not make failed evidence become passing evidence by declaration.**

Example:
- Failed replay-protection test remains failed
- Program decision may be to continue unrelated work
- But the test failure is not erased by the decision

Human authority governs DISPOSITION, not reality.

---

## SECTION 29: FINAL PROGRAM POSTURE

The intellectual work is no longer the bottleneck.

The next question is not:
> "Can TronixMesh be made more elegant?"

The question is:
> "What does authoritative evidence prove exists today, what does it prove works, and what minimum gaps remain between that state and a governed production effect?"

Proceed accordingly.

**Architecture expansion is over. Evidence begins now.**

---

## CHANGE MANIFEST (28 RC Patches)

| ID | Section | Original | New | Reason | Approval |
|----|---------|----------|-----|--------|----------|
| RC-001 | 1, 2 | ALIVE without recovery semantics | Add recovery semantics + reconstruction questions | Governance completeness | Chairman 01:49 |
| RC-002 | 5 | Self-referential hash | Exclude Document Hash field from domain | Security/authenticity | Chairman 01:49 |
| RC-003 | 6 | Directive supersedes v1.0 | v1.0 remains normative until v1.1 approved | Hierarchy clarity | Chairman 01:49 |
| RC-004 | 7 | Chairman required; no fallback | Fail closed if Chairman unavailable; escalation timeline | Governance continuity | Chairman 01:49 |
| RC-005 | 11 | "recorded before effect" | Precise: AUTHORIZE → COMMIT → INVOKE | Effect ordering | Chairman 01:49 |
| RC-006 | 12 | RESULT generic | Distinguish 5 outcome types | Evidence precision | Chairman 01:49 |
| RC-007 | 13 | Enum COMPLETE/VERIFIED | Two independent dimensions | State accuracy | Chairman 01:49 |
| RC-008 | 14 | No inventory first | Inventory precedes all implementation | Evidence priority | Chairman 01:49 |
| RC-009 | 15 | Inference in labels | Evidence-only labels (UNKNOWN if uncertain) | Precision | Chairman 01:49 |
| RC-010 | 15 | Chairman as primary source | Authoritative artifacts first; escalate if needed | Evidence hierarchy | Chairman 01:49 |
| RC-011 | 15 | No secrets protocol | Explicit: verify behavior, never expose keys | Security | Chairman 01:49 |
| RC-012 | A10 | Observation ≈ shadow test | Shadow testing at designated gate only; synthetic injection | Testing discipline | Chairman 01:49 |
| RC-013 | A10 | Loose threshold | Frozen pre-registered threshold | Precision | Chairman 01:49 |
| RC-014 | A13 | Zero tolerance soft | Reserve for absolute conditions; document unresolved | Language precision | Chairman 01:49 |
| RC-015 | Blocking | Propagate rhetorically | Propagate per dependency graph | Scope accuracy | Chairman 01:49 |
| RC-016 | Track C | Production evidence required for filing | Decoupled; production optional, deadline fixed | Separation of concerns | Chairman 01:49 |
| RC-017 | B7 | "where possible" independent | Required for calibration predictions | Validation integrity | Chairman 01:49 |
| RC-018 | B9 | Cognitive kill criterion vague | Materially outperform baseline or stop | Rigor | Chairman 01:49 |
| RC-019 | Track C | No disclosure protocol | Delay until patent review; treat as IP action | IP protection | Chairman 01:49 |
| RC-020 | Track B | Anti-churn muted B1/B4 | Mandate remains; prohibit only discretionary work | Work authorization | Chairman 01:49 |
| RC-021 | A heading | "BLOCKS NOTHING" | "Controls ALIVE while permitting parallel work" | Clarity | Chairman 01:49 |
| RC-022 | A11 | Vague cutover approval | Governed artifact with explicit allowlist/denylist | Precision | Chairman 01:49 |
| RC-023 | 23 | No finding/disposition separation | Technical finding ≠ program decision | Authority semantics | Chairman 01:49 |
| RC-024 | 22 | Vague "don't restart" | Rebuild only on evidence of defect/contradiction/impossibility | Maintenance discipline | Chairman 01:49 |
| RC-025 | 24 | No lock-patch manifest | Ship with change manifest (25 rows) | Audit trail | Chairman 01:49 |
| RC-026 | 25 | Open-ended review scope | Scope frozen; checks only contradictions/integrity | Review discipline | Chairman 01:49 |
| RC-027 | 26 | Vague reopen triggers | Only contradiction/defect/failure/impossibility | Architecture freeze | Chairman 01:49 |
| RC-028 | 21 | Prior response errors | Correct MISSING→UNKNOWN, remove estimate, clarify ACTIVE | Correction | Chairman 01:49 |

---

## SIGNATURE & HASH

**Status:** READY FOR CANONICAL HASH COMPUTATION & MANIFEST ENTRY

**Document Hash (RC-002):** [COMPUTED AT MANIFEST ENTRY — Document Hash field excluded from hash domain]

**Lock Authority:** Chris Leiser (Chairman)
**Lock Timestamp:** 2026-08-16 01:49 UTC

---

## IMMEDIATE EXECUTION (AFTER HASH & MANIFEST ENTRY)

1. Compute canonical hash (Document Hash field EXCLUDED)
2. Document hash-domain specification
3. Enter hash + artifact into Canonical Manifest
4. Lock Runtime Specification v1.1 requirements
5. Perform Actual-State Reconciliation
6. Return dependency-sequenced implementation table with all evidence

---

**END OF TRONIXMESH ACTIVATION DIRECTIVE v1.0 — FINAL RC LOCKED**

Ready for canonical hash computation and Canonical Manifest entry.
