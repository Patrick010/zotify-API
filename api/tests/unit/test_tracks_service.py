import pytest
from unittest.mock import MagicMock
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
        {"id": "1", "name": "Test Track", "artist": "Test Artist", "album": "Test Album"},
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
    items, total = tracks_service.search_tracks(q="test", limit=10, offset=0, engine=None)
    assert total == 0
    assert items == []

def test_create_track_no_db(monkeypatch):
    monkeypatch.setattr("zotify_api.services.tracks_service.get_db_engine", lambda: None)
    with pytest.raises(Exception, match="No DB engine available"):
        payload = {"name": "test", "artist": "test", "album": "test", "duration_seconds": 1, "path": "test"}
        tracks_service.create_track(payload=payload)

def test_get_track_no_db():
    track = tracks_service.get_track(track_id="1", engine=None)
    assert track is None
