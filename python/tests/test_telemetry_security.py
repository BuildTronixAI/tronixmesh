from tronixmesh.agents.chain import CompetitiveIntelChain, MeshRuntime
from tronixmesh.coordinate import MeshCoordinate
from tronixmesh.security import check_no_model_authority, security_floor_report
from tronixmesh.telemetry import get_correlation_id, new_correlation_id, reset_correlation_id, set_correlation_id


def test_correlation_id_on_provenance():
    chain = CompetitiveIntelChain(MeshRuntime.create())
    result = chain.start("telemetry query", task_id="tel-1")
    assert result["status"] == "completed"
    events = chain.runtime.provenance.events_for_task("tel-1")
    start = next(e for e in events if e.event_type == "TASK_START")
    assert "correlation_id" in start.payload
    # context cleared after start
    assert get_correlation_id() is None


def test_security_floor_cross_cell_and_model_authority():
    src = MeshCoordinate.parse(
        "L2R.Buildtronix.Engineering.research.public.balanced.text.long"
    )
    bad = MeshCoordinate.parse(
        "L2R.Buildtronix.Sales.structure.confidential.frontier.text.medium"
    )
    findings = security_floor_report(source=src, destination=bad)
    assert any(not f.ok and f.code == "S1_CROSS_CELL" for f in findings)
    assert check_no_model_authority({"role": "research"}).ok
    assert not check_no_model_authority({"grant_id": "x"}).ok


def test_correlation_contextvar_roundtrip():
    cid = new_correlation_id()
    tok = set_correlation_id(cid)
    assert get_correlation_id() == cid
    reset_correlation_id(tok)
    assert get_correlation_id() is None
