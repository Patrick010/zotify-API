import pytest
from unittest.mock import MagicMock
from io import BytesIO
from zotify_api.main import app
from zotify_api.services.db import get_db_engine

@pytest.fixture
def mock_db():
    """Fixture to mock the database engine."""
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    original_override = app.dependency_overrides.get(get_db_engine)
    app.dependency_overrides[get_db_engine] = lambda: mock_engine
    yield mock_engine, mock_conn
    app.dependency_overrides[get_db_engine] = original_override

def test_list_tracks_no_db(client):
    app.dependency_overrides[get_db_engine] = lambda: None
    response = client.get("/api/tracks")
    assert response.status_code == 200
    body = response.json()
    assert body["data"] == []
    assert body["meta"]["total"] == 0
    app.dependency_overrides.clear()

def test_list_tracks_with_db(client, mock_db):
    mock_engine, mock_conn = mock_db
    mock_conn.execute.return_value.mappings.return_value.all.return_value = [
        {"id": "1", "name": "Test Track", "artist": "Test Artist", "album": "Test Album"},
    ]
    response = client.get("/api/tracks")
    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) == 1
    assert body["data"][0]["name"] == "Test Track"

def test_crud_flow_unauthorized(client):
    response = client.post("/api/tracks", json={"name": "New Track", "artist": "New Artist"})
    assert response.status_code == 401

def test_crud_flow(client, mock_db):
    mock_engine, mock_conn = mock_db

    # Create
    mock_conn.execute.return_value.lastrowid = 1
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

def test_upload_cover_unauthorized(client):
    file_content = b"fake image data"
    response = client.post(
        "/api/tracks/1/cover",
        files={"cover_image": ("test.jpg", BytesIO(file_content), "image/jpeg")}
    )
    assert response.status_code == 401

def test_upload_cover(client, mock_db):
    file_content = b"fake image data"
    response = client.post(
        "/api/tracks/1/cover",
        headers={"X-API-Key": "test_key"},
        files={"cover_image": ("test.jpg", BytesIO(file_content), "image/jpeg")}
    )
    assert response.status_code == 200
    assert "cover_url" in response.json()
