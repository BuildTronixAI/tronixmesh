# TronixMesh — Comprehensive Architecture Write-Up

**Status:** Working reference document (v2.0 draft)  
**Owner:** Christopher Channing Leiser / L2R Holdings LLC / Buildtronix AI Corp  
**IP Basis:** US Provisional Patent 64/072,487, filed 05/22/2026 (non-provisional + Paris Convention deadline 05/22/2027)  
**Classification:** Working reference — review against patent claims before any external disclosure  
**Recorded in-repo:** 2026-07-17  
**Related:** [`TRONIXMESH-DESIGN-DOCTRINE.md`](./TRONIXMESH-DESIGN-DOCTRINE.md) · [`PHASE-B-SLICE.md`](./PHASE-B-SLICE.md) · Phase B plan · Doctrine Bundle v1.1

---

## 1. What TronixMesh Is

TronixMesh is not an AI agent framework. It is a **governance runtime** whose purpose is to make autonomous AI systems provably trustworthy by separating reasoning from authority. The design philosophy in one line:

> **Agents reason. The runtime governs. Humans retain ultimate authority.**

Unlike LangGraph, AutoGen, CrewAI, or OpenAI Swarm, TronixMesh treats the LLM as **untrusted compute**. The model produces recommendations; it is never the source of authority. The runtime owns state, permissions, identity, governance, evidence verification, and policy execution.

---

## 2. Coordinate-Native Governance (The Patented Core)

*This is the defining innovation and the subject of the provisional patent — it must anchor any comprehensive description.*

TronixMesh uses **fractal coordinate addressing**: every agent, resource, capability, decision, and audit record is assigned a coordinate within a hierarchical address space. Governance is not bolted on as middleware — it is **embedded at the coordinate level**, meaning:

- An agent's coordinate encodes its position in the authority hierarchy, its permitted scope, and its isolation boundary.
- Any operation carries **embedded enforcement proof**: the runtime can verify, from the coordinate and its cryptographic lineage alone, that the operation was authorized within scope — without consulting the model or trusting agent-reported state.
- Coordinates make governance **composable and fractal**: the same enforcement semantics apply at any depth (a single tool call, an agent, a tenant, an entire mesh), so adding agents or tenants never requires redesigning the governance layer.

This is the claim that distinguishes TronixMesh from every conventional framework: governance is a property of the address space itself, provable at enforcement time, rather than a policy check layered over an unmodeled agent graph.

---

## 3. Four Topology Layers

The mesh is organized as four orthogonal topology layers, each with its own invariants:

1. **Authority topology** — who may authorize what, expressed as the tiered authority model (Section 5) and Decision Tokens.
2. **Routing topology** — how work, messages, and escalations move between agents, reviewers, and humans; includes the outbox queue and Dead Letter Queue semantics.
3. **Memory topology** — where state lives, who may read/write it, and how it is checkpointed and recovered (Section 14).
4. **Isolation topology** — capability and tenant boundaries; no agent, model, or tenant can observe or affect another's coordinate space without an explicit, tokenized grant.

Governance conclusions must hold across all four layers simultaneously; an operation valid in the authority layer but violating isolation fails closed.

---

## 4. High-Level Architecture

```
                    Human Authority
                           │
                  Chairman / Operators
                           │
                    Decision Tokens
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
 Governance Engine                    Policy Engine
         │                                   │
         └──────────────┬────────────────────┘
                        │
              Runtime Enforcement Layer
              (coordinate-native, fail-closed)
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
   BOB Runtime      Robert Runtime     Council
  (Execution)       (Planner)        (Reviewers)
      │                 │                 │
      └──────────────┬──┴─────────────────┘
                     │
             Tool Execution Layer
                     │
     Databases • APIs • Telegram • Git • Claude
```

---

## 5. Tiered Authority Model (Tier 0–4)

Authority is explicit and tiered rather than implicit. **Tier 0** is human sovereignty — the Chairman/operator level that cannot be overridden, delegated away, or redefined by any AI component. Descending tiers hold progressively narrower, revocable authority, down to individual tool invocations. Every Decision Token binds to a tier; the runtime refuses any operation whose token tier is insufficient for the capability's risk class. **HITL approval gates** are the mechanism by which operations cross tier boundaries: risk-classed capabilities (spend money, modify production, delete records, communicate as the principal) require a human-issued or human-delegated token before the governance state machine can advance to AUTHORIZED.

---

## 6. Governance Engine and State Machine

Every significant operation progresses through a governance state machine. The full state vocabulary is richer than approve/deny:

`DRAFT → PROPOSED → UNDER_REVIEW → CPR (Conditional Pending Review) → APPROVED → AUTHORIZED → EXECUTING → EXECUTED → VERIFIED → SEALED`, with `BLOCKED` and `ROLLED_BACK` as terminal/recovery branches.

The runtime refuses execution if governance requirements are not satisfied. Runtime behavior is state-dependent: a SEALED record is immutable; a BLOCKED operation cannot be retried without a new proposal; ROLLED_BACK operations leave their full audit lineage intact.

---

## 7. The Doctrine Bundle (Nine Doctrines)

The runtime principles are formalized as the **TronixMesh Doctrine Bundle** — nine doctrines that have each passed adversarial review cycles. At minimum:

**Fail Closed.** If anything cannot be verified, stop. Never continue on assumptions.

**Human Sovereignty.** Humans always outrank AI. AI cannot redefine governance, remove approvals, change policy, or bypass humans.

**Reviewer Independence.** Reviewers recommend; they never execute. No Council member holds execution authority.

**Separation of Reasoning and Authority.** LLM output flows through recommendation → runtime validation → policy verification → evidence verification → Decision Token → execution. Reasoning and authority never merge.

**Halt & Degraded State (Doctrine 8).** The system defines explicit degraded operating modes rather than binary up/down. When invariants are threatened (auth failure, audit chain break, checkpoint corruption), the runtime transitions to a degraded state with reduced capability grants and mandatory human notification, and defines the conditions under which a halted mesh may resume. This prevents the failure mode where an agent silently continues with partial governance.

*(The remaining doctrines cover evidence, audit, capability enforcement, and identity — the Doctrine Bundle document is the authoritative source and should be attached as an appendix to any external version of this write-up.)*

---

## 8. Conscience Layer: Witness and Little Voice

From the BOB governance specs (v3.2–v3.4), TronixMesh includes a **constitutional conscience layer** that conventional frameworks lack entirely:

- **Witness** — an independent observer module that records what an agent actually did (not what it reported doing), producing observation hashes that feed the evidence model. Witness output is compared against agent self-reports; divergence triggers governance escalation.
- **Little Voice** — an in-loop conscience module that evaluates proposed actions against the doctrine bundle *before* they reach the governance engine, providing early refusal and flagging rather than relying solely on post-hoc enforcement.

Together these implement defense-in-depth: the model is checked by its conscience module, the conscience is checked by the runtime, the runtime is checked by the audit chain, and the audit chain is verifiable by humans.

---

## 9. Accountability Runtime: Focus Heartbeat System

The **BOB Focus Heartbeat System (v1.4)** governs agent liveness and accountability. Every agent operates under a heartbeat state machine; missed or malformed heartbeats transition the agent toward degraded state per Doctrine 8. **Force-testing protocols** deliberately inject failure conditions (revoked tokens, stale evidence, broken chains) to verify that enforcement actually fires — governance that is never tested is assumed broken. This converts "the runtime enforces policy" from a design claim into a continuously verified property.

---

## 10. Capability System

Capabilities (read filesystem, read database, send email, spend money, modify production, deploy code, delete records, human communication) are classified, and each carries an owner, risk class, approval requirements, audit trail, and rollback policy. The model cannot elevate itself; capability grants exist only as coordinate-scoped, token-bound runtime objects.

---

## 11. Decision Tokens

Rather than "Claude approved this," TronixMesh issues cryptographically verifiable authorization objects containing the request, approver, timestamp, governance version, policy version, scope, expiration, and signature. Execution requires a valid, unexpired, in-scope token. Tokens are single-purpose and replay-protected via the nonce ledger.

---

## 12. Cryptographic and Audit Layer (RR-0056)

The audit chain is not aspirational — it has a concrete reference implementation, **RR-0056**:

- Append-only PostgreSQL audit log; no UPDATE or DELETE paths exist for audit rows.
- Writes occur only through a **SECURITY DEFINER RPC**, so no client role — including service roles — can write audit records directly or bypass chain construction.
- **Hash chaining**: each record commits to the hash of its predecessor, making insertion, deletion, or reordering detectable.
- **Tamper-evidence layering**: chain verification, row-level integrity, and (planned) external anchoring via RFC 3161 timestamping, so tampering requires compromising multiple independent layers.
- **Tenant-scoped hash chains**: in multi-tenant deployment, each tenant's audit lineage is independently verifiable without exposing other tenants' records — proven in the OeniVault/Clover event-ledger implementation, which shares this architecture.

Additional cryptographic controls: Ed25519 signatures, nonce protection, replay prevention, immutable audit history, per-operation JWTs, identity-bound execution.

---

## 13. Evidence Model

Actions require evidence: git commits, database snapshots, test results, policy versions, architecture decision records, review packages. Evidence is hashed before approval; any subsequent change to the evidence invalidates prior approvals, forcing re-review. Witness observation hashes (Section 8) are first-class evidence.

---

## 14. Memory and Recovery Architecture

The platform moved away from JSON memory toward **SQLite WAL** due to concurrency and corruption concerns. Current direction: append-only events, semantic hashes, observation hashes, a state registry, an outbox queue, a recovery journal, and checkpointing (SqliteSaver in the Robert reference implementation). The long-term goal is **deterministic recovery after crashes** — a restarted mesh reconstructs exactly the governance state it held at failure, and the recovery itself is an audited event.

---

## 15. Multi-Agent Roles

**BOB** — operational executor and chief of staff: Telegram, tools, monitoring, execution, reporting. Runs on the OpenClaw gateway.

**Robert** — architect/planner (LangGraph reference implementation): StateGraph with SqliteSaver checkpointing, six nodes (Planner, Architect, Coder, Executor, Reviewer, Deliverer), a dedicated Policy Engine, Dead Letter Queue, and LLM cost metering. Robert demonstrates that a conventional agent graph can be placed *under* the TronixMesh runtime rather than beside it.

**Council** — independent reasoning models (GPT, Claude, Gemini, Grok) for disagreement, adversarial review, consensus, and failure-mode identification. The Council spec (v1.5) adds **signed audit chains for deliberations**: every Council opinion, dissent, and consensus outcome is itself a chained, attributable record — review is auditable, not just execution.

No model is automatically trusted; each remains independent and interchangeable.

---

## 16. Security Model Summary

Per-operation JWTs, identity-bound execution, nonce ledgers, replay protection, immutable audit records, least privilege, capability isolation, fail-closed defaults, service-role isolation, execution authorization, SSRF mitigation, credential scrubbing, audit-log atomicity, and RLS policies including DELETE protection (hardened through the v1.3 security patch cycle).

---

## 17. Trust Model

```
Human → Governance → Runtime → Evidence → Policies → Agent → LLM
```

The LLM is deliberately at the bottom of the trust stack.

---

## 18. Differentiation

| Feature | Conventional Frameworks | TronixMesh |
|---|---|---|
| Coordinate-native governance w/ enforcement proof | No | **Yes (patented)** |
| Runtime owns authority | No | Yes |
| Cryptographic approvals (Decision Tokens) | Rare | Yes |
| Governance state machine | Minimal | Extensive (12 states) |
| Formal doctrine bundle | No | Yes (9 doctrines) |
| Conscience modules (Witness / Little Voice) | No | Yes |
| Heartbeat + force-tested enforcement | No | Yes |
| Degraded-state semantics | No | Yes (Doctrine 8) |
| Tenant-scoped verifiable audit chains | No | Yes |
| Human sovereignty | Implicit | Explicit (Tier 0) |
| Reviewer independence | Rare | Doctrine |
| Fail-closed architecture | Partial | Core principle |

---

## 19. IP Position

US Provisional 64/072,487 (coordinate-native governance with embedded enforcement proof) filed 05/22/2026 with no prior public disclosure — international novelty preserved. Non-provisional and Paris Convention filings due by **05/22/2027**. TronixMesh sits within a broader P1–P11+ portfolio spanning construction tech, AI governance, personal identity, IoT mesh, and emergency response. Any public write-up derived from this document should be reviewed against the patent claims before disclosure.

---

## 20. Long-Term Vision

The end state is a **governed AI operating system**: multiple specialized agents operating concurrently under a runtime that enforces policy independently of any model, with cryptographically verifiable approvals and execution records, human authority preserved at Tier 0, and recovery, rollback, and auditability built in. Models are interchangeable reasoning engines; identity, permissions, execution, evidence, and governance live in a deterministic, coordinate-native runtime. That separation is the central idea that ties the project together — and the coordinate-native enforcement proof is what makes it defensible, both architecturally and as intellectual property.

---

*End of TronixMesh Comprehensive Architecture Write-Up v2.0 draft.*
