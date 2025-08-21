from io import BytesIO
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from zotify_api.main import app

client = TestClient(app)


def test_list_tracks_no_db():
    """Test listing tracks when the database is empty."""
    response = client.get("/api/tracks/")
    assert response.status_code == 200
    assert response.json() == {"data": [], "total": 0}


def test_list_tracks_with_db(test_db_session):
    """Test listing tracks with a populated database."""
    # Add some dummy tracks
    from zotify_api.database import crud, models

    crud.create_track(
        test_db_session,
        models.Track(
            name="Track 1",
            artist="Artist 1",
            album="Album 1",
            spotify_id="spotify_id_1",
            duration_ms=180000,
            cover_url="http://example.com/cover1.jpg",
        ),
    )
    crud.create_track(
        test_db_session,
        models.Track(
            name="Track 2",
            artist="Artist 2",
            album="Album 2",
            spotify_id="spotify_id_2",
            duration_ms=240000,
            cover_url="http://example.com/cover2.jpg",
        ),
    )

    response = client.get("/api/tracks/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["data"]) == 2
    assert data["data"][0]["name"] == "Track 1"


def test_crud_flow_unauthorized():
    """Test that CRUD operations fail without an API key."""
    # Create
    response = client.post(
        "/api/tracks/", json={"name": "test", "artist": "test", "album": "test"}
    )
    assert response.status_code == 401

    # Read
    response = client.get("/api/tracks/123")
    assert response.status_code == 401

    # Update
    response = client.put(
        "/api/tracks/123", json={"name": "updated", "artist": "updated"}
    )
    assert response.status_code == 401

    # Delete
    response = client.delete("/api/tracks/123")
    assert response.status_code == 401


def test_upload_cover_unauthorized():
    """Test that cover upload fails without an API key."""
    file_content = b"test_image_content"
    files = {"file": ("test.jpg", BytesIO(file_content), "image/jpeg")}
    response = client.post("/api/tracks/123/cover", files=files)
    assert response.status_code == 401


@pytest.mark.parametrize(
    "track_id, expected_status", [(1, 200), (999, 404)]  # Existing and non-existing
)
def test_get_metadata(track_id, expected_status, test_db_session, monkeypatch):
    # Setup: Ensure track 1 exists for the success case
    if track_id == 1:
        from zotify_api.database import crud, models

        crud.create_track(
            test_db_session,
            models.Track(
                id=1,
                name="Test Track",
                artist="Test Artist",
                album="Test Album",
                spotify_id="test_id",
            ),
        )

    # Mock the metadata service
    mock_metadata_service = MagicMock()
    mock_metadata_service.get_metadata.return_value = {"spotify": {"id": "test_id"}}
    monkeypatch.setattr(
        "zotify_api.routes.tracks.get_metadata_service",
        lambda: mock_metadata_service,
    )

    response = client.get(
        f"/api/tracks/{track_id}/metadata", headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == expected_status
    if expected_status == 200:
        mock_metadata_service.get_metadata.assert_called_once_with(track_id)
