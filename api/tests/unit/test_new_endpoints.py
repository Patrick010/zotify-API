import pytest
import respx
from zotify_api.auth_state import spotify_tokens

@pytest.fixture(autouse=True)
def clear_tokens():
    """Clear spotify tokens before each test."""
    spotify_tokens.update({
        "access_token": None,
        "refresh_token": None,
        "expires_at": 0,
    })

@pytest.fixture
def mock_spotify_api():
    """Mock the Spotify API."""
    with respx.mock(base_url="https://api.spotify.com/v1") as mock:
        yield mock

@pytest.fixture
def mock_spotify_token_api():
    """Mock the Spotify Token API."""
    with respx.mock(base_url="https://accounts.spotify.com/api/token") as mock:
        yield mock

def test_get_auth_status_no_api_key(client):
    response = client.get("/api/auth/status")
    assert response.status_code == 401

def test_get_auth_status_unauthenticated(client):
    response = client.get("/api/auth/status", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is False
    assert data["token_valid"] is False

def test_get_auth_status_authenticated(client, mock_spotify_api):
    spotify_tokens["access_token"] = "valid_token"
    mock_spotify_api.get("/me").respond(200, json={"id": "testuser"})
    response = client.get("/api/auth/status", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is True
    assert data["token_valid"] is True
    assert data["user_id"] == "testuser"

def test_logout(client):
    spotify_tokens["access_token"] = "valid_token"
    response = client.post("/api/auth/logout", headers={"X-API-Key": "test_key"})
    assert response.status_code == 204
    assert spotify_tokens["access_token"] is None

def test_refresh_no_token(client):
    response = client.get("/api/auth/refresh", headers={"X-API-Key": "test_key"})
    assert response.status_code == 400

def test_refresh_success(client, mock_spotify_token_api):
    spotify_tokens["refresh_token"] = "my_refresh_token"
    mock_spotify_token_api.post("").respond(200, json={"access_token": "new_access_token", "expires_in": 3600})
    response = client.get("/api/auth/refresh", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert spotify_tokens["access_token"] == "new_access_token"

def test_get_spotify_me(client, mock_spotify_api):
    spotify_tokens["access_token"] = "valid_token"
    mock_spotify_api.get("/me").respond(200, json={"id": "testuser", "display_name": "Test User"})
    response = client.get("/api/spotify/me", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json()["id"] == "testuser"

def test_get_spotify_devices(client, mock_spotify_api):
    spotify_tokens["access_token"] = "valid_token"
    mock_spotify_api.get("/me/player/devices").respond(200, json={"devices": [{"id": "123", "name": "Test Device"}]})
    response = client.get("/api/spotify/devices", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert len(response.json()["devices"]) == 1

def test_get_tracks_metadata(client, mock_spotify_api):
    spotify_tokens["access_token"] = "valid_token"
    mock_spotify_api.get("/tracks").respond(200, json={"tracks": [{"id": "1", "name": "Track 1"}, {"id": "2", "name": "Track 2"}]})
    response = client.post("/api/tracks/metadata", headers={"X-API-Key": "test_key"}, json={"track_ids": ["1", "2"]})
    assert response.status_code == 200
    assert len(response.json()["metadata"]) == 2

def test_get_system_uptime(client):
    response = client.get("/api/system/uptime", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert "uptime_seconds" in data
    assert "uptime_human" in data

def test_get_system_env(client):
    response = client.get("/api/system/env", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "python_version" in data
    assert "platform" in data

def test_get_schema(client):
    response = client.get("/api/schema", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert "openapi" in response.json()

def test_get_schema_q(client):
    response = client.get("/api/schema?q=SystemEnv", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert "title" in response.json() and response.json()["title"] == "SystemEnv"
