from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_all_metadata():
    """ Test for GET /metadata """
    response = client.get("/api/metadata")
    assert response.status_code == 200
    response_json = response.json()
    assert "total_tracks" in response_json
    assert "total_playlists" in response_json
    assert "last_updated" in response_json
    assert "library_size_mb" in response_json

def test_get_metadata():
    response = client.get("/api/metadata/abc123")
    assert response.status_code == 200
    assert response.json()["mood"] == "Chill"

def test_patch_metadata():
    update_data = {"mood": "Energetic", "rating": 5}
    response = client.patch("/api/metadata/abc123", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "updated"
