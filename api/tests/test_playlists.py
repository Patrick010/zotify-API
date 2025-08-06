import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.database import get_db, save_db
from zotify_api.models.playlist import Playlist

client = TestClient(app)

@pytest.fixture
def temp_db():
    db = {
        "playlists": [
            {"id": "1", "name": "My Favorite Songs", "tracks": ["track1", "track2"]},
            {"id": "2", "name": "Workout Mix", "tracks": []}
        ]
    }
    return db

@pytest.fixture(autouse=True)
def run_around_tests(temp_db):
    def override_get_db():
        return temp_db['playlists']

    def override_save_db(db_instance):
        temp_db['playlists'] = db_instance

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[save_db] = override_save_db
    yield
    app.dependency_overrides = {}

def test_get_playlists(temp_db):
    """ Test for GET /playlists """
    response = client.get("/api/playlists")
    assert response.status_code == 200

    # The response should be a list of Playlist objects
    response_json = response.json()
    assert isinstance(response_json, list)

    # Check if the structure matches the Playlist model
    for item in response_json:
        assert "id" in item
        assert "name" in item
        assert "tracks" in item

    # Check if the data matches our mock db
    assert len(response_json) == len(temp_db["playlists"])
    # A more specific check on content
    assert response_json[0]["name"] == temp_db["playlists"][0]["name"]


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
