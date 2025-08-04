import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.database import get_db, save_db
from zotify_api.models.playlist import Playlist

# In-memory "database" for testing
fake_db = {
    "playlists": [
        {"id": "1", "name": "My Favorite Songs", "tracks": ["track1", "track2"]},
        {"id": "2", "name": "Workout Mix", "tracks": []}
    ]
}

# A dependency override to use a stateful mock database
def override_get_db():
    return fake_db['playlists']

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
    response = client.get("/playlists")
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
    assert len(response_json) == len(fake_db["playlists"])
    # A more specific check on content
    assert response_json[0]["name"] == fake_db["playlists"][0]["name"]


def test_create_playlist():
    """ Test for POST /playlists """
    new_playlist_data = {"name": "Chill Vibes"}

    response = client.post("/playlists", json=new_playlist_data)

    # The status code for resource creation should be 201
    assert response.status_code == 201, response.text

    response_data = response.json()
    assert response_data["name"] == new_playlist_data["name"]
    assert "id" in response_data
    assert "tracks" in response_data
    assert response_data["tracks"] == [] # New playlists should have no tracks
