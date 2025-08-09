import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from zotify_api.auth_state import pending_states, spotify_tokens

@patch("zotify_api.services.spotify.sync_playlists", new_callable=AsyncMock)
@patch("zotify_api.services.spotify.get_me", new_callable=AsyncMock)
def test_sync_playlists_success(mock_get_me, mock_sync, client):
    """ Test syncing playlists """
    mock_get_me.return_value = {"id": "testuser"}
    mock_sync.return_value = {"status": "success", "count": 5}
    response = client.post("/api/spotify/sync_playlists", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json()["count"] == 5

@patch("zotify_api.services.spotify.get_playlists", new_callable=AsyncMock)
def test_get_playlists_success(mock_get_playlists, client):
    mock_get_playlists.return_value = {"items": [{"id": "p1", "name": "Playlist 1"}]}
    response = client.get("/api/spotify/playlists", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert "items" in response.json()

@patch("zotify_api.services.spotify.create_playlist", new_callable=AsyncMock)
@patch("zotify_api.services.spotify.get_me", new_callable=AsyncMock)
def test_create_playlist_success(mock_get_me, mock_create_playlist, client):
    mock_get_me.return_value = {"id": "testuser"}
    mock_create_playlist.return_value = {
        "id": "new_p1",
        "name": "New Playlist",
        "public": True,
        "collaborative": False,
        "description": "Desc",
        "tracks": {"href": "some_url", "total": 0}
    }
    payload = {"name": "New Playlist", "public": True, "collaborative": False, "description": "Desc"}
    response = client.post("/api/spotify/playlists", headers={"X-API-Key": "test_key"}, json=payload)
    assert response.status_code == 201
    assert response.json()["id"] == "new_p1"

@patch("zotify_api.services.spotify.add_tracks_to_playlist", new_callable=AsyncMock)
def test_add_tracks_success(mock_add_tracks, client):
    mock_add_tracks.return_value = {"snapshot_id": "snapshot1"}
    payload = {"uris": ["uri1", "uri2"]}
    response = client.post("/api/spotify/playlists/p1/tracks", headers={"X-API-Key": "test_key"}, json=payload)
    assert response.status_code == 201
    assert "snapshot_id" in response.json()

@patch("zotify_api.services.spotify.unfollow_playlist", new_callable=AsyncMock)
def test_delete_playlist_success(mock_unfollow, client):
    response = client.delete("/api/spotify/playlists/p1", headers={"X-API-Key": "test_key"})
    assert response.status_code == 204

@patch("zotify_api.services.spotify.get_me", new_callable=AsyncMock)
def test_get_me_success(mock_get_me, client):
    """
    Tests the /api/spotify/me endpoint, mocking the service call.
    """
    mock_user_profile = {"id": "user1", "display_name": "Test User"}
    mock_get_me.return_value = mock_user_profile

    response = client.get("/api/spotify/me", headers={"X-API-Key": "test_key"})

    assert response.status_code == 200
    assert response.json() == mock_user_profile
    mock_get_me.assert_called_once()

@patch("zotify_api.services.spotify.get_me", new_callable=AsyncMock)
def test_get_me_unauthorized(mock_get_me, client):
    """
    Tests that the /api/spotify/me endpoint is protected by the admin API key.
    """
    response = client.get("/api/spotify/me") # No X-API-Key header
    assert response.status_code == 401
    mock_get_me.assert_not_called()
