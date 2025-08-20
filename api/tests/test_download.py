import pytest

from zotify_api.database.session import get_db
from zotify_api.main import app
from zotify_api.services import download_service

# The custom, module-level database setup has been removed.
# This test file will now use the fixtures defined in conftest.py,
# which is the standard for this project.

@pytest.fixture(autouse=True)
def override_get_db(test_db_session):
    """
    Fixture to override the `get_db` dependency with the isolated test session
    provided by the `test_db_session` fixture from conftest.py.
    `autouse=True` ensures this runs for every test in this file.
    """
    def override_db():
        yield test_db_session

    app.dependency_overrides[get_db] = override_db
    yield
    # The override is cleared by the main client fixture in conftest.py,
    # but cleaning it here too doesn't hurt.
    app.dependency_overrides.clear()


# The client is now provided by the `client` fixture from conftest.py.
# We just need to ask for it as an argument in the test functions.

# --- Tests ---

def test_get_initial_queue_status(client):
    response = client.get("/api/downloads/status")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_jobs"] == 0
    assert data["pending"] == 0
    assert data["completed"] == 0
    assert data["failed"] == 0
    assert data["jobs"] == []

def test_add_new_downloads(client):
    response = client.post("/api/downloads", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track1", "track2"]})
    assert response.status_code == 200
    jobs = response.json()["data"]
    assert len(jobs) == 2
    assert jobs[0]["track_id"] == "track1"
    assert jobs[1]["track_id"] == "track2"
    assert jobs[0]["status"] == "pending"

    response = client.get("/api/downloads/status")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_jobs"] == 2
    assert data["pending"] == 2

def test_process_job_success(client):
    client.post("/api/downloads", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track_success"]})
    response = client.post("/api/downloads/process", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    job = response.json()["data"]
    assert job["track_id"] == "track_success"
    assert job["status"] == "completed"
    assert job["progress"] == 1.0

    response = client.get("/api/downloads/status")
    data = response.json()["data"]
    assert data["total_jobs"] == 1
    assert data["completed"] == 1

def test_process_job_failure(client, monkeypatch):
    client.post("/api/downloads", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track_fail"]})

    # Force a failure
    original_method = download_service.process_download_queue
    def mock_process_fail(*args, **kwargs):
        return original_method(*args, **kwargs, force_fail=True)
    monkeypatch.setattr(download_service, "process_download_queue", mock_process_fail)

    response = client.post("/api/downloads/process", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    job = response.json()["data"]
    assert job["track_id"] == "track_fail"
    assert job["status"] == "failed"
    assert "Forced failure" in job["error_message"]

    response = client.get("/api/downloads/status")
    data = response.json()["data"]
    assert data["total_jobs"] == 1
    assert data["failed"] == 1

def test_retry_failed_jobs(client, monkeypatch):
    # Add and fail a job
    client.post("/api/downloads", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track_to_retry"]})
    original_method = download_service.process_download_queue
    def mock_process_fail(*args, **kwargs):
        return original_method(*args, **kwargs, force_fail=True)
    monkeypatch.setattr(download_service, "process_download_queue", mock_process_fail)
    client.post("/api/downloads/process", headers={"X-API-Key": "test_key"})

    # Check it failed
    response = client.get("/api/downloads/status")
    assert response.json()["data"]["failed"] == 1
    assert response.json()["data"]["pending"] == 0

    # Retry
    response = client.post("/api/downloads/retry")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_jobs"] == 1
    assert data["failed"] == 0
    assert data["pending"] == 1
    assert data["jobs"][0]["status"] == "pending"

def test_process_empty_queue(client):
    response = client.post("/api/downloads/process", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json()["data"] is None
