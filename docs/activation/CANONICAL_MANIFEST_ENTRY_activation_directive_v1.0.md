# Canonical Manifest Entry — TronixMesh Activation Directive v1.0

**Entry type:** Authoritative artifact registry record (in-repo representation)
**Prepared:** 2026-08-16
**Prepared for:** Entry into the external BOB Canonical Manifest system (immediate-execution steps 1–3)

> This record fulfils immediate-execution steps 1–3 (compute canonical hash; document hash-domain
> specification; provide the hash + artifact for Canonical Manifest entry). The **authoritative** entry
> is made in the BOB Canonical Manifest system; the hash rendered in the human-readable directive copy is
> informational per RC-002. This file is the reproducible source of the canonical hash.

---

## 1. Artifact identity

| Field | Value |
|-------|-------|
| Artifact ID | `TRONIXMESH_ACTIVATION_DIRECTIVE_v1.0` |
| Artifact file | `docs/activation/TRONIXMESH_ACTIVATION_DIRECTIVE_v1.0.md` |
| Version | 1.0 (28 RC patches integrated) |
| Lock authority | Chris Leiser (Chairman) |
| Lock timestamp | 2026-08-16 01:49 UTC |
| Git commit of persisted artifact | recorded by the commit that adds this entry (see PR/branch) |
| Authority tier | *(assigned by Chairman at manifest entry)* |
| Effective epoch / time | *(recorded by Canonical Manifest at entry)* |
| Supersession | Supersedes the PENDING/NON-CANONICAL drafts of this directive on this branch; per-clause supersession of prior artifacts is enumerated in the directive change manifest (28 RC rows) |

---

## 2. Hash-domain specification (RC-002) — normative & reproducible

**Rule.** The canonical hash is `SHA-256` computed over the **UTF-8** bytes of
`TRONIXMESH_ACTIVATION_DIRECTIVE_v1.0.md` after **removing every line whose left-stripped text begins
with one of the two Document Hash field renderings**, then rejoining the remaining lines with the
newline character `\n` (LF). No other normalization is applied.

Excluded line prefixes (the `Document Hash` field; RC-002 excludes it from the hash domain):

- `**Document Hash:**`  (header field)
- `**Document Hash (RC-002):**`  (Signature & Hash section)

**Reference implementation (authoritative):**

```python
import hashlib, pathlib
text = pathlib.Path("docs/activation/TRONIXMESH_ACTIVATION_DIRECTIVE_v1.0.md").read_text("utf-8")
def excluded(line):
    s = line.lstrip()
    return s.startswith("**Document Hash:**") or s.startswith("**Document Hash (RC-002):**")
canonical = "\n".join(l for l in text.split("\n") if not excluded(l)).encode("utf-8")
print(hashlib.sha256(canonical).hexdigest())
```

- Lines excluded from the hash domain: **2** (exactly the two renderings above).
- Canonical byte length: **42867**.

BOB SHALL NOT improvise hashing semantics; any change to this rule is itself a change-controlled event.

---

## 3. Canonical hash

| Hash | Value |
|------|-------|
| **CANONICAL SHA-256 (RC-002 domain)** | `88897076733c6f4b00cb9dcb6ab741fea141092fdfa68d4582cb697d07d8c330` |
| Full-file SHA-256 (informational only; **not** the canonical hash) | `4e2d0c0bc4ae20fbec581bfc0464c81909fb35fcddecce2f82646ed518849025` |

The **canonical** value is the RC-002-domain hash. It is stable across edits to the excluded
`Document Hash` field lines. If any other byte of the artifact changes, this hash changes and the entry
must be recomputed.

---

## 4. Manifest entry procedure (external system)

Per directive §11.3 / immediate-execution steps 3–4 (performed by the Chairman / BOB Canonical Manifest
system — **not** performed here):

1. Record `TRONIXMESH_ACTIVATION_DIRECTIVE_v1.0` + canonical hash (§3) in the Canonical Manifest.
2. Assign authority tier.
3. Record effective epoch / time.
4. Mark superseded subordinate clauses per the directive change manifest.
5. Lock Runtime Specification **v1.1** requirements separately (RC-003) — v1.0 remains normative until
   v1.1 is separately approved, authenticated, hashed, and entered. **Not done here.**

Until the external entry completes, downstream production gates dependent on unresolved v1.1 semantics
remain uncrossable (RC-003).

---

*End of Canonical Manifest Entry record.*
