import os
from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_track_metadata():
    response = client.get("/api/tracks/test-track-1/metadata")
    assert response.status_code == 200
    assert response.json()["id"] == "test-track-1"

def test_update_track_metadata():
    update_data = {"title": "New Title"}
    response = client.patch("/api/tracks/test-track-1/metadata", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_refresh_track_metadata():
    response = client.post("/api/tracks/test-track-1/metadata/refresh")
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

def test_upload_cover():
    # Create a dummy file for testing
    with open("cover.jpg", "w") as f:
        f.write("test")

    with open("cover.jpg", "rb") as f:
        response = client.post(
            "/api/tracks/test-track-1/cover",
            files={"cover_image": ("cover.jpg", f, "image/jpeg")}
        )

    # Clean up the dummy file
    os.remove("cover.jpg")

    assert response.status_code == 200
    assert "Embedded image: cover.jpg" in response.json()["cover"]
