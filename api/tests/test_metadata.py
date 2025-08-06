from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_metadata():
    response = client.get("/api/metadata/abc123")
    assert response.status_code == 200
    assert response.json()["mood"] == "Chill"

def test_patch_metadata():
    update_data = {"mood": "Energetic", "rating": 5}
    response = client.patch("/api/metadata/abc123", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "updated"

    # Verify that the metadata was updated
    final_metadata = client.get("/api/metadata/abc123").json()
    assert final_metadata["mood"] == "Energetic"
    assert final_metadata["rating"] == 5
