import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from unittest.mock import MagicMock

client = TestClient(app)

def test_search_disabled_by_default(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.enable_fork_features", False)
    response = client.get("/api/search", params={"q": "test"})
    assert response.status_code == 404

def test_search_spotify_fallback(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.enable_fork_features", True)
    monkeypatch.setattr("zotify_api.config.settings.feature_search_advanced", True)
    monkeypatch.setattr("zotify_api.services.db.get_db_engine", lambda: None)
    monkeypatch.setattr(
        "zotify_api.services.search.search_spotify",
            lambda q, type, limit, offset: ([{"id": "spotify:track:1", "name": "test", "type": "track", "artist": "test", "album": "test"}], 1),
    )
    response = client.get("/api/search", params={"q": "test"})
    assert response.status_code == 200
    body = response.json()
    assert body["data"][0]["id"] == "spotify:track:1"

def test_search_db_flow(monkeypatch):
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_text = MagicMock()
    mock_conn.execute.return_value.mappings.return_value.all.return_value = [{"id": "local:track:1", "name": "test", "type": "track", "artist": "test", "album": "test"}]
    monkeypatch.setattr("zotify_api.config.settings.enable_fork_features", True)
    monkeypatch.setattr("zotify_api.config.settings.feature_search_advanced", True)
    monkeypatch.setattr("zotify_api.services.db.get_db_engine", lambda: mock_engine)
    monkeypatch.setattr("zotify_api.services.search.text", mock_text)
    response = client.get("/api/search", params={"q": "test"})
    assert response.status_code == 200
    body = response.json()
    assert body["data"][0]["id"] == "local:track:1"
