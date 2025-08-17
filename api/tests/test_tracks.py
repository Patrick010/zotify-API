import pytest
from unittest.mock import MagicMock
from io import BytesIO
from zotify_api.main import app
from zotify_api.services.db import get_db_engine

@pytest.fixture
def mock_db(client):
    """Fixture to mock the database engine."""
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    app.dependency_overrides[get_db_engine] = lambda: mock_engine
    yield mock_engine, mock_conn
    del app.dependency_overrides[get_db_engine]

def test_list_tracks_no_db(client):
    app.dependency_overrides[get_db_engine] = lambda: None
    response = client.get("/api/tracks")
    assert response.status_code == 200
    body = response.json()
    assert body["data"] == []
    assert body["meta"]["total"] == 0
    del app.dependency_overrides[get_db_engine]

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

from unittest.mock import patch
from fastapi import HTTPException

def test_upload_cover(client, mock_db):
    file_content = b"fake image data"
    response = client.post(
        "/api/tracks/1/cover",
        headers={"X-API-Key": "test_key"},
        files={"cover_image": ("test.jpg", BytesIO(file_content), "image/jpeg")}
    )
    assert response.status_code == 200
    assert "cover_url" in response.json()

def test_get_metadata_unauthorized(client):
    response = client.post("/api/tracks/metadata", json={"track_ids": ["id1"]})
    assert response.status_code == 401 # No X-API-Key

from unittest.mock import AsyncMock

from zotify_api.services import auth as auth_service

from fastapi.testclient import TestClient

@patch("zotify_api.services.tracks_service.get_tracks_metadata_from_spotify", new_callable=AsyncMock)
def test_get_metadata_success(mock_get_metadata, client, mock_provider):
    mock_metadata = [{"id": "track1", "name": "Test Track"}]
    mock_get_metadata.return_value = mock_metadata

    response = client.post(
        "/api/tracks/metadata",
        headers={"X-API-Key": "test_key"},
        json={"track_ids": ["track1"]}
    )

    assert response.status_code == 200
    assert response.json() == {"metadata": mock_metadata}
    mock_get_metadata.assert_called_with(["track1"], provider=mock_provider)


def test_get_extended_metadata(client):
    response = client.get("/api/tracks/abc123/metadata")
    assert response.status_code == 200
    assert "title" in response.json()


def test_patch_extended_metadata(client):
    update_data = {"mood": "Energetic", "rating": 5}
    response = client.patch("/api/tracks/abc123/metadata", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@patch("zotify_api.services.tracks_service.get_tracks_metadata_from_spotify", new_callable=AsyncMock)
def test_get_metadata_spotify_error(mock_get_metadata, client, mock_provider):
    # Simulate an error from the service layer (e.g., Spotify is down)
    mock_get_metadata.side_effect = HTTPException(status_code=503, detail="Service unavailable")

    response = client.post(
        "/api/tracks/metadata",
        headers={"X-API-Key": "test_key"},
        json={"track_ids": ["track1"]}
    )
    assert response.status_code == 503
    assert "Service unavailable" in response.json()["detail"]
