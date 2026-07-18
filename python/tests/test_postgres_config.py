from tronixmesh.postgres import load_database_config, ping_postgres


def test_default_sqlite(monkeypatch):
    monkeypatch.delenv("TRONIX_DATABASE_URL", raising=False)
    cfg = load_database_config()
    assert cfg.backend == "sqlite"
    assert ping_postgres()["ok"] is True


def test_postgres_url_without_psycopg(monkeypatch):
    monkeypatch.setenv("TRONIX_DATABASE_URL", "postgresql://user:pass@localhost:5432/tronix")
    cfg = load_database_config()
    assert cfg.is_postgres
    # May fail connectivity or missing driver — must not raise
    status = ping_postgres()
    assert status["backend"] == "postgres"
    assert "ok" in status
