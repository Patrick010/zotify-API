import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from fastapi import HTTPException
from zotify_api.services.spotify_client import SpotifyClient

@pytest.mark.asyncio
async def test_spotify_client_get_tracks_metadata_success():
    """
    Tests that the Spotify client can successfully fetch track metadata.
    """
    mock_json_response = {
        "tracks": [
            {"id": "track1", "name": "Track 1"},
            {"id": "track2", "name": "Track 2"},
        ]
    }

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        # The return value of the async request is a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json_response
        mock_response.raise_for_status = MagicMock()
        mock_request.return_value = mock_response

        client = SpotifyClient(access_token="fake_token")
        metadata = await client.get_tracks_metadata(["track1", "track2"])

        assert metadata == mock_json_response["tracks"]
        mock_request.assert_called_once()
        assert mock_request.call_args.kwargs['headers']['Authorization'] == "Bearer fake_token"
        await client.close()

@pytest.mark.asyncio
async def test_spotify_client_get_current_user_success():
    """
    Tests that the Spotify client can successfully fetch the current user.
    """
    mock_json_response = {"id": "user1", "display_name": "Test User"}

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json_response
        mock_response.raise_for_status = MagicMock()
        mock_request.return_value = mock_response

        client = SpotifyClient(access_token="fake_token")
        user = await client.get_current_user()

        assert user == mock_json_response
        mock_request.assert_called_once()
        await client.close()

@pytest.mark.asyncio
async def test_spotify_client_no_token():
    """
    Tests that the client raises an HTTPException if no access token is provided.
    """
    client = SpotifyClient(access_token=None)
    with pytest.raises(HTTPException) as excinfo:
        await client.get_current_user()

    assert excinfo.value.status_code == 401
    assert "Not authenticated" in excinfo.value.detail
    await client.close()

@pytest.mark.asyncio
async def test_spotify_client_http_error():
    """
    Tests that the client propagates HTTP exceptions from the API.
    """
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        # The async request itself raises an exception
        mock_request.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock(status_code=404, text="Not Found")
        )

        client = SpotifyClient(access_token="fake_token")
        with pytest.raises(HTTPException) as excinfo:
            await client.get_current_user()

        assert excinfo.value.status_code == 404
        assert excinfo.value.detail == "Not Found"
        await client.close()

@pytest.mark.asyncio
async def test_spotify_client_get_devices_success():
    """
    Tests that the Spotify client can successfully fetch devices.
    """
    mock_json_response = {"devices": [{"id": "device1", "name": "Device 1"}]}

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_json_response
        mock_request.return_value = mock_response

        client = SpotifyClient(access_token="fake_token")
        devices = await client.get_devices()

        assert devices == mock_json_response["devices"]
        mock_request.assert_called_once_with("GET", "/me/player/devices", headers={"Authorization": "Bearer fake_token"})
        await client.close()

@pytest.mark.asyncio
async def test_spotify_client_refresh_token_success():
    """
    Tests that the Spotify client can successfully refresh an access token.
    """
    mock_json_response = {"access_token": "new_fake_token", "expires_in": 3600, "refresh_token": "new_refresh_token"}

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_json_response
        mock_post.return_value = mock_response

        client = SpotifyClient(access_token="old_token", refresh_token="old_refresh")
        await client.refresh_access_token()

        # This is a bit of a tricky test as it modifies the global state
        # We can assert the internal state of the client for now
        assert client._access_token == "new_fake_token"
        assert client._refresh_token == "new_refresh_token"
        mock_post.assert_called_once()
        await client.close()

@pytest.mark.asyncio
async def test_spotify_client_search_success():
    """
    Tests that the Spotify client can successfully perform a search.
    """
    mock_json_response = {"tracks": {"items": [{"id": "track1", "name": "Search Result"}]}}

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_json_response
        mock_request.return_value = mock_response

        client = SpotifyClient(access_token="fake_token")
        results = await client.search(q="test", type="track", limit=1, offset=0)

        assert results == mock_json_response
        mock_request.assert_called_once()
        await client.close()
