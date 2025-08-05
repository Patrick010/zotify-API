import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
import zotify_api.services.metadata as metadata_service
from sqlalchemy.exc import OperationalError

client = TestClient(app)

def test_metadata_fallback_on_operational_error(monkeypatch):
    # Make get_db_engine() return an engine-like object whose connect() raises OperationalError
    class FakeConn:
        def __enter__(self):
            raise OperationalError("no such table", None, None)
        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeEngine:
        def connect(self):
            return FakeConn()

    monkeypatch.setattr("zotify_api.services.db.get_db_engine", lambda: FakeEngine())
    # Call the endpoint
    r = client.get("/api/metadata")
    assert r.status_code == 200
    body = r.json()
    # Validate fallback structure
    assert body.get("total_tracks") == 0
    assert body.get("total_playlists") == 0
    # last_updated can be None or missing depending on model — check tolerant
    assert "library_size_mb" in body

def test_metadata_fallback_no_engine(monkeypatch):
    monkeypatch.setattr("zotify_api.services.db.get_db_engine", lambda: None)
    r = client.get("/api/metadata")
    assert r.status_code == 200
    body = r.json()
    assert body["total_tracks"] == 0
