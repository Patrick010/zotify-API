import pytest

def test_sync_playlists_success(client, mock_provider):
    """ Test syncing playlists """
    response = client.post("/api/spotify/sync_playlists", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json()["count"] == 1

def test_sync_playlists_unauthorized(client, mock_provider):
    """ Test that sync_playlists is protected by the admin API key. """
    response = client.post("/api/spotify/sync_playlists")
    assert response.status_code == 401
