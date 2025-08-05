from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_metadata():
    resp = client.get("/api/metadata")
    assert resp.status_code == 200
    b = resp.json()
    assert isinstance(b["total_tracks"], int)
    assert isinstance(b["total_playlists"], int)
    assert "last_updated" in b
    assert isinstance(b["library_size_mb"], float)
