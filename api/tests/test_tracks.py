import os
from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_tracks():
    """ Test for GET /tracks """
    response = client.get("/api/tracks")
    assert response.status_code == 200
    response_json = response.json()
    assert "data" in response_json
    assert "meta" in response_json
    assert isinstance(response_json["data"], list)
    assert len(response_json["data"]) == 2

def test_get_tracks_with_limit():
    """ Test for GET /tracks with limit """
    response = client.get("/api/tracks?limit=1")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) == 1

def test_get_tracks_with_offset():
    """ Test for GET /tracks with offset """
    response = client.get("/api/tracks?offset=1")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) == 1
    assert response_json["data"][0]["title"] == "Demo Track 2"

def test_get_tracks_with_search():
    """ Test for GET /tracks with search """
    response = client.get("/api/tracks?search=Artist 1")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) == 1
    assert response_json["data"][0]["title"] == "Demo Track 1"

def test_get_track_metadata():
    response = client.get("/api/tracks/1/metadata")
    assert response.status_code == 200
    assert response.json()["title"] == "Demo Track 1"

def test_update_track_metadata():
    update_data = {"title": "New Title"}
    response = client.patch("/api/tracks/1/metadata", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_refresh_track_metadata():
    response = client.post("/api/tracks/1/metadata/refresh")
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

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
