import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.services.download_service import get_downloads_service, DownloadsService

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
    response = client.get("/api/download/status")
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
    response = client.get("/api/download/status")
    assert response.status_code == 200
    data = response.json()
    assert data["total_jobs"] == 2
    assert data["pending"] == 2
    assert data["completed"] == 0

def test_retry_failed_jobs_and_process(fresh_downloads_service):
    """
    Tests that a failed job can be retried and then successfully processed.
    This confirms the fix to re-queue retried jobs.
    """
    # Manually set a job to failed for testing
    service = fresh_downloads_service
    job = service.add_downloads_to_queue(["failed_track"])[0]
    job.status = "failed"

    # Check status before retry
    response = client.get("/api/download/status")
    data = response.json()
    assert data["total_jobs"] == 1
    assert data["failed"] == 1
    assert data["pending"] == 0

    # Retry failed jobs
    response = client.post("/api/download/retry")
    assert response.status_code == 200
    data = response.json()
    assert data["total_jobs"] == 1
    assert data["failed"] == 0
    assert data["pending"] == 1
    assert data["jobs"][0]["status"] == "pending"

    # Now, process the re-queued job
    response = client.post("/api/download/process", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    processed_job = response.json()
    assert processed_job["track_id"] == "failed_track"
    assert processed_job["status"] == "completed"

    # Final status check
    response = client.get("/api/download/status")
    data = response.json()
    assert data["total_jobs"] == 1
    assert data["pending"] == 0
    assert data["completed"] == 1


def test_auth_logic(fresh_downloads_service):
    # status and retry should be public (no key needed)
    response = client.get("/api/download/status")
    assert response.status_code == 200

    response = client.post("/api/download/retry")
    assert response.status_code == 200

    # posting a new download should require auth
    response = client.post("/api/download", json={"track_ids": ["track1"]})
    assert response.status_code == 401

    # ...and should succeed with auth
    response = client.post("/api/download", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track1"]})
    assert response.status_code == 200


def test_process_job_success(fresh_downloads_service):
    client.post("/api/download", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track_success"]})

    response = client.post("/api/download/process", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    job = response.json()
    assert job["track_id"] == "track_success"
    assert job["status"] == "completed"
    assert job["progress"] == 1.0

    response = client.get("/api/download/status")
    data = response.json()
    assert data["total_jobs"] == 1
    assert data["pending"] == 0
    assert data["completed"] == 1


def test_process_job_failure(fresh_downloads_service, monkeypatch):
    client.post("/api/download", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track_fail"]})

    # Patch the service method to force a failure
    service = fresh_downloads_service
    original_method = service.process_download_queue
    def mock_process_fail(*args, **kwargs):
        return original_method(force_fail=True)
    monkeypatch.setattr(service, "process_download_queue", mock_process_fail)

    response = client.post("/api/download/process", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    job = response.json()
    assert job["track_id"] == "track_fail"
    assert job["status"] == "failed"
    assert job["error_message"] == "Forced failure for testing."

    response = client.get("/api/download/status")
    data = response.json()
    assert data["total_jobs"] == 1
    assert data["pending"] == 0
    assert data["failed"] == 1


def test_process_empty_queue(fresh_downloads_service):
    response = client.post("/api/download/process", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json() is None


def test_process_auth(fresh_downloads_service):
    response = client.post("/api/download/process")
    assert response.status_code == 401

    response = client.post("/api/download/process", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
