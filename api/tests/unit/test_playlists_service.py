from unittest.mock import MagicMock

import pytest

from zotify_api.services.playlists_service import (
    PlaylistsService,
    PlaylistsServiceError,
)


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

def test_normalization_logic():
    service = PlaylistsService(db_engine=None)
    assert service._normalize_limit(10) == 10
    assert service._normalize_limit(999) == 250
    assert service._normalize_limit(-1) == 25
    assert service._normalize_limit("a") == 25
    assert service._normalize_offset(10) == 10
    assert service._normalize_offset(-1) == 0
    assert service._normalize_offset("a") == 0

def test_get_limits():
    service = PlaylistsService(db_engine=None)
    assert isinstance(service.get_default_limit(), int)
    assert isinstance(service.get_max_limit(), int)

def test_get_playlists_service_dependency():
    from zotify_api.services.playlists_service import get_playlists_service

    def mock_get_db_engine():
        return MagicMock()

    dependency = get_playlists_service(db_engine=mock_get_db_engine())
    assert isinstance(dependency, PlaylistsService)
