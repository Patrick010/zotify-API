import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from unittest.mock import MagicMock
from zotify_api.routes import search

client = TestClient(app)

def test_search_disabled_by_default():
    def get_feature_flags_override():
        return {"fork_features": False, "search_advanced": False}

    app.dependency_overrides[search.get_feature_flags] = get_feature_flags_override
    response = client.get("/api/search", params={"q": "test"})
    assert response.status_code == 404
    app.dependency_overrides = {}

def test_search_spotify_fallback():
    def get_feature_flags_override():
        return {"fork_features": True, "search_advanced": True}

    def get_db_engine_override():
        return None

    def get_spotify_search_func_override():
        return lambda q, type, limit, offset: ([{"id": "spotify:track:1", "name": "test", "type": "track", "artist": "test", "album": "test"}], 1)

    app.dependency_overrides[search.get_feature_flags] = get_feature_flags_override
    app.dependency_overrides[search.get_db_engine] = get_db_engine_override
    app.dependency_overrides[search.get_spotify_search_func] = get_spotify_search_func_override
    response = client.get("/api/search", params={"q": "test"})
    assert response.status_code == 200
    body = response.json()
    assert body["data"][0]["id"] == "spotify:track:1"
    app.dependency_overrides = {}

def test_search_db_flow():
    def get_feature_flags_override():
        return {"fork_features": True, "search_advanced": True}

    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value.mappings.return_value.all.return_value = [{"id": "local:track:1", "name": "test", "type": "track", "artist": "test", "album": "test"}]

    def get_db_engine_override():
        return mock_engine

    app.dependency_overrides[search.get_feature_flags] = get_feature_flags_override
    app.dependency_overrides[search.get_db_engine] = get_db_engine_override
    response = client.get("/api/search", params={"q": "test"})
    assert response.status_code == 200
    body = response.json()
    assert body["data"][0]["id"] == "local:track:1"
    app.dependency_overrides = {}

def test_search_db_fails_fallback_to_spotify():
    def get_feature_flags_override():
        return {"fork_features": True, "search_advanced": True}

    mock_engine = MagicMock()
    mock_engine.connect.side_effect = Exception("DB error")

    def get_db_engine_override():
        return mock_engine

    def get_spotify_search_func_override():
        return lambda q, type, limit, offset: ([{"id": "spotify:track:2", "name": "test2", "type": "track", "artist": "test2", "album": "test2"}], 1)

    app.dependency_overrides[search.get_feature_flags] = get_feature_flags_override
    app.dependency_overrides[search.get_db_engine] = get_db_engine_override
    app.dependency_overrides[search.get_spotify_search_func] = get_spotify_search_func_override
    response = client.get("/api/search", params={"q": "test"})
    assert response.status_code == 200
    body = response.json()
    assert body["data"][0]["id"] == "spotify:track:2"
    app.dependency_overrides = {}
