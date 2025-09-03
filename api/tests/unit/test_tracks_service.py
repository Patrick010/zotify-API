from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from zotify_api.database import models
from zotify_api.services import tracks_service


def test_get_tracks_no_db() -> None:
    items, total = tracks_service.get_tracks(db=None)
    assert items == []
    assert total == 0


@patch("zotify_api.database.crud.get_tracks")
def test_get_tracks_with_db(mock_get_tracks: MagicMock) -> None:
    mock_db = MagicMock(spec=Session)
    mock_get_tracks.return_value = [
        models.Track(
            id="1", name="Test Track", artist="Test Artist", album="Test Album"
        )
    ]
    items, total = tracks_service.get_tracks(db=mock_db)
    assert len(items) == 1
    assert total == 1
    assert items[0]["name"] == "Test Track"


@patch("zotify_api.database.crud.get_tracks")
def test_get_tracks_db_fails(mock_get_tracks: MagicMock) -> None:
    mock_db = MagicMock(spec=Session)
    mock_get_tracks.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        tracks_service.get_tracks(db=mock_db)


@patch("zotify_api.database.crud.get_tracks")
def test_search_tracks(mock_get_tracks: MagicMock) -> None:
    mock_db = MagicMock(spec=Session)
    mock_get_tracks.return_value = []
    items, total = tracks_service.search_tracks(
        db=mock_db, q="test", limit=10, offset=0
    )
    assert total == 0
    assert items == []


def test_get_track_no_db() -> None:
    track = tracks_service.get_track(db=None, track_id="1")
    assert track is None


@patch("zotify_api.database.crud.get_track")
def test_get_track_success(mock_get_track: MagicMock) -> None:
    mock_db = MagicMock(spec=Session)
    mock_get_track.return_value = models.Track(id="1", name="Test")
    track = tracks_service.get_track(mock_db, "1")
    assert track is not None
    assert track["name"] == "Test"


@patch("zotify_api.database.crud.get_track")
def test_get_track_db_fails(mock_get_track: MagicMock) -> None:
    mock_db = MagicMock(spec=Session)
    mock_get_track.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        tracks_service.get_track(mock_db, "1")


@patch("zotify_api.database.crud.create_track")
def test_create_track_success(mock_create_track: MagicMock) -> None:
    mock_db = MagicMock(spec=Session)
    payload = {
        "name": "test",
        "artist": "test",
        "album": "test",
    }
    mock_create_track.return_value = models.Track(id="1", **payload)
    track = tracks_service.create_track(mock_db, payload)
    assert track["name"] == "test"
    mock_create_track.assert_called_once_with(mock_db, payload)


@patch("zotify_api.database.crud.create_track")
def test_create_track_db_fails(mock_create_track: MagicMock) -> None:
    mock_db = MagicMock(spec=Session)
    mock_create_track.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        payload = {
            "name": "test",
            "artist": "test",
            "album": "test",
        }
        tracks_service.create_track(mock_db, payload)


@patch("zotify_api.database.crud.update_track")
def test_update_track_success(mock_update_track: MagicMock) -> None:
    mock_db = MagicMock(spec=Session)
    payload = {"name": "New Name"}
    mock_update_track.return_value = models.Track(id="1", **payload)
    track = tracks_service.update_track(mock_db, "1", payload)
    assert track is not None
    assert track["name"] == "New Name"
    mock_update_track.assert_called_once_with(mock_db, "1", payload)


@patch("zotify_api.database.crud.delete_track")
def test_delete_track_success(mock_delete_track: MagicMock) -> None:
    mock_db = MagicMock(spec=Session)
    tracks_service.delete_track(mock_db, "1")
    mock_delete_track.assert_called_once_with(mock_db, "1")


@patch("zotify_api.database.crud.delete_track")
def test_delete_track_db_fails(mock_delete_track: MagicMock) -> None:
    mock_db = MagicMock(spec=Session)
    mock_delete_track.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        tracks_service.delete_track(mock_db, "1")


def test_upload_cover() -> None:
    result = tracks_service.upload_cover("1", b"")
    assert result["track_id"] == "1"
    assert "cover_url" in result


@pytest.mark.asyncio
async def test_get_tracks_metadata_from_spotify() -> None:
    from zotify_api.providers.base import BaseProvider

    mock_provider = MagicMock(spec=BaseProvider)
    mock_provider.client = MagicMock()
    mock_provider.client.get_tracks_metadata = AsyncMock(return_value=[{"id": "1"}])

    metadata = await tracks_service.get_tracks_metadata_from_spotify(
        ["1"], mock_provider
    )
    assert len(metadata) == 1
    assert metadata[0]["id"] == "1"
