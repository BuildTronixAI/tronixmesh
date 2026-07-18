import pytest

from tronixmesh.memory import CellMemoryStore, ScopeViolation


def test_put_get_with_scopes():
    mem = CellMemoryStore(":memory:")
    mem.put(
        "task:1",
        {"n": 1},
        scope_tags=("task", "engineering"),
        ttl_seconds=60,
        writer_scopes=("task", "engineering", "ops"),
    )
    entry = mem.get("task:1", reader_scopes=("task", "engineering"))
    assert entry is not None
    assert entry.value["n"] == 1


def test_scope_violation_on_read():
    mem = CellMemoryStore(":memory:")
    mem.put(
        "secret",
        {"x": 1},
        scope_tags=("confidential",),
        ttl_seconds=60,
        writer_scopes=("confidential",),
    )
    with pytest.raises(ScopeViolation):
        mem.get("secret", reader_scopes=("public",))


def test_ttl_sweep():
    mem = CellMemoryStore(":memory:")
    mem.put(
        "ephemeral",
        {"x": 1},
        scope_tags=("task",),
        ttl_seconds=3600,
        writer_scopes=("task",),
    )
    mem._conn.execute(
        "UPDATE cell_memory SET expires_at = '2000-01-01T00:00:00Z' WHERE key = ?",
        ("ephemeral",),
    )
    mem._conn.commit()
    assert mem.get("ephemeral", reader_scopes=("task",)) is None
