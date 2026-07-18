from tronixmesh.taskstore import TaskStatus, TaskStore


def test_task_lifecycle():
    store = TaskStore(":memory:")
    store.create("t1", payload={"query": "x"})
    store.update("t1", status=TaskStatus.RUNNING, step="research")
    store.quarantine("t1", "hold")
    rec = store.get("t1")
    assert rec is not None
    assert rec.status == TaskStatus.QUARANTINED
    assert rec.error == "hold"
    assert store.list(status=TaskStatus.QUARANTINED)[0].task_id == "t1"
