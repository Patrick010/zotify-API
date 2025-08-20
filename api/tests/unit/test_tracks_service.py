from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from zotify_api.services import tracks_service


def test_get_tracks_no_db():
    items, total = tracks_service.get_tracks(engine=None)
    assert items == []
    assert total == 0


def test_get_tracks_with_db():
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value.mappings.return_value.all.return_value = [
        {
            "id": "1",
            "name": "Test Track",
            "artist": "Test Artist",
            "album": "Test Album",
        },
    ]
    items, total = tracks_service.get_tracks(engine=mock_engine)
    assert len(items) == 1
    assert total == 1
    assert items[0]["name"] == "Test Track"


def test_get_tracks_db_fails():
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = Exception("DB error")
    items, total = tracks_service.get_tracks(engine=mock_engine)
    assert items == []
    assert total == 0


def test_search_tracks_spotify_fallback():
    items, total = tracks_service.search_tracks(
        q="test", limit=10, offset=0, engine=None
    )
    assert total == 0
    assert items == []


def test_create_track_no_db(monkeypatch):
    monkeypatch.setattr(
        "zotify_api.services.tracks_service.get_db_engine", lambda: None
    )
    with pytest.raises(Exception, match="No DB engine available"):
        payload = {
            "name": "test",
            "artist": "test",
            "album": "test",
            "duration_seconds": 1,
            "path": "test",
        }
        tracks_service.create_track(payload=payload)


def test_get_track_no_db():
    track = tracks_service.get_track(track_id="1", engine=None)
    assert track is None


def test_get_track_success():
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value.mappings.return_value.first.return_value = {
        "id": "1",
        "name": "Test",
    }
    track = tracks_service.get_track("1", engine=mock_engine)
    assert track is not None
    assert track["name"] == "Test"


def test_get_track_db_fails():
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = Exception("DB error")
    track = tracks_service.get_track("1", engine=mock_engine)
    assert track is None


def test_create_track_success():
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    payload = {
        "name": "test",
        "artist": "test",
        "album": "test",
        "duration_seconds": 1,
        "path": "test",
    }
    track = tracks_service.create_track(payload, engine=mock_engine)
    assert track["name"] == "test"
    mock_conn.execute.assert_called_once()


def test_create_track_db_fails():
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        payload = {
            "name": "test",
            "artist": "test",
            "album": "test",
            "duration_seconds": 1,
            "path": "test",
        }
        tracks_service.create_track(payload, engine=mock_engine)


def test_update_track_success():
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    with patch("zotify_api.services.tracks_service.get_track") as mock_get:
        mock_get.return_value = {"id": "1", "name": "Old Name"}
        payload = {"name": "New Name"}
        track = tracks_service.update_track("1", payload, engine=mock_engine)
        assert track["name"] == "New Name"
        mock_conn.execute.assert_called_once()


def test_delete_track_success():
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    tracks_service.delete_track("1", engine=mock_engine)
    mock_conn.execute.assert_called_once()


def test_delete_track_db_fails():
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        tracks_service.delete_track("1", engine=mock_engine)


def test_upload_cover():
    result = tracks_service.upload_cover("1", b"")
    assert result["track_id"] == "1"
    assert "cover_url" in result


@pytest.mark.asyncio
async def test_get_tracks_metadata_from_spotify():
    from zotify_api.providers.base import BaseProvider

    mock_provider = MagicMock(spec=BaseProvider)
    mock_provider.client = MagicMock()
    mock_provider.client.get_tracks_metadata = AsyncMock(return_value=[{"id": "1"}])

    metadata = await tracks_service.get_tracks_metadata_from_spotify(
        ["1"], mock_provider
    )
    assert len(metadata) == 1
    assert metadata[0]["id"] == "1"
