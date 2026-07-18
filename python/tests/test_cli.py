import json
from pathlib import Path

from tronixmesh.cli import main
from tronixmesh.taskstore import TaskStatus


def test_cli_run_pilot_and_provenance(tmp_path: Path):
    db = str(tmp_path / "pilot.db")
    rc = main(["--db", db, "run-pilot", "cli query", "--task-id", "cli-1"])
    assert rc == 0
    rc = main(["--db", db, "provenance", "cli-1"])
    assert rc == 0
    rc = main(["--db", db, "list", "--status", TaskStatus.COMPLETED.value])
    assert rc == 0


def test_cli_quarantine_and_resume(tmp_path: Path, capsys):
    db = str(tmp_path / "pilot.db")
    assert main(["--db", db, "run-pilot", "q", "--task-id", "cli-2"]) == 0
    assert main(["--db", db, "quarantine", "cli-2", "--reason", "ops hold"]) == 0
    out = capsys.readouterr().out
    # last command output is quarantine record — re-run quarantine capture cleanly
    assert main(["--db", db, "list", "--status", "quarantined"]) == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed[0]["task_id"] == "cli-2"
    # resume re-runs; completed again
    assert main(["--db", db, "resume", "cli-2"]) == 0
