# Eval set v0 — Competitive intel pilot (synthetic)

**Date:** 2026-07-18  
**Policy:** Synthetic confidential fixtures only. No real internal data.

## Goals (plan §4.1 / §4.1a)

| Metric | Target |
|--------|--------|
| M1 accuracy | ≥90% on labeled set |
| FP (over-confidential / wrong function) | ≤2% on clean public set |
| FN (missed boundary / escalate) | ≤5% on boundary set |
| Ambiguity | 0 silent forced routes |

## Layout

- `cases.jsonl` — one labeled intent per line  
- Labels: `gold_action` ∈ `route|escalate`, `gold_function`, `sensitivity_class` ∈ `public|boundary|ambiguous`

## Run

```bash
cd python && pytest tests/test_eval_v0.py -q
```
