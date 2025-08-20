import pytest
from unittest.mock import MagicMock, call, patch
from zotify_api.database import crud, models
from zotify_api.schemas import download as schemas

def test_get_spotify_token_found():
    """ Tests retrieving a token when it exists. """
    mock_db = MagicMock()
    mock_token = models.SpotifyToken(access_token="test")

    # Configure the mock session to return the token
    mock_db.query.return_value.first.return_value = mock_token

    token = crud.get_spotify_token(mock_db)

    mock_db.query.assert_called_once_with(models.SpotifyToken)
    assert token is mock_token

def test_get_spotify_token_not_found():
    """ Tests retrieving a token when it does not exist. """
    mock_db = MagicMock()

    # Configure the mock session to return None
    mock_db.query.return_value.first.return_value = None

    token = crud.get_spotify_token(mock_db)

    mock_db.query.assert_called_once_with(models.SpotifyToken)
    assert token is None


def test_create_or_update_spotify_token_creates_new():
    """ Tests creating a spotify token when one does not exist """
    mock_db = MagicMock()
    mock_db.query.return_value.first.return_value = None # Simulate no existing token

    token_data = {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token",
        "expires_at": "2025-01-01T00:00:00Z",
    }

    new_token = crud.create_or_update_spotify_token(mock_db, token_data)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert new_token.access_token == "new_access_token"


def test_create_or_update_spotify_token_updates_existing():
    """ Tests updating a spotify token when one already exists """
    mock_db = MagicMock()
    existing_token = models.SpotifyToken(access_token="old", refresh_token="old", expires_at="old")
    mock_db.query.return_value.first.return_value = existing_token

    token_data = {
        "access_token": "updated_access_token",
        "refresh_token": "updated_refresh_token",
        "expires_at": "2026-01-01T00:00:00Z",
    }

    updated_token = crud.create_or_update_spotify_token(mock_db, token_data)

    mock_db.add.assert_not_called()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(existing_token)
    assert updated_token.access_token == "updated_access_token"
    assert updated_token.refresh_token == "updated_refresh_token"


def test_delete_spotify_token():
    """ Tests deleting a token """
    mock_db = MagicMock()
    mock_token = models.SpotifyToken()
    mock_db.query.return_value.first.return_value = mock_token

    crud.delete_spotify_token(mock_db)

    mock_db.delete.assert_called_once_with(mock_token)
    mock_db.commit.assert_called_once()


def test_delete_spotify_token_not_found():
    """ Tests that delete does nothing if token is not found """
    mock_db = MagicMock()
    mock_db.query.return_value.first.return_value = None

    crud.delete_spotify_token(mock_db)

    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()

# --- DownloadJob Tests ---

def test_create_download_job():
    mock_db = MagicMock()
    job_schema = schemas.DownloadJobCreate(track_id="test_track")

    db_job = crud.create_download_job(mock_db, job_schema)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert db_job.track_id == "test_track"

def test_get_download_job():
    mock_db = MagicMock()
    crud.get_download_job(mock_db, "job_id_1")
    mock_db.query.assert_called_once_with(models.DownloadJob)
    mock_db.query.return_value.filter.assert_called_once()

def test_get_all_download_jobs():
    mock_db = MagicMock()
    crud.get_all_download_jobs(mock_db)
    mock_db.query.assert_called_once_with(models.DownloadJob)
    mock_db.query.return_value.order_by.return_value.all.assert_called_once()

def test_get_next_pending_download_job():
    mock_db = MagicMock()
    crud.get_next_pending_download_job(mock_db)
    mock_db.query.assert_called_once_with(models.DownloadJob)
    mock_db.query.return_value.filter.return_value.order_by.return_value.first.assert_called_once()

def test_update_download_job_status():
    mock_db = MagicMock()
    mock_job = models.DownloadJob()

    crud.update_download_job_status(mock_db, mock_job, schemas.DownloadJobStatus.IN_PROGRESS, progress=50.0)

    assert mock_job.status == "in_progress"
    assert mock_job.progress == 50.0
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_job)

def test_retry_failed_download_jobs():
    mock_db = MagicMock()
    query_mock = mock_db.query.return_value
    query_mock.filter.return_value.update.return_value = 2 # Simulate 2 rows updated

    count = crud.retry_failed_download_jobs(mock_db)

    query_mock.filter.return_value.update.assert_called_once_with(
        {"status": "pending", "error_message": None}
    )
    mock_db.commit.assert_called_once()
    assert count == 2

# --- Playlist and Track Tests ---

def test_get_or_create_track_exists():
    mock_db = MagicMock()
    mock_track = models.Track(id="existing_id", name="Existing Track")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_track

    track = crud.get_or_create_track(mock_db, "existing_id")

    mock_db.add.assert_not_called()
    assert track == mock_track

def test_get_or_create_track_creates():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    track = crud.get_or_create_track(mock_db, "new_id", "New Track")

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert track.id == "new_id"

def test_clear_all_playlists_and_tracks():
    mock_db = MagicMock()
    crud.clear_all_playlists_and_tracks(mock_db)

    assert mock_db.query.call_count == 3
    assert mock_db.commit.call_count == 1

def test_create_or_update_playlist_creates_new():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None # No existing playlist

    # Mock get_or_create_track to avoid its internal logic
    with patch("zotify_api.database.crud.get_or_create_track") as mock_get_or_create:
        mock_get_or_create.side_effect = lambda db, track_id: models.Track(id=track_id)

        playlist = crud.create_or_update_playlist(mock_db, "pl1", "New PL", ["t1", "t2"])

        mock_db.add.assert_called_once() # For the playlist
        assert mock_get_or_create.call_count == 2
        assert len(playlist.tracks) == 2
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
