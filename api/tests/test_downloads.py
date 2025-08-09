import pytest
from zotify_api.main import app
from zotify_api.services import downloads_service

@pytest.fixture
def downloads_service_override():
    """Fixture to override the downloads service with a predictable state."""
    download_state = {
        "in_progress": [],
        "failed": {"track_7": "Network error", "track_10": "404 not found"},
        "completed": ["track_3", "track_5"]
    }
    def get_downloads_service_override():
        return downloads_service.DownloadsService(download_state)

    original_override = app.dependency_overrides.get(downloads_service.get_downloads_service)
    app.dependency_overrides[downloads_service.get_downloads_service] = get_downloads_service_override
    yield
    app.dependency_overrides[downloads_service.get_downloads_service] = original_override


def test_download_status(client, downloads_service_override):
    response = client.get("/api/downloads/status")
    assert response.status_code == 200
    assert "in_progress" in response.json()["data"]
    assert "failed" in response.json()["data"]
    assert "completed" in response.json()["data"]

def test_retry_downloads_unauthorized(client, downloads_service_override):
    response = client.post("/api/downloads/retry", json={"track_ids": ["track_7", "track_10"]})
    assert response.status_code == 401

def test_retry_downloads(client, downloads_service_override):
    # Get initial state
    initial_status = client.get("/api/downloads/status").json()
    initial_failed_count = len(initial_status["data"]["failed"])
    assert initial_failed_count > 0

    # Retry failed downloads
    response = client.post(
        "/api/downloads/retry",
        headers={"X-API-Key": "test_key"},
        json={"track_ids": ["track_7", "track_10"]}
    )
    assert response.status_code == 200
    assert response.json()["data"]["queued"] is True

    # Verify that the failed queue is now empty
    final_status = client.get("/api/downloads/status").json()
    assert len(final_status["data"]["failed"]) == 0
    assert "track_7" in final_status["data"]["in_progress"]
    assert "track_10" in final_status["data"]["in_progress"]
