# TronixMesh Design Doctrine

**Document type:** Authoritative design philosophy  
**Status:** Normative north star (implementation is phased)  
**Authority:** Christopher C. Leiser, Chairman  
**Recorded:** 2026-07-17  
**Related:** [`TRONIXMESH-ARCHITECTURE-v2.md`](./TRONIXMESH-ARCHITECTURE-v2.md) (comprehensive write-up) · Phase B plan · Doctrine Bundle v1.1 · ADRs · [`PHASE-B-SLICE.md`](./PHASE-B-SLICE.md)

---

## What TronixMesh Is

TronixMesh is **not** simply an AI agent framework. It is a **governance runtime** whose purpose is to make autonomous AI systems provably trustworthy by **separating reasoning from authority**.

### Design philosophy (one line)

> **Agents reason. The runtime governs. Humans retain ultimate authority.**

### Patented core (must not be omitted)

**Coordinate-native governance with embedded enforcement proof** (US Provisional 64/072,487): fractal coordinates embed authority scope and isolation; enforcement is provable from coordinate + cryptographic lineage without trusting the model. Full treatment: Architecture Write-Up §2.

Unlike LangGraph, AutoGen, CrewAI, or OpenAI Swarm, TronixMesh treats the LLM as **untrusted compute**. The LLM is never the source of authority.

| The runtime owns | The model produces |
|------------------|--------------------|
| State | Recommendations |
| Permissions | Drafts |
| Identity | Analysis |
| Governance | Plans |
| Evidence verification | Suggestions |
| Policy execution | — |

---

## Architecture

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

### Multi-agent view

```
             Chairman
                 │
          Human Authority
                 │
          Decision Token
                 │
        ┌────────┴────────┐
        │                 │
      BOB             Robert
  Operational      Deep Reasoning
        │                 │
        └───────┬─────────┘
                │
            Council Layer
      GPT • Claude • Gemini • Grok
                │
        Consensus / Dissent
                │
         Runtime Enforcement
```

Each model remains independent. **No model is automatically trusted.**

---

## Primary Components

### 1. Runtime Layer

The operating system for agents. **No agent bypasses runtime.**

Responsibilities:

- Lifecycle management  
- Identity  
- Capability enforcement  
- Policy execution  
- Retries / recovery / checkpoints  
- Telemetry  
- Audit logging  

### 2. Governance Engine

Defining feature. Significant operations progress through a governance state machine. The runtime **refuses execution** if governance requirements are not satisfied.

### 3. Capability System

Capabilities are classified (examples: read filesystem, read database, send email, spend money, modify production, deploy code, delete records, human communication).

Each capability has: owner · risk class · approval requirements · audit trail · rollback policy.

**The model cannot elevate itself.**

### 4. Decision Tokens

Not “Claude approved this.” Cryptographically verifiable authorization objects containing:

- request · approver · timestamp  
- governance version · policy version  
- scope · expiration · signature  

**Execution requires a valid token.**

---

## Runtime Principles (Foundational Doctrines)

### Fail Closed

If anything cannot be verified: **STOP**. Never continue on assumptions.

### Human Sovereignty

Humans always outrank AI. AI cannot:

- redefine governance  
- remove approvals  
- change policy  
- bypass humans  

### Reviewer Independence

Reviewers **recommend**. They **never execute**.

### Separation of Reasoning and Authority

```
LLM
 ↓
Recommendation
 ↓
Runtime Validation
 ↓
Policy Verification
 ↓
Evidence Verification
 ↓
Decision Token
 ↓
Execution
```

Reasoning and authority **never merge**.

---

## Governance States

Richer than approved / not approved. Runtime behavior depends on state.

```
DRAFT → PROPOSED → UNDER_REVIEW → CPR (Conditional Pending Review)
  → BLOCKED | AUTHORIZED → EXECUTING → EXECUTED → VERIFIED → SEALED
                                              ↘ ROLLED_BACK
```

Typical happy path:

```
PROPOSED → UNDER_REVIEW → APPROVED → AUTHORIZED → EXECUTED → VERIFIED → SEALED
```

---

## Cryptographic Layer

Direction of recent iterations:

- Ed25519 signatures  
- Nonce protection / replay prevention  
- Append-only ledgers / hash chains  
- Immutable audit history  
- RFC 3161 timestamping (**planned**)  

Every major decision becomes independently verifiable.

---

## Evidence Model

Actions require evidence (examples: git commit, DB snapshot, test results, policy version, ADR, review package). Evidence is **hashed before approval**. Future changes invalidate prior approvals.

---

## Memory Architecture

Moved away from JSON memory toward **SQLite WAL** (concurrency / corruption). Direction:

- SQLite WAL  
- Append-only events  
- Semantic / observation hashes  
- State registry · outbox queue · recovery journal · checkpoints  

Longer-term goal: **deterministic recovery** after crashes.

---

## Trust Model (intentional order)

```
Human
 ↓
Governance
 ↓
Runtime
 ↓
Evidence
 ↓
Policies
 ↓
Agent
 ↓
LLM          ← near the bottom, intentionally
```

---

## Security Model (key controls)

- Per-operation JWTs (target)  
- Identity-bound execution  
- Nonce ledgers / replay protection  
- Immutable audit records  
- Least privilege / capability isolation  
- Fail-closed defaults  
- Service-role isolation  
- Execution authorization  

---

## Current Agent Roles

| Role | Function | Authority |
|------|----------|-----------|
| **BOB** | Operational executor — Telegram, tools, monitoring, execution, reporting | Executes only under runtime + tokens |
| **Robert** | Architect — planning, long reasoning, architecture, review, memory, orchestration | Reasons; does not self-authorize |
| **Council** | Independent models — disagreement, adversarial review, consensus, failure modes | Recommend only; **no execution authority** |

---

## Differentiation

| Feature | Conventional frameworks | TronixMesh |
|---------|-------------------------|------------|
| Runtime owns authority | No | **Yes** |
| Cryptographic approvals | Rare | **Yes** |
| Governance state machine | Minimal | **Extensive** |
| Human sovereignty | Often implicit | **Explicit** |
| Capability enforcement | Basic | **Central** |
| Independent reviewer doctrine | Rare | **Yes** |
| Decision tokens | No | **Yes** |
| Fail-closed architecture | Partial | **Core principle** |
| Immutable audit chain | Optional | **Required** |
| Policy before execution | Sometimes | **Always** |

---

## Long-Term Vision

A **governed AI operating system**, not an orchestration framework:

- Multiple specialized agents concurrently  
- Runtime enforces policy independently of any model  
- Cryptographically verifiable approvals and execution records  
- Human authority via explicit governance  
- Recovery, rollback, and auditability built in  
- Model-agnostic: Claude, GPT, Gemini, Grok, or successors replaceable without changing the governance layer  

**Central idea:** treat AI models as interchangeable reasoning engines; place identity, permissions, execution, evidence, and governance under a **deterministic runtime**.

---

## Phasing note

This doctrine is the north star. **Not every component ships in Phase B.** See [`PHASE-B-SLICE.md`](./PHASE-B-SLICE.md) for the reduction-to-practice slice currently Authorized for Build.

---

*End of TronixMesh Design Doctrine.*
