# ADR-0004: Envelope signature architecture (schema freeze)

- Status: **Accepted**
- Date: 2026-07-17
- Deciders: Chris (via Phase B final production feedback — Cursor execution)
- Supersedes: Proposed “Ed25519 vs HMAC / verify later” draft (2026-07-16)

## Decision

**Option B — Signature-agnostic envelope (schema frozen; algorithm pluggable).**

The Context Envelope carries a fixed signature block layout. Future algorithms (including the intended first algorithm, Ed25519) populate an opaque signature blob without changing the envelope schema.

Verification behavior remains **feature-flagged**. Schema is not deferred.

### Frozen envelope signature fields

| Field | Type | Notes |
|-------|------|-------|
| `signature_version` | uint16 / string enum | Envelope signature block version; start at `1` |
| `algorithm_id` | string | e.g. `ed25519`, `hmac-sha256`; identifies how `signature` is interpreted |
| `key_id` | string | Stable key identifier (tenant-/mesh-scoped); not raw key material |
| `signed_at` | RFC3339 timestamp | When signature was produced |
| `content_hash` | string | Hash of canonical signed bytes (algorithm for hash named in `signature_version` policy; default SHA-256) |
| `signature` | opaque bytes (base64 in JSON) | Algorithm-specific blob; schema treats as opaque |
| `proof_extension` | object \| null | Optional proof/witness/gov metadata extension; forward-compatible |

### Canonicalization (frozen for v1)

1. Serialize envelope **payload + routing + authority + provenance refs** excluding the signature block itself.  
2. Produce `content_hash` over that canonical form.  
3. `signature` signs `content_hash` (or the canonical bytes — fixed in implementation note under `signature_version=1` as: sign the raw canonical bytes; store SHA-256 of those bytes in `content_hash` for audit).  
4. Changing canonicalization requires bumping `signature_version`.

### Intended first algorithm

- **`algorithm_id = ed25519`** for Phase B production path when keys exist.  
- `hmac-sha256` may be used only if listed in [`registry/TECHNOLOGY.md`](../registry/TECHNOLOGY.md) as Experimental and still fits this **same** field layout (no schema change).  
- Unsigned envelopes are **rejected** (fail-closed / F10).

## Alternatives considered

1. **Option A — Freeze Ed25519-only schema** — strongest long-term alignment with Doctrine-1B; rejects HMAC without schema escape. Rejected for Phase B freeze because Day-1 key ops may need HMAC on a single node without claiming a different envelope shape.  
2. **Option B — Signature-agnostic envelope (chosen)** — freezes layout/identifiers/opaque blob; algorithm choice does not reopen schema.  
3. **Defer ADR / “verify later”** — **rejected**. Signature architecture shapes the envelope; deferral reintroduces schema uncertainty (layout, algorithm ids, key ids, hashing inputs, serialization boundaries, proof compatibility).

## Rationale

Earlier iterations established: **proof shapes schema**. The same logic applies: **signature architecture shapes the envelope**. “Verify later” is not an acceptable schema state. Option B is a legitimate architectural deferral of *algorithm operations*, not of *schema*.

## Consequences

- Schema freeze (T3 / Gate architecture) **includes** the fields above — Covered in doctrine-to-gate matrix.  
- Storage, APIs, and fixtures must tolerate `algorithm_id` + opaque `signature`.  
- ProofPackage / MeshResolver attach later without envelope migration **if** they consume these fields.  
- ADR status lives **only** in this file — no separate Decision Log.  
- Technology registry may mark HMAC experimental; it must not invent parallel signature fields.
