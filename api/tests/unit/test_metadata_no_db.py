from fastapi.testclient import TestClient
from zotify_api.main import app
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def patch_db_none(monkeypatch):
    monkeypatch.setattr("zotify_api.routes.metadata.get_db_engine", lambda: None)

def test_metadata_fallback():
    r = client.get("/api/metadata")
    assert r.status_code == 200
    body = r.json()
    # Expect fallback values (define what fallback looks like)
    assert "total_tracks" in body
