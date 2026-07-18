"""Operator CLI — resume / quarantine / replay / provenance / run-pilot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .agents.chain import CompetitiveIntelChain, MeshRuntime
from .taskstore import TaskStatus


def _runtime(db: Optional[str]) -> MeshRuntime:
    path = db or str(Path.home() / ".tronixmesh" / "pilot.db")
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    return MeshRuntime.create(db_path=path)


def cmd_run_pilot(args: argparse.Namespace) -> int:
    rt = _runtime(args.db)
    chain = CompetitiveIntelChain(rt)
    result = chain.start(args.query, task_id=args.task_id)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") == TaskStatus.COMPLETED.value else 1


def cmd_quarantine(args: argparse.Namespace) -> int:
    rt = _runtime(args.db)
    rec = rt.tasks.get(args.task_id)
    if rec is None:
        print(f"unknown task: {args.task_id}", file=sys.stderr)
        return 2
    updated = rt.tasks.quarantine(args.task_id, args.reason)
    rt.provenance.append(
        task_id=args.task_id,
        event_type="QUARANTINE",
        payload={"reason": args.reason, "operator": True},
    )
    print(json.dumps(updated.to_dict(), indent=2, sort_keys=True))
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    rt = _runtime(args.db)
    chain = CompetitiveIntelChain(rt)
    try:
        result = chain.resume(args.task_id)
    except KeyError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") == TaskStatus.COMPLETED.value else 1


def cmd_replay(args: argparse.Namespace) -> int:
    """Replay a committed step (F9) — shows idempotent no-op behavior."""
    rt = _runtime(args.db)
    rec = rt.tasks.get(args.task_id)
    if rec is None:
        print(f"unknown task: {args.task_id}", file=sys.stderr)
        return 2
    query = rec.payload.get("query") or ""
    # Re-invoke chain; runner returns replayed=True for committed handoffs
    chain = CompetitiveIntelChain(rt)
    result = chain.start(query, task_id=args.task_id)
    events = [
        e.to_dict()
        for e in rt.provenance.events_for_task(args.task_id)
        if e.event_type in {"STEP_REPLAY", "STEP_COMMITTED", "ROUTE_DECISION"}
    ]
    print(
        json.dumps(
            {"result": result, "replay_related_events": events[-10:]},
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def cmd_provenance(args: argparse.Namespace) -> int:
    rt = _runtime(args.db)
    events = [e.to_dict() for e in rt.provenance.events_for_task(args.task_id)]
    ok = rt.provenance.verify_chain()
    print(json.dumps({"chain_ok": ok, "events": events}, indent=2, sort_keys=True))
    return 0 if ok else 1


def cmd_list(args: argparse.Namespace) -> int:
    rt = _runtime(args.db)
    status = TaskStatus(args.status) if args.status else None
    rows = [t.to_dict() for t in rt.tasks.list(status=status)]
    print(json.dumps(rows, indent=2, sort_keys=True))
    return 0


def cmd_eval_campaign(args: argparse.Namespace) -> int:
    from evals.v1.campaign import report_json, run_campaign

    report = run_campaign(set_name=args.set)
    print(report_json(report))
    return 0 if report.meets_floor else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tronixmesh-ops",
        description="Tronix Mesh Phase B operator surface (CLI).",
    )
    p.add_argument(
        "--db",
        default=None,
        help="SQLite base path for task/memory/provenance (default: ~/.tronixmesh/pilot.db)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run-pilot", help="Run research→structure→review pilot")
    run.add_argument("query", help="Synthetic competitive-intel query")
    run.add_argument("--task-id", default=None)
    run.set_defaults(func=cmd_run_pilot)

    q = sub.add_parser("quarantine", help="Quarantine a task (fail-closed)")
    q.add_argument("task_id")
    q.add_argument("--reason", default="operator quarantine")
    q.set_defaults(func=cmd_quarantine)

    r = sub.add_parser("resume", help="Resume / re-run a task (idempotent handoffs)")
    r.add_argument("task_id")
    r.set_defaults(func=cmd_resume)

    rp = sub.add_parser("replay", help="Replay chain; show idempotent step events")
    rp.add_argument("task_id")
    rp.set_defaults(func=cmd_replay)

    pr = sub.add_parser("provenance", help="Dump provenance chain for a task")
    pr.add_argument("task_id")
    pr.set_defaults(func=cmd_provenance)

    ls = sub.add_parser("list", help="List tasks")
    ls.add_argument(
        "--status",
        choices=[s.value for s in TaskStatus],
        default=None,
    )
    ls.set_defaults(func=cmd_list)

    ev = sub.add_parser("eval-campaign", help="Run classifier eval campaign (v1)")
    ev.add_argument("--set", default="v1", choices=["v1"])
    ev.set_defaults(func=cmd_eval_campaign)

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
