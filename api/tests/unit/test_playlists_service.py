import pytest
from unittest.mock import MagicMock
from zotify_api.services.playlists_service import PlaylistsService, PlaylistsServiceError

@pytest.fixture
def mock_db_engine():
    return MagicMock()

def test_get_playlists_no_db():
    service = PlaylistsService(db_engine=None)
    items, total = service.get_playlists()
    assert items == []
    assert total == 0

def test_get_playlists_with_db(mock_db_engine):
    mock_conn = MagicMock()
    mock_db_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value.mappings.return_value.all.return_value = [
        {"id": "1", "name": "Test Playlist", "description": "A test playlist"},
    ]
    service = PlaylistsService(db_engine=mock_db_engine)
    items, total = service.get_playlists()
    assert len(items) == 1
    assert items[0]["name"] == "Test Playlist"

def test_get_playlists_with_search(mock_db_engine):
    mock_conn = MagicMock()
    mock_db_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value.mappings.return_value.all.return_value = [
        {"id": "1", "name": "Searched Playlist", "description": "A test playlist"},
    ]
    service = PlaylistsService(db_engine=mock_db_engine)
    items, total = service.get_playlists(search="Searched")
    assert len(items) == 1
    assert items[0]["name"] == "Searched Playlist"

def test_create_playlist_no_db():
    service = PlaylistsService(db_engine=None)
    with pytest.raises(PlaylistsServiceError):
        service.create_playlist({"name": "Test Playlist"})

def test_create_playlist_with_db(mock_db_engine):
    mock_conn = MagicMock()
    mock_db_engine.connect.return_value.__enter__.return_value = mock_conn
    service = PlaylistsService(db_engine=mock_db_engine)
    playlist_in = {"name": "Test Playlist", "description": "A test playlist"}
    playlist_out = service.create_playlist(playlist_in)
    assert playlist_out["name"] == playlist_in["name"]

def test_get_playlists_db_error(mock_db_engine):
    mock_db_engine.connect.side_effect = Exception("DB Error")
    service = PlaylistsService(db_engine=mock_db_engine)
    with pytest.raises(PlaylistsServiceError):
        service.get_playlists()

def test_create_playlist_db_error(mock_db_engine):
    mock_db_engine.connect.side_effect = Exception("DB Error")
    service = PlaylistsService(db_engine=mock_db_engine)
    with pytest.raises(PlaylistsServiceError):
        service.create_playlist({"name": "Test Playlist"})
