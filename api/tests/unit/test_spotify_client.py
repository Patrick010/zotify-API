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
