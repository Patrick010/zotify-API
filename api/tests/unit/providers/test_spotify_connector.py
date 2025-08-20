import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from sqlalchemy.orm import Session
from zotify_api.providers.spotify_connector import SpotifyConnector
from zotify_api.providers import spotify_connector as sc_module


@pytest.mark.asyncio
@patch("zotify_api.providers.spotify_connector.crud.create_or_update_spotify_token")
@patch("httpx.AsyncClient")
async def test_handle_oauth_callback_success(mock_AsyncClient, mock_crud_call, monkeypatch):
    """ Tests the happy path for the OAuth callback handler """
    mock_db = Session()
    connector = SpotifyConnector(db=mock_db)

    # Configure the mock for the async context manager
    mock_client_instance = AsyncMock()

    # Configure the response from the 'post' call
    mock_post_response = AsyncMock()
    mock_post_response.json.return_value = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600
    }
    mock_post_response.raise_for_status.return_value = None
    mock_client_instance.post.return_value = mock_post_response

    # Make the AsyncClient return our configured instance when used as a context manager
    mock_AsyncClient.return_value.__aenter__.return_value = mock_client_instance

    monkeypatch.setitem(__import__("zotify_api.auth_state").auth_state.pending_states, "test_state", "test_code_verifier")

    html_response = await connector.handle_oauth_callback(code="test_code", error=None, state="test_state")

    mock_crud_call.assert_called_once()
    assert "Successfully authenticated" in html_response

@pytest.mark.asyncio
async def test_handle_oauth_callback_error():
    """ Tests the failure path for the OAuth callback handler """
    mock_db = Session()
    connector = SpotifyConnector(db=mock_db)

    html_response = await connector.handle_oauth_callback(code=None, error="access_denied", state="test_state")

    assert "Authentication Failed" in html_response
    assert "access_denied" in html_response


@pytest.mark.asyncio
@patch("zotify_api.providers.spotify_connector.secrets.token_bytes", return_value=b'test_verifier_bytes')
@patch("zotify_api.providers.spotify_connector.hashlib.sha256")
async def test_get_oauth_login_url(mock_sha256, mock_token_bytes, monkeypatch):
    """ Tests the construction of the OAuth login URL. """
    # Mock the hashing to produce a predictable challenge
    mock_digest = MagicMock()
    mock_digest.digest.return_value = b'test_challenge_bytes'
    mock_sha256.return_value = mock_digest

    mock_db = Session()
    connector = SpotifyConnector(db=mock_db)

    # Correctly target the dictionary where it's used by patching the module directly
    monkeypatch.setattr(sc_module, "pending_states", {})

    test_state = "new_test_state"
    auth_url = await connector.get_oauth_login_url(state=test_state)

    assert "https://accounts.spotify.com/authorize" in auth_url
    assert f"&state={test_state}" in auth_url
    assert "&code_challenge_method=S256" in auth_url

    # b'test_verifier_bytes' -> 'dGVzdF92ZXJpZmllcl9ieXRlcw'
    # b'test_challenge_bytes' -> 'dGVzdF9jaGFsbGVuZ2VfYnl0ZXM'
    assert "code_challenge=dGVzdF9jaGFsbGVuZ2VfYnl0ZXM" in auth_url

    # Now, check the state of the dictionary on the module itself
    assert sc_module.pending_states[test_state] == 'dGVzdF92ZXJpZmllcl9ieXRlcw'


@pytest.mark.asyncio
async def test_search_success():
    """ Tests the search method happy path """
    mock_db = Session()
    mock_spoti_client = AsyncMock()
    mock_spoti_client.search.return_value = {
        "tracks": {
            "items": [{"name": "Test Track"}],
            "total": 1
        }
    }

    connector = SpotifyConnector(db=mock_db, client=mock_spoti_client)

    items, total = await connector.search(q="test", type="track", limit=10, offset=0)

    mock_spoti_client.search.assert_called_once_with(q="test", type="track", limit=10, offset=0)
    assert total == 1
    assert len(items) == 1
    assert items[0]["name"] == "Test Track"


@pytest.mark.asyncio
async def test_search_no_client():
    """ Tests that search raises an exception if the client is not initialized """
    mock_db = Session()
    connector = SpotifyConnector(db=mock_db, client=None)

    with pytest.raises(Exception, match="SpotiClient not initialized."):
        await connector.search(q="test", type="track", limit=10, offset=0)


@pytest.mark.asyncio
async def test_get_playlist_success():
    """ Tests the get_playlist method happy path """
    mock_db = Session()
    mock_spoti_client = AsyncMock()
    mock_spoti_client.get_playlist.return_value = {"id": "test_id", "name": "Test Playlist"}

    connector = SpotifyConnector(db=mock_db, client=mock_spoti_client)

    playlist = await connector.get_playlist("test_id")

    mock_spoti_client.get_playlist.assert_called_once_with("test_id")
    assert playlist["name"] == "Test Playlist"


@pytest.mark.asyncio
async def test_get_playlist_no_client():
    """ Tests that get_playlist raises an exception if the client is not initialized """
    mock_db = Session()
    connector = SpotifyConnector(db=mock_db, client=None)

    with pytest.raises(Exception, match="SpotiClient not initialized."):
        await connector.get_playlist("test_id")


@pytest.mark.asyncio
async def test_get_playlist_tracks_success():
    """ Tests the get_playlist_tracks method happy path """
    mock_db = Session()
    mock_spoti_client = AsyncMock()
    mock_spoti_client.get_playlist_tracks.return_value = {"items": [{"track": {"name": "Test Track"}}]}

    connector = SpotifyConnector(db=mock_db, client=mock_spoti_client)

    tracks = await connector.get_playlist_tracks("test_id", limit=50, offset=0)

    mock_spoti_client.get_playlist_tracks.assert_called_once_with("test_id", limit=50, offset=0)
    assert "items" in tracks


@pytest.mark.asyncio
async def test_get_playlist_tracks_no_client():
    """ Tests that get_playlist_tracks raises an exception if the client is not initialized """
    mock_db = Session()
    connector = SpotifyConnector(db=mock_db, client=None)

    with pytest.raises(Exception, match="SpotiClient not initialized."):
        await connector.get_playlist_tracks("test_id", limit=50, offset=0)


@pytest.mark.asyncio
@patch("zotify_api.providers.spotify_connector.crud")
async def test_sync_playlists_success(mock_crud):
    """ Tests the sync_playlists method happy path """
    mock_db = Session()
    mock_spoti_client = AsyncMock()
    mock_spoti_client.get_all_current_user_playlists.return_value = [
        {"id": "pl1", "name": "Playlist 1", "tracks": {"items": [{"track": {"id": "t1"}}]}},
        {"id": "pl2", "name": "Playlist 2", "tracks": {"items": [{"track": {"id": "t2"}}]}},
    ]

    connector = SpotifyConnector(db=mock_db, client=mock_spoti_client)

    result = await connector.sync_playlists()

    mock_spoti_client.get_all_current_user_playlists.assert_called_once()
    mock_crud.clear_all_playlists_and_tracks.assert_called_once_with(mock_db)
    assert mock_crud.create_or_update_playlist.call_count == 2
    assert result["count"] == 2


@pytest.mark.asyncio
async def test_sync_playlists_no_client():
    """ Tests that sync_playlists raises an exception if the client is not initialized """
    mock_db = Session()
    connector = SpotifyConnector(db=mock_db, client=None)

    with pytest.raises(Exception, match="SpotiClient not initialized."):
        await connector.sync_playlists()
