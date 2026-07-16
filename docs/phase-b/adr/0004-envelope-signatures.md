# ADR-0004: Envelope signatures (Ed25519 vs HMAC)

- Status: Proposed
- Date: 2026-07-16
- Deciders: Chris (finalize by T3)

## Decision

**Pending.** Preference: **Ed25519** for envelope signature blocks. HMAC-SHA256 allowed only as an explicit, time-boxed pilot downgrade with an ADR update and Phase C upgrade commitment.

## Alternatives considered

1. **Ed25519** — aligns with doctrine/crypto direction; asymmetric verify; better long-term story.  
2. **HMAC-SHA256** — simpler key distribution on a single node; weaker alignment with Doctrine-1B.  
3. **Unsigned envelopes in Phase B** — rejected; breaks fail-closed and F10.

## Rationale

Signature **structure** is required in the proof-native schema regardless. Algorithm choice should not block schema freeze, but must be recorded before soft launch so keys and verify hooks are consistent.

## Consequences

- Schema includes algorithm identifier + key id fields.  
- If HMAC is chosen temporarily, document rotation to Ed25519 before Phase C.  
- Accept this ADR (or HMAC variant) by T3.
