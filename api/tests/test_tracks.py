import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.services.db import get_db_engine
from unittest.mock import MagicMock
from io import BytesIO

client = TestClient(app)

def test_list_tracks_no_db():
    app.dependency_overrides[get_db_engine] = lambda: None
    response = client.get("/api/tracks")
    assert response.status_code == 200
    body = response.json()
    assert body["data"] == []
    assert body["meta"]["total"] == 0
    app.dependency_overrides.clear()

def test_list_tracks_with_db():
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value.mappings.return_value.all.return_value = [
        {"id": "1", "name": "Test Track", "artist": "Test Artist", "album": "Test Album"},
    ]
    app.dependency_overrides[get_db_engine] = lambda: mock_engine
    response = client.get("/api/tracks")
    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) == 1
    assert body["data"][0]["name"] == "Test Track"
    app.dependency_overrides.clear()

def test_crud_flow_unauthorized():
    response = client.post("/api/tracks", json={"name": "New Track", "artist": "New Artist"})
    assert response.status_code == 401

def test_crud_flow(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    # Create
    mock_conn.execute.return_value.lastrowid = 1
    app.dependency_overrides[get_db_engine] = lambda: mock_engine
    create_payload = {"name": "New Track", "artist": "New Artist"}
    response = client.post("/api/tracks", headers={"X-API-Key": "test_key"}, json=create_payload)
    assert response.status_code == 201
    track_id = response.json()["id"]

    # Get
    mock_conn.execute.return_value.mappings.return_value.first.return_value = {"id": track_id, **create_payload}
    response = client.get(f"/api/tracks/{track_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "New Track"

    # Patch
    update_payload = {"name": "Updated Track"}
    response = client.patch(f"/api/tracks/{track_id}", headers={"X-API-Key": "test_key"}, json=update_payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Track"

    # Delete
    response = client.delete(f"/api/tracks/{track_id}", headers={"X-API-Key": "test_key"})
    assert response.status_code == 204

    app.dependency_overrides.clear()

def test_upload_cover_unauthorized():
    file_content = b"fake image data"
    response = client.post(
        "/api/tracks/1/cover",
        files={"cover_image": ("test.jpg", BytesIO(file_content), "image/jpeg")}
    )
    assert response.status_code == 401

def test_upload_cover(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    mock_engine = MagicMock()
    app.dependency_overrides[get_db_engine] = lambda: mock_engine

    file_content = b"fake image data"
    response = client.post(
        "/api/tracks/1/cover",
        headers={"X-API-Key": "test_key"},
        files={"cover_image": ("test.jpg", BytesIO(file_content), "image/jpeg")}
    )
    assert response.status_code == 200
    assert "cover_url" in response.json()
    app.dependency_overrides.clear()
