import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient
from fastapi.testclient import TestClient
from zotify_api.main import app

# Use TestClient only for sync endpoints
sync_client = TestClient(app)


def test_spotify_login():
    response = sync_client.get("/api/spotify/login")
    assert response.status_code == 200
    data = response.json()
    assert "auth_url" in data
    assert "https://accounts.spotify.com/authorize" in data["auth_url"]


def test_token_status():
    response = sync_client.get("/api/spotify/token_status")
    assert response.status_code == 200
    data = response.json()
    assert "access_token_valid" in data
    assert "expires_in_seconds" in data


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_spotify_callback(mock_post):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600,
    }
    mock_post.return_value = mock_response

    client = AsyncClient(app=app, base_url="http://testserver")
    response = await client.get("/api/spotify/callback?code=test_code")
    assert response.status_code == 200
    assert response.json() == {"status": "Spotify tokens stored"}


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
@patch("zotify_api.routes.spotify.refresh_token_if_needed", new_callable=AsyncMock)
async def test_fetch_metadata(mock_refresh, mock_get):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "test_track_id"}
    mock_get.return_value = mock_response

    client = AsyncClient(app=app, base_url="http://testserver")
    response = await client.get("/api/spotify/metadata/test_track_id")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test_track_id"
    mock_refresh.assert_called_once()


@pytest.mark.asyncio
@patch("zotify_api.routes.spotify.refresh_token_if_needed", new_callable=AsyncMock)
async def test_sync_playlists(mock_refresh):
    client = AsyncClient(app=app, base_url="http://testserver")
    response = await client.post("/api/spotify/sync_playlists")
    assert response.status_code == 200
    assert response.json() == {"status": "Playlists synced (stub)"}
    mock_refresh.assert_called_once()
