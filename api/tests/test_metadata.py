from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_metadata():
    response = client.get("/api/metadata/abc123")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Track Title"
    assert data["mood"] == "Chill"

def test_patch_metadata():
    # Reset state before this test to ensure idempotency
    original_metadata = {"mood": "Chill", "rating": 4}
    client.patch("/api/metadata/abc123", json=original_metadata)

    update_data = {"mood": "Energetic", "rating": 5}
    response = client.patch("/api/metadata/abc123", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "updated"
    assert data["track_id"] == "abc123"

    # Verify that the metadata was updated
    final_response = client.get("/api/metadata/abc123")
    assert final_response.status_code == 200
    final_metadata = final_response.json()
    assert final_metadata["mood"] == "Energetic"
    assert final_metadata["rating"] == 5
