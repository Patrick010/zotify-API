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


def test_get_auth_status_no_api_key(client):
    response = client.get("/api/auth/status")
    assert response.status_code == 401

def test_get_auth_status_unauthenticated(client):
    response = client.get("/api/auth/status", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is False
    assert data["token_valid"] is False

from unittest.mock import patch, AsyncMock
from zotify_api.schemas.auth import AuthStatus

@patch("zotify_api.routes.auth.get_auth_status", new_callable=AsyncMock)
def test_get_auth_status_authenticated(mock_get_status, client):
    mock_get_status.return_value = AuthStatus(
        authenticated=True,
        user_id="testuser",
        token_valid=True,
        expires_in=3600
    )
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

@patch("zotify_api.routes.auth.refresh_spotify_token", new_callable=AsyncMock)
def test_refresh_success(mock_refresh, client):
    mock_refresh.return_value = 1234567890
    response = client.get("/api/auth/refresh", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json()["expires_at"] == 1234567890

@patch("zotify_api.routes.spotify.spotify_service.get_me", new_callable=AsyncMock)
def test_get_spotify_me(mock_get_me, client):
    mock_get_me.return_value = {"id": "testuser", "display_name": "Test User"}
    response = client.get("/api/spotify/me", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json()["id"] == "testuser"

@patch("zotify_api.routes.spotify.spotify_service.get_spotify_devices", new_callable=AsyncMock)
def test_get_spotify_devices(mock_get_devices, client):
    mock_get_devices.return_value = [{"id": "123", "name": "Test Device"}]
    response = client.get("/api/spotify/devices", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert len(response.json()["devices"]) == 1
    assert response.json()["devices"][0]["name"] == "Test Device"

@patch("zotify_api.routes.tracks.tracks_service.get_tracks_metadata_from_spotify", new_callable=AsyncMock)
def test_get_tracks_metadata(mock_get_metadata, client):
    mock_get_metadata.return_value = [{"id": "1", "name": "Track 1"}, {"id": "2", "name": "Track 2"}]
    response = client.post("/api/tracks/metadata", headers={"X-API-Key": "test_key"}, json={"track_ids": ["1", "2"]})
    assert response.status_code == 200
    assert len(response.json()["metadata"]) == 2
    assert response.json()["metadata"][0]["name"] == "Track 1"

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
