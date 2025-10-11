# ID: API-240
from typing import Any
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from zotify_api.main import app
from zotify_api.services.db import get_db_engine

client = TestClient(app)


def test_list_playlists_no_db() -> None:
    app.dependency_overrides[get_db_engine] = lambda: None
    resp = client.get("/api/playlists")
    assert resp.status_code == 200
    body = resp.json()
    assert body["data"] == []
    assert body["meta"]["total"] == 0
    del app.dependency_overrides[get_db_engine]


def test_list_playlists_with_db() -> None:
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value.mappings.return_value.all.return_value = [
        {"id": "1", "name": "My List", "description": "desc"},
    ]
    app.dependency_overrides[get_db_engine] = lambda: mock_engine
    resp = client.get("/api/playlists?limit=10&offset=0")
    assert resp.status_code == 200
    assert resp.json()["data"][0]["name"] == "My List"
    del app.dependency_overrides[get_db_engine]


def test_create_playlist_validation() -> None:
    resp = client.post("/api/playlists", json={"name": ""})
    assert resp.status_code == 422


def test_create_playlist_db_failure() -> None:
    def broken_engine() -> Any:
        class Broken:
            def connect(self) -> None:
                raise Exception("boom")

        return Broken()

    app.dependency_overrides[get_db_engine] = lambda: broken_engine()
    resp = client.post("/api/playlists", json={"name": "abc"})
    assert resp.status_code == 503
    del app.dependency_overrides[get_db_engine]


def test_create_playlist() -> None:
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    app.dependency_overrides[get_db_engine] = lambda: mock_engine
    resp = client.post("/api/playlists", json={"name": "My new playlist"})
    assert resp.status_code == 201
    assert resp.json()["name"] == "My new playlist"
    del app.dependency_overrides[get_db_engine]
