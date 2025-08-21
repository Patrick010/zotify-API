from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from fastapi import HTTPException

from zotify_api.services.spoti_client import SpotiClient


@pytest.mark.asyncio
async def test_spoti_client_get_tracks_metadata_success():
    """
    Tests that the SpotiClient can successfully fetch track metadata.
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

        client = SpotiClient(access_token="fake_token")
        metadata = await client.get_tracks_metadata(["track1", "track2"])

        assert metadata == mock_json_response["tracks"]
        mock_request.assert_called_once()
        assert mock_request.call_args.kwargs['headers']['Authorization'] == "Bearer fake_token"
        await client.close()

@pytest.mark.asyncio
async def test_spoti_client_get_current_user_success():
    """
    Tests that the SpotiClient can successfully fetch the current user.
    """
    mock_json_response = {"id": "user1", "display_name": "Test User"}

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json_response
        mock_response.raise_for_status = MagicMock()
        mock_request.return_value = mock_response

        client = SpotiClient(access_token="fake_token")
        user = await client.get_current_user()

        assert user == mock_json_response
        mock_request.assert_called_once()
        await client.close()

@pytest.mark.asyncio
async def test_spoti_client_no_token():
    """
    Tests that the client raises a ValueError if it is initialized with no token.
    """
    with pytest.raises(ValueError, match="SpotiClient must be initialized with an access token."):
        SpotiClient(access_token=None)

@pytest.mark.asyncio
async def test_spoti_client_http_error():
    """
    Tests that the client propagates HTTP exceptions from the API.
    """
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        # The async request itself raises an exception
        mock_request.side_effect = httpx.HTTPStatusError(
            "Error", request=MagicMock(), response=MagicMock(status_code=404, text="Not Found")
        )

        client = SpotiClient(access_token="fake_token")
        with pytest.raises(HTTPException) as excinfo:
            await client.get_current_user()

        assert excinfo.value.status_code == 404
        assert excinfo.value.detail == "Not Found"
        await client.close()

@pytest.mark.asyncio
async def test_spoti_client_get_devices_success():
    """
    Tests that the SpotiClient can successfully fetch devices.
    """
    mock_json_response = {"devices": [{"id": "device1", "name": "Device 1"}]}

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_json_response
        mock_request.return_value = mock_response

        client = SpotiClient(access_token="fake_token")
        devices = await client.get_devices()

        assert devices == mock_json_response["devices"]
        mock_request.assert_called_once_with("GET", "/me/player/devices", headers={"Authorization": "Bearer fake_token"})
        await client.close()

@pytest.mark.asyncio
async def test_spoti_client_refresh_token_success():
    """
    Tests that the SpotiClient can successfully refresh an access token.
    """
    mock_json_response = {"access_token": "new_fake_token", "expires_in": 3600, "refresh_token": "new_refresh_token"}

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_json_response
        mock_post.return_value = mock_response

        result = await SpotiClient.refresh_access_token(refresh_token="old_refresh")
        assert result["access_token"] == "new_fake_token"

@pytest.mark.asyncio
async def test_spoti_client_search_success():
    """
    Tests that the SpotiClient can successfully perform a search.
    """
    mock_json_response = {"tracks": {"items": [{"id": "track1", "name": "Search Result"}]}}

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_json_response
        mock_request.return_value = mock_response

        client = SpotiClient(access_token="fake_token")
        results = await client.search(q="test", type="track", limit=1, offset=0)

        assert results == mock_json_response
        mock_request.assert_called_once()
        await client.close()

@pytest.mark.asyncio
async def test_spoti_client_get_playlists_success():
    mock_json_response = {"items": [{"id": "p1", "name": "Playlist 1"}]}
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_json_response
        mock_request.return_value = mock_response
        client = SpotiClient(access_token="fake_token")
        result = await client.get_current_user_playlists()
        assert result == mock_json_response
        mock_request.assert_called_once_with("GET", "/me/playlists", params={"limit": 20, "offset": 0}, headers={"Authorization": "Bearer fake_token"})
        await client.close()

@pytest.mark.asyncio
async def test_spoti_client_create_playlist_success():
    mock_json_response = {"id": "new_p1", "name": "New Playlist"}
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_json_response
        mock_request.return_value = mock_response
        client = SpotiClient(access_token="fake_token")
        result = await client.create_playlist("user1", "New Playlist", True, False, "Desc")
        assert result == mock_json_response
        await client.close()

@pytest.mark.asyncio
async def test_spoti_client_add_tracks_success():
    mock_json_response = {"snapshot_id": "snapshot1"}
    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_json_response
        mock_request.return_value = mock_response
        client = SpotiClient(access_token="fake_token")
        result = await client.add_tracks_to_playlist("p1", ["uri1", "uri2"])
        assert result == mock_json_response
        await client.close()

@pytest.mark.asyncio
async def test_spoti_client_get_all_playlists_pagination():
    """
    Tests that the client correctly handles pagination when fetching all playlists.
    """
    mock_page1 = {
        "items": [{"id": "p1"}],
        "next": "/me/playlists?offset=1&limit=1"
    }
    mock_page2 = {
        "items": [{"id": "p2"}],
        "next": None
    }

    with patch("httpx.AsyncClient.request", new_callable=AsyncMock) as mock_request:
        mock_response1 = MagicMock()
        mock_response1.json.return_value = mock_page1
        mock_response2 = MagicMock()
        mock_response2.json.return_value = mock_page2
        mock_request.side_effect = [mock_response1, mock_response2]

        client = SpotiClient(access_token="fake_token")
        results = await client.get_all_current_user_playlists()

        assert len(results) == 2
        assert results[0]["id"] == "p1"
        assert results[1]["id"] == "p2"
        assert mock_request.call_count == 2
        await client.close()

@pytest.mark.asyncio
async def test_spoti_client_exchange_code_for_token_success():
    """
    Tests that the client can successfully exchange an auth code for a token.
    """
    mock_json_response = {"access_token": "new_token", "refresh_token": "new_refresh"}
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_json_response
        mock_post.return_value = mock_response

        result = await SpotiClient.exchange_code_for_token("auth_code", "code_verifier")
        assert result == mock_json_response
