from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_playlist_sync():
    response = client.post("/api/sync/playlist", json={"playlist_id": "abc123"})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "synced_tracks" in response.json()
    assert "conflicts" in response.json()
