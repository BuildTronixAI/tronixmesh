# ADR-0001: Proof-native envelopes

- Status: Accepted
- Date: 2026-07-16
- Deciders: Chris (Gate 0)

## Decision

Context Envelope schema is **proof-native** from Phase B day one: signature blocks, hash-chain references, governance metadata slots, proof identifiers, and witness-coordinate fields are versioned in the schema even when verification behavior is incomplete.

Behavior (full ProofPackage verify, MeshResolver hot path, distributed enforcement) is **feature-flagged** and may be stubbed or off in Phase B.

## Alternatives considered

1. **Envelope-first, retrofit proof later** — smaller initial schema; forces migrations when proof fields land.  
2. **Full MeshResolver + ProofPackage on hot path in Phase B** — correct long-term substrate, exceeds pilot capacity and Doctrine-1B readiness.  
3. **Proof-native schema + flagged behavior (chosen)** — forward-compatible without dual implementation.

## Rationale

Dependency order is Proof model → Envelope schema → Storage → Interfaces → Behavior. Treating proof as an orthogonal add-on creates schema evolution risk. Patentable differentiation may depend on proof/governance capabilities; schema must not preclude them. Phase B still proves the handoff primitive under failure without shipping every verification path.

## Consequences

- Schema freeze at T3 includes proof fields (populated or explicitly null-versioned).  
- Storage and APIs must tolerate those fields.  
- Feature flags control enablement; turning verify on later must not require breaking migrations.  
- Marketing must not claim Doctrine-1B crypto certification until those flags and doctrine paths are actually on.
