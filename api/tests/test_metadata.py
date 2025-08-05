import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def patch_metadata(monkeypatch):
    def fake_get_db_counts():
        from datetime import datetime
        return (10, 2, datetime(2025,8,1))
    monkeypatch.setattr("zotify_api.services.db.get_db_engine", lambda: True)
    monkeypatch.setattr("zotify_api.routes.metadata.get_db_counts", fake_get_db_counts)
    monkeypatch.setattr("zotify_api.routes.metadata.get_library_size_mb", lambda: 123.45)

def test_metadata_returns_schema():
    r = client.get("/api/metadata")
    assert r.status_code == 200
    b = r.json()
    assert b["total_tracks"] == 10
    assert isinstance(b["library_size_mb"], float)
