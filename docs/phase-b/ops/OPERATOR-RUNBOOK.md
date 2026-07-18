# Phase B Operator Runbook

**Audience:** Chris (primary on-call) · backup named at Gate 0  
**CLI:** `tronixmesh-ops` (from `python/` after `pip install -e .`)

## Pilot happy path

```bash
cd python && pip install -e ".[dev]"
tronixmesh-ops run-pilot "synthetic competitor query" --task-id demo-1
tronixmesh-ops provenance demo-1
tronixmesh-ops list --status completed
```

Default DB base path: `~/.tronixmesh/pilot.db` (+ `.prov` / `.mem` / `.tasks` sidecars).

## Quarantine / resume (fail closed)

```bash
tronixmesh-ops quarantine demo-1 --reason "operator hold"
tronixmesh-ops list --status quarantined
tronixmesh-ops resume demo-1
```

Resume re-invokes the LangGraph chain; Mesh idempotency keys prevent duplicate committed handoffs (F9).

## Replay / provenance integrity

```bash
tronixmesh-ops replay demo-1
tronixmesh-ops provenance demo-1   # includes chain_ok
```

If `chain_ok` is false → **F8**: stop, quarantine related tasks, do not execute further handoffs.

## Classifier eval campaign

```bash
tronixmesh-ops eval-campaign --set v1
```

Floor: accuracy ≥90%, FP≤2% (public), FN≤5% (boundary), 0 silent forced routes on ambiguous.

## Live workers (optional)

```bash
export TRONIX_WORKER_PROVIDER=anthropic   # or gemini | stub
export ANTHROPIC_API_KEY=...              # or GOOGLE_API_KEY for gemini
tronixmesh-ops run-pilot "query" --task-id live-1
```

Workers remain **recommendations only**. Missing keys fall back to stub. Never grant authority from model output (S3).

## Postgres cutover (when Vultr DSN exists)

```bash
export TRONIX_DATABASE_URL=postgresql://...
python -c "from tronixmesh.postgres import ping_postgres; print(ping_postgres())"
```

SQLite stand-ins remain default until ping is green and store adapters are switched (ADR-0003/0005).

## Failure quick map

| Code | Meaning | Operator action |
|------|---------|-----------------|
| F1 | Transient destination | Auto-retry; if exhausted → quarantine |
| F2 | Ambiguity | Escalate — do not force route |
| F3 | Unroutable | Quarantine; fix registry |
| F7 | Channel violation | Quarantine; review grants/rules |
| F8 | Hash mismatch | Halt; restore from backup when Postgres live |
| F9 | Replay | Expected no-op on committed step |
| F10 | Bad signature | Reject; rotate/check keys |

## Soft-launch

Still gated by staged rollout (plan §9). This runbook does **not** authorize production deploy.
