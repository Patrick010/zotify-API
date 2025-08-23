from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest import MonkeyPatch
from sqlalchemy.orm import Session

from zotify_api.providers.spotify_connector import SpotifyConnector


@pytest.mark.asyncio
@patch("zotify_api.providers.spotify_connector.crud.create_or_update_spotify_token")
@patch("httpx.AsyncClient")
async def test_handle_oauth_callback_success(
    mock_AsyncClient: AsyncMock, mock_crud_call: AsyncMock, monkeypatch: MonkeyPatch
) -> None:
    """Tests the happy path for the OAuth callback handler"""
    mock_db = Session()
    connector = SpotifyConnector(db=mock_db)

    # Configure the mock for the async context manager
    mock_client_instance = AsyncMock()

    # Configure the response from the 'post' call
    mock_post_response = AsyncMock()
    mock_post_response.json.return_value = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600,
    }
    mock_post_response.raise_for_status = MagicMock(return_value=None)
    mock_client_instance.post.return_value = mock_post_response

    # Make the AsyncClient return our configured instance when used as a context manager
    mock_AsyncClient.return_value.__aenter__.return_value = mock_client_instance

    monkeypatch.setitem(
        __import__("zotify_api.auth_state").auth_state.pending_states,
        "test_state",
        "test_code_verifier",
    )

    html_response = await connector.handle_oauth_callback(
        code="test_code", error=None, state="test_state"
    )

    mock_crud_call.assert_called_once()
    assert "Successfully authenticated" in html_response


@pytest.mark.asyncio
async def test_handle_oauth_callback_error() -> None:
    """Tests the failure path for the OAuth callback handler"""
    mock_db = Session()
    connector = SpotifyConnector(db=mock_db)

    html_response = await connector.handle_oauth_callback(
        code=None, error="access_denied", state="test_state"
    )

    assert "Authentication Failed" in html_response
    assert "access_denied" in html_response


@pytest.mark.asyncio
async def test_get_oauth_login_url(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        "zotify_api.providers.spotify_connector.CLIENT_ID", "test_client_id"
    )
    connector = SpotifyConnector(db=Session())
    url = await connector.get_oauth_login_url("test_state")
    assert "test_client_id" in url
    assert "test_state" in url
    assert "code_challenge" in url


@pytest.mark.asyncio
async def test_search_success() -> None:
    mock_client = AsyncMock()
    mock_client.search.return_value = {"tracks": {"items": ["track1"], "total": 1}}
    connector = SpotifyConnector(db=Session(), client=mock_client)
    items, total = await connector.search("test", "track", 1, 0)
    assert items == ["track1"]
    assert total == 1


@pytest.mark.asyncio
async def test_search_no_client() -> None:
    connector = SpotifyConnector(db=Session())
    with pytest.raises(Exception, match="SpotiClient not initialized."):
        await connector.search("test", "track", 1, 0)


@pytest.mark.asyncio
async def test_get_playlist_success() -> None:
    mock_client = AsyncMock()
    mock_client.get_playlist.return_value = {"name": "Test Playlist"}
    connector = SpotifyConnector(db=Session(), client=mock_client)
    playlist = await connector.get_playlist("playlist_id")
    assert playlist["name"] == "Test Playlist"


@pytest.mark.asyncio
async def test_get_playlist_no_client() -> None:
    connector = SpotifyConnector(db=Session())
    with pytest.raises(Exception, match="SpotiClient not initialized."):
        await connector.get_playlist("playlist_id")


@pytest.mark.asyncio
async def test_get_playlist_tracks_success() -> None:
    mock_client = AsyncMock()
    mock_client.get_playlist_tracks.return_value = {"items": ["track1"]}
    connector = SpotifyConnector(db=Session(), client=mock_client)
    tracks = await connector.get_playlist_tracks("playlist_id", 1, 0)
    assert tracks["items"] == ["track1"]


@pytest.mark.asyncio
async def test_get_playlist_tracks_no_client() -> None:
    connector = SpotifyConnector(db=Session())
    with pytest.raises(Exception, match="SpotiClient not initialized."):
        await connector.get_playlist_tracks("playlist_id", 1, 0)


@pytest.mark.asyncio
@patch("zotify_api.providers.spotify_connector.crud")
async def test_sync_playlists_success(mock_crud: AsyncMock) -> None:
    mock_client = AsyncMock()
    mock_client.get_all_current_user_playlists.return_value = [
        {
            "id": "p1",
            "name": "Playlist 1",
            "tracks": {"items": [{"track": {"id": "t1"}}]},
        }
    ]
    connector = SpotifyConnector(db=Session(), client=mock_client)
    result = await connector.sync_playlists()
    assert result["status"] == "success"
    assert result["count"] == 1
    mock_crud.clear_all_playlists_and_tracks.assert_called_once()
    mock_crud.create_or_update_playlist.assert_called_once()


@pytest.mark.asyncio
async def test_sync_playlists_no_client() -> None:
    connector = SpotifyConnector(db=Session())
    with pytest.raises(Exception, match="SpotiClient not initialized."):
        await connector.sync_playlists()
