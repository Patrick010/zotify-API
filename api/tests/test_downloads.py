import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.services import downloads_service

client = TestClient(app)

@pytest.fixture
def downloads_service_override():
    download_state = {
        "in_progress": [],
        "failed": {"track_7": "Network error", "track_10": "404 not found"},
        "completed": ["track_3", "track_5"]
    }
    def get_downloads_service_override():
        return downloads_service.DownloadsService(download_state)
    return get_downloads_service_override

def test_download_status(downloads_service_override):
    app.dependency_overrides[downloads_service.get_downloads_service] = downloads_service_override
    response = client.get("/api/downloads/status")
    assert response.status_code == 200
    assert "in_progress" in response.json()["data"]
    assert "failed" in response.json()["data"]
    assert "completed" in response.json()["data"]
    app.dependency_overrides = {}

def test_retry_downloads_unauthorized(downloads_service_override):
    app.dependency_overrides[downloads_service.get_downloads_service] = downloads_service_override
    response = client.post("/api/downloads/retry", json={"track_ids": ["track_7", "track_10"]})
    assert response.status_code == 401
    app.dependency_overrides = {}

def test_retry_downloads(downloads_service_override, monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    app.dependency_overrides[downloads_service.get_downloads_service] = downloads_service_override
    # Get initial state
    initial_status = client.get("/api/downloads/status").json()
    initial_failed_count = len(initial_status["data"]["failed"])
    assert initial_failed_count > 0

    # Retry failed downloads
    response = client.post("/api/downloads/retry", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track_7", "track_10"]})
    assert response.status_code == 200
    assert response.json()["data"]["queued"] is True

    # Verify that the failed queue is now empty
    final_status = client.get("/api/downloads/status").json()
    assert len(final_status["data"]["failed"]) == 0
    assert "track_7" in final_status["data"]["in_progress"]
    assert "track_10" in final_status["data"]["in_progress"]
    app.dependency_overrides = {}
