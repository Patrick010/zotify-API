from unittest.mock import MagicMock, patch

import pytest

from zotify_api.database import crud
from zotify_api.database.models import DownloadJob, SpotifyToken, Track
from zotify_api.schemas import download as schemas


@pytest.fixture
def db_session() -> MagicMock:
    """Fixture for a mocked database session."""
    session = MagicMock()
    # Mock the query method to return a chainable object
    query_mock = MagicMock()
    session.query.return_value = query_mock
    query_mock.filter.return_value = query_mock
    query_mock.order_by.return_value = query_mock
    query_mock.first.return_value = None
    query_mock.all.return_value = []
    return session


def test_get_spotify_token_found(db_session: MagicMock) -> None:
    mock_token = SpotifyToken(
        access_token="test_access", refresh_token="test_refresh", expires_at=12345
    )
    db_session.query.return_value.first.return_value = mock_token

    token = crud.get_spotify_token(db_session)

    assert token is not None
    assert token.access_token == "test_access"


def test_get_spotify_token_not_found(db_session: MagicMock) -> None:
    db_session.query.return_value.first.return_value = None
    token = crud.get_spotify_token(db_session)
    assert token is None


def test_create_or_update_spotify_token_creates_new(db_session: MagicMock) -> None:
    db_session.query.return_value.first.return_value = None  # No existing token
    token_data = {
        "access_token": "new_access",
        "refresh_token": "new_refresh",
        "expires_at": 67890,
    }

    crud.create_or_update_spotify_token(db_session, token_data)

    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once()


def test_create_or_update_spotify_token_updates_existing(
    db_session: MagicMock,
) -> None:
    mock_token = SpotifyToken(
        access_token="old_access", refresh_token="old_refresh", expires_at=12345
    )
    db_session.query.return_value.first.return_value = mock_token
    token_data = {"access_token": "updated_access", "expires_at": 67890}

    crud.create_or_update_spotify_token(db_session, token_data)

    assert mock_token.access_token == "updated_access"
    assert mock_token.refresh_token == "old_refresh"  # Should not be updated
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once()


def test_delete_spotify_token(db_session: MagicMock) -> None:
    mock_token = SpotifyToken(
        access_token="test_access", refresh_token="test_refresh", expires_at=12345
    )
    db_session.query.return_value.first.return_value = mock_token

    crud.delete_spotify_token(db_session)

    db_session.delete.assert_called_once_with(mock_token)
    db_session.commit.assert_called_once()


def test_delete_spotify_token_not_found(db_session: MagicMock) -> None:
    db_session.query.return_value.first.return_value = None
    crud.delete_spotify_token(db_session)
    db_session.delete.assert_not_called()
    db_session.commit.assert_not_called()


def test_create_download_job(db_session: MagicMock) -> None:
    job_create = schemas.DownloadJobCreate(track_id="test_track")
    crud.create_download_job(db_session, job_create)
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once()


def test_get_download_job(db_session: MagicMock) -> None:
    crud.get_download_job(db_session, "job_123")
    db_session.query.assert_called_with(DownloadJob)
    db_session.query.return_value.filter.assert_called_once()


def test_get_all_download_jobs(db_session: MagicMock) -> None:
    crud.get_all_download_jobs(db_session)
    db_session.query.assert_called_with(DownloadJob)
    db_session.query.return_value.order_by.assert_called_once()


def test_get_next_pending_download_job(db_session: MagicMock) -> None:
    crud.get_next_pending_download_job(db_session)
    db_session.query.assert_called_with(DownloadJob)
    db_session.query.return_value.filter.assert_called_once()
    db_session.query.return_value.order_by.assert_called_once()


def test_update_download_job_status(db_session: MagicMock) -> None:
    mock_job = DownloadJob(job_id="job_123")
    crud.update_download_job_status(
        db_session, mock_job, schemas.DownloadJobStatus.COMPLETED, progress=100
    )
    assert mock_job.status == "completed"
    assert mock_job.progress == 100
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(mock_job)


def test_retry_failed_download_jobs(db_session: MagicMock) -> None:
    crud.retry_failed_download_jobs(db_session)
    db_session.query.assert_called_with(DownloadJob)
    db_session.query.return_value.filter.assert_called_once()
    db_session.query.return_value.filter.return_value.update.assert_called_once()
    db_session.commit.assert_called_once()


def test_get_or_create_track_exists(db_session: MagicMock) -> None:
    mock_track = Track(id="track_123", name="Test Track")
    db_session.query.return_value.filter.return_value.first.return_value = mock_track
    track = crud.get_or_create_track(db_session, "track_123", "Test Track")
    assert track == mock_track
    db_session.add.assert_not_called()


def test_get_or_create_track_creates(db_session: MagicMock) -> None:
    db_session.query.return_value.filter.return_value.first.return_value = None
    track = crud.get_or_create_track(db_session, "track_123", "Test Track")
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once()
    assert track.id == "track_123"
    assert track.name == "Test Track"


def test_create_or_update_playlist_creates_new(db_session: MagicMock) -> None:
    db_session.query.return_value.filter.return_value.first.return_value = None

    with patch("zotify_api.database.crud.get_or_create_track") as mock_get_track:
        mock_get_track.return_value = Track(id="track_1")

        crud.create_or_update_playlist(
            db_session, "playlist_1", "My Playlist", ["track_1"]
        )

        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
        db_session.refresh.assert_called_once()


def test_clear_all_playlists_and_tracks(db_session: MagicMock) -> None:
    crud.clear_all_playlists_and_tracks(db_session)
    assert db_session.query.return_value.delete.call_count == 3
    db_session.commit.assert_called_once()
