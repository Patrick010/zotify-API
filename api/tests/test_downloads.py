import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.services.downloads_service import get_downloads_service, DownloadsService

client = TestClient(app)

@pytest.fixture
def fresh_downloads_service(monkeypatch):
    """ Ensures each test gets a fresh service instance and a dummy admin key. """
    service = DownloadsService()
    app.dependency_overrides[get_downloads_service] = lambda: service
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    yield service
    app.dependency_overrides = {}

def test_get_initial_queue_status(fresh_downloads_service):
    response = client.get("/api/downloads/status", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_jobs"] == 0
    assert data["pending"] == 0
    assert data["completed"] == 0
    assert data["failed"] == 0
    assert data["jobs"] == []

def test_add_new_downloads(fresh_downloads_service):
    # Add two tracks to the queue
    response = client.post("/api/download", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track1", "track2"]})
    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) == 2
    assert jobs[0]["track_id"] == "track1"
    assert jobs[1]["track_id"] == "track2"
    assert jobs[0]["status"] == "pending"

    # Check the queue status
    response = client.get("/api/downloads/status", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_jobs"] == 2
    assert data["pending"] == 2
    assert data["completed"] == 0

def test_retry_failed_jobs(fresh_downloads_service):
    # Manually set a job to failed for testing
    service = fresh_downloads_service
    job = service.add_downloads_to_queue(["failed_track"])[0]
    job.status = "failed"

    # Check status before retry
    response = client.get("/api/downloads/status", headers={"X-API-Key": "test_key"})
    data = response.json()
    assert data["total_jobs"] == 1
    assert data["failed"] == 1
    assert data["pending"] == 0

    # Retry failed jobs
    response = client.post("/api/downloads/retry", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_jobs"] == 1
    assert data["failed"] == 0
    assert data["pending"] == 1
    assert data["jobs"][0]["status"] == "pending"

def test_unauthorized_access(fresh_downloads_service):
    response = client.get("/api/downloads/status")
    assert response.status_code == 401 # or 403 depending on implementation

    response = client.post("/api/download", json={"track_ids": ["track1"]})
    assert response.status_code == 401

    response = client.post("/api/downloads/retry")
    assert response.status_code == 401
