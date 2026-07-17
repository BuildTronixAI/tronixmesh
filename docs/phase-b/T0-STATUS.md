# Phase B — T0 Status

**T0 started:** 2026-07-17  
**Authorization:** Gate 0 signed — Christopher C. Leiser, Chairman  
**Plan status:** Approved for Build

## Delivered this increment

| Item | Location | Tests |
|------|----------|-------|
| Coordinate parsing (v1.1 8-segment) | `python/tronixmesh/coordinate.py` | pass |
| Proof-native envelope + ADR-0004 signature block | `python/tronixmesh/envelope.py` | pass |
| Ed25519 / HMAC signing helpers | `python/tronixmesh/signing.py` | pass |
| Provenance append-only hash chain (SQLite) | `python/tronixmesh/provenance.py` | pass |
| Coordinate registry | `python/tronixmesh/registry.py` | pass |
| Channel rules (default-deny) | `python/tronixmesh/channel.py` | pass |
| Minimal authority (bootstrap grants) | `python/tronixmesh/authority.py` | pass |
| Handoff primitive | `python/tronixmesh/handoff.py` | pass |
| Feature flags | `python/tronixmesh/flags.py` | — |

```bash
cd python && pip install -e ".[dev]" && pytest
# 12 passed
```

## Next (T0–T3 / T4–T8)

1. Accept ADR-0005 after Vultr inventory  
2. Postgres-backed provenance (beyond SQLite) when infra ready  
3. Routing layer + failure-injection harness  
4. Three agent runtimes (research / structure / review)  
5. Eval set v0 drafting  

## IP note

Runtime code lives under `python/` in this repository per current Authorized for Build path. Keep claim-sensitive expansion and internal fixtures out of public marketing surfaces; relocate to private eng repo if counsel requires.
