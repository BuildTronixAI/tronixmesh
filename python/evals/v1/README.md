# Eval set v1 — Classifier campaign (synthetic)

**Date:** 2026-07-18  
**Policy:** Synthetic fixtures only. Expands v0 with FP/FN campaign reporting (plan §4.1a).

## Targets

| Metric | Target |
|--------|--------|
| Accuracy | ≥90% |
| FP (over-route / wrong confidential) | ≤2% on public set |
| FN (missed boundary) | ≤5% on boundary set |
| Silent forced route on ambiguous | 0 |

## Run

```bash
cd python && pytest tests/test_eval_v1.py -q
tronixmesh-ops eval-campaign --set v1
```
