import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from unittest.mock import patch, AsyncMock
from zotify_api.main import app

@pytest.mark.asyncio
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_spotify_callback(mock_post):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value={
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600,
    })
    mock_post.return_value = mock_response

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/spotify/callback?code=test_code")

    assert response.status_code == 200
    assert response.json() == {"status": "Spotify tokens stored"}


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
@patch("zotify_api.routes.spotify.refresh_token_if_needed", new_callable=AsyncMock)
async def test_fetch_metadata(mock_refresh, mock_get):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = AsyncMock(return_value={"id": "test_track_id"})
    mock_get.return_value = mock_response

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/api/spotify/metadata/test-track-id")

    assert response.status_code == 200
    data = await response.json()
    assert data["id"] == "test_track_id"


@pytest.mark.asyncio
@patch("zotify_api.routes.spotify.refresh_token_if_needed", new_callable=AsyncMock)
async def test_sync_playlists(mock_refresh):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/api/spotify/playlist/sync")

    assert response.status_code == 200
