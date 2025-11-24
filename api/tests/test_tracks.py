from io import BytesIO
from typing import Any, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from zotify_api.main import app
from zotify_api.services.db import get_db_engine


@pytest.fixture
def mock_db(client: TestClient) -> Generator[Any, None, None]:
    """Fixture to mock the database engine."""
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    app.dependency_overrides[get_db_engine] = lambda: mock_engine
    yield mock_engine, mock_conn
    del app.dependency_overrides[get_db_engine]


def test_list_tracks_no_db(client: TestClient) -> None:
    app.dependency_overrides[get_db_engine] = lambda: None
    response = client.get("/api/tracks")
    assert response.status_code == 200
    body = response.json()
    assert body["data"] == []
    assert body["meta"]["total"] == 0
    del app.dependency_overrides[get_db_engine]


def test_list_tracks_with_db(client: TestClient, mock_db: Any) -> None:
    mock_engine, mock_conn = mock_db
    mock_conn.execute.return_value.mappings.return_value.all.return_value = [
        {
            "id": "1",
            "name": "Test Track",
            "artist": "Test Artist",
            "album": "Test Album",
        },
    ]
    response = client.get("/api/tracks")
    assert response.status_code == 200
    body = response.json()
    assert len(body["data"]) == 1
    assert body["data"][0]["name"] == "Test Track"


def test_crud_flow_unauthorized(client: TestClient) -> None:
    response = client.post(
        "/api/tracks", json={"name": "New Track", "artist": "New Artist"}
    )
    assert response.status_code == 401


def test_crud_flow(client: TestClient, mock_db: Any) -> None:
    mock_engine, mock_conn = mock_db

    # Create
    mock_conn.execute.return_value.lastrowid = 1
    create_payload = {"name": "New Track", "artist": "New Artist"}
    response = client.post(
        "/api/tracks", headers={"X-API-Key": "test_key"}, json=create_payload
    )
    assert response.status_code == 201
    track_id = response.json()["id"]

    # Get
    mock_conn.execute.return_value.mappings.return_value.first.return_value = {
        "id": track_id,
        **create_payload,
    }
    response = client.get(f"/api/tracks/{track_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "New Track"

    # Patch
    update_payload = {"name": "Updated Track"}
    response = client.patch(
        f"/api/tracks/{track_id}",
        headers={"X-API-Key": "test_key"},
        json=update_payload,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Track"

    # Delete
    response = client.delete(
        f"/api/tracks/{track_id}", headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == 204


def test_upload_cover_unauthorized(client: TestClient) -> None:
    file_content = b"fake image data"
    response = client.post(
        "/api/tracks/1/cover",
        files={"cover_image": ("test.jpg", BytesIO(file_content), "image/jpeg")},
    )
    assert response.status_code == 401


def test_upload_cover(client: TestClient, mock_db: Any) -> None:
    file_content = b"fake image data"
    response = client.post(
        "/api/tracks/1/cover",
        headers={"X-API-Key": "test_key"},
        files={"cover_image": ("test.jpg", BytesIO(file_content), "image/jpeg")},
    )
    assert response.status_code == 200
    assert "cover_url" in response.json()


def test_get_metadata_unauthorized(client: TestClient) -> None:
    response = client.post("/api/tracks/metadata", json={"track_ids": ["id1"]})
    assert response.status_code == 401  # No X-API-Key


@patch(
    "zotify_api.services.tracks_service.get_tracks_metadata_from_spotify",
    new_callable=AsyncMock,
)
def test_get_metadata_success(
    mock_get_metadata: AsyncMock, client: TestClient, mock_provider: MagicMock
) -> None:
    mock_metadata = [{"id": "track1", "name": "Test Track"}]
    mock_get_metadata.return_value = mock_metadata

    response = client.post(
        "/api/tracks/metadata",
        headers={"X-API-Key": "test_key"},
        json={"track_ids": ["track1"]},
    )

    assert response.status_code == 200
    assert response.json() == {"metadata": mock_metadata}
    mock_get_metadata.assert_called_with(["track1"], provider=mock_provider)


def test_get_extended_metadata(client: TestClient) -> None:
    response = client.get("/api/tracks/abc123/metadata")
    assert response.status_code == 200
    assert "title" in response.json()


def test_patch_extended_metadata(client: TestClient) -> None:
    update_data = {"mood": "Energetic", "rating": 5}
    response = client.patch("/api/tracks/abc123/metadata", json=update_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@patch(
    "zotify_api.services.tracks_service.get_tracks_metadata_from_spotify",
    new_callable=AsyncMock,
)
def test_get_metadata_spotify_error(
    mock_get_metadata: AsyncMock, client: TestClient, mock_provider: MagicMock
) -> None:
    # Simulate an error from the service layer (e.g., Spotify is down)
    mock_get_metadata.side_effect = HTTPException(
        status_code=503, detail="Service unavailable"
    )

    response = client.post(
        "/api/tracks/metadata",
        headers={"X-API-Key": "test_key"},
        json={"track_ids": ["track1"]},
    )
    assert response.status_code == 503
    assert "Service unavailable" in response.json()["detail"]
