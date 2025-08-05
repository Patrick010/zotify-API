import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.database import get_db, save_db
from zotify_api.models.playlist import Playlist

# In-memory "database" for testing
fake_db = {
    "playlists": [
        Playlist(id="1", name="My Favorite Songs", tracks=["track1", "track2"]),
        Playlist(id="2", name="Workout Mix", tracks=[])
    ]
}

# A dependency override to use a stateful mock database
def override_get_db():
    return fake_db["playlists"]

def override_save_db(db_instance):
    # In a real scenario, this would save to the fake_db, but for now, we'll just pass
    # This highlights the need for a more robust mocking strategy if we need to test state changes.
    pass

# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[save_db] = override_save_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Reset the fake_db before each test
    global fake_db
    fake_db = {
        "playlists": [
            {"id": "1", "name": "My Favorite Songs", "tracks": ["track1", "track2"]},
            {"id": "2", "name": "Workout Mix", "tracks": []}
        ]
    }
    yield
    # Teardown can happen here if needed

def test_get_playlists():
    """ Test for GET /playlists """
    response = client.get("/api/playlists")
    assert response.status_code == 200
    response_json = response.json()
    assert "data" in response_json
    assert "meta" in response_json
    assert isinstance(response_json["data"], list)
    assert len(response_json["data"]) == 2

def test_get_playlists_with_limit():
    """ Test for GET /playlists with limit """
    response = client.get("/api/playlists?limit=1")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) == 1

def test_get_playlists_with_offset():
    """ Test for GET /playlists with offset """
    response = client.get("/api/playlists?offset=1")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) == 1
    assert response_json["data"][0]["name"] == "Workout Mix"

def test_get_playlists_with_search():
    """ Test for GET /playlists with search """
    response = client.get("/api/playlists?search=Favorite")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) == 1
    assert response_json["data"][0]["name"] == "My Favorite Songs"

def test_create_playlist():
    """ Test for POST /playlists """
    new_playlist_data = {"name": "Chill Vibes"}

    response = client.post("/api/playlists", json=new_playlist_data)

    # The status code for resource creation should be 201
    assert response.status_code == 201, response.text

    response_data = response.json()
    assert response_data["name"] == new_playlist_data["name"]
    assert "id" in response_data
    assert "tracks" in response_data
    assert response_data["tracks"] == [] # New playlists should have no tracks
