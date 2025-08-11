import pytest
import os
from fastapi.testclient import TestClient
from zotify_api.main import app
import zotify_api.services.downloads_db as downloads_db
from zotify_api.services.download_service import get_downloads_service, downloads_service_instance

client = TestClient(app)

@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """
    Fixture to set up a temporary, isolated database for each test.
    This prevents tests from interfering with each other.
    """
    # Create a temporary database file
    temp_db_path = tmp_path / "test_downloads.db"

    # Use monkeypatch to make the download_db module use the temporary file
    monkeypatch.setattr(downloads_db, "DB_FILE", str(temp_db_path))

    # Initialize the database schema in the temporary database
    downloads_db.init_db()

    yield temp_db_path

    # Cleanup is handled by tmp_path fixture, but we can be explicit if needed
    if os.path.exists(temp_db_path):
        os.remove(temp_db_path)

@pytest.fixture
def fresh_downloads_service(test_db, monkeypatch):
    """
    Ensures each test uses the isolated test database and has a dummy admin key.
    The `test_db` fixture dependency ensures the DB is set up before the service is used.
    """
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    # The service instance is a singleton, so we just return it.
    # The test_db fixture ensures it's operating on a clean DB.
    yield downloads_service_instance
    # No need to reset the singleton, as each test gets its own DB.


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

def test_retry_failed_jobs_and_process(fresh_downloads_service, monkeypatch):
    """
    Tests that a failed job can be retried and then successfully processed.
    This confirms the fix to re-queue retried jobs.
    """
    # Add a job
    client.post("/api/download", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track_to_fail"]})

    # Force it to fail
    original_method = downloads_service_instance.process_download_queue
    def mock_process_fail(*args, **kwargs):
        return original_method(force_fail=True)
    monkeypatch.setattr(downloads_service_instance, "process_download_queue", mock_process_fail)
    client.post("/api/download/process", headers={"X-API-Key": "test_key"})

    # Restore original method
    monkeypatch.undo()

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
    assert processed_job["track_id"] == "track_to_fail"
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
    original_method = downloads_service_instance.process_download_queue
    def mock_process_fail(*args, **kwargs):
        return original_method(force_fail=True)
    monkeypatch.setattr(downloads_service_instance, "process_download_queue", mock_process_fail)

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
