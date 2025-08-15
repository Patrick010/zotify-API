import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from zotify_api.main import app
from zotify_api.database.session import get_db, Base
from zotify_api.services import download_service

# --- Test Database Setup ---

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture()
def db_session():
    """
    Fixture to provide a clean, isolated database session for each test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(autouse=True)
def override_get_db(db_session):
    """
    Fixture to override the `get_db` dependency with the isolated test session.
    `autouse=True` ensures this runs for every test.
    """
    def override_db():
        yield db_session

    app.dependency_overrides[get_db] = override_db
    yield
    del app.dependency_overrides[get_db]

client = TestClient(app)

# --- Tests ---

def test_get_initial_queue_status():
    response = client.get("/api/download/status")
    assert response.status_code == 200
    data = response.json()
    assert data["total_jobs"] == 0
    assert data["pending"] == 0
    assert data["completed"] == 0
    assert data["failed"] == 0
    assert data["jobs"] == []

def test_add_new_downloads():
    response = client.post("/api/download", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track1", "track2"]})
    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) == 2
    assert jobs[0]["track_id"] == "track1"
    assert jobs[1]["track_id"] == "track2"
    assert jobs[0]["status"] == "pending"

    response = client.get("/api/download/status")
    assert response.status_code == 200
    data = response.json()
    assert data["total_jobs"] == 2
    assert data["pending"] == 2

def test_process_job_success():
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
    assert data["completed"] == 1

def test_process_job_failure(monkeypatch):
    client.post("/api/download", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track_fail"]})

    # Force a failure
    original_method = download_service.process_download_queue
    def mock_process_fail(*args, **kwargs):
        return original_method(*args, **kwargs, force_fail=True)
    monkeypatch.setattr(download_service, "process_download_queue", mock_process_fail)

    response = client.post("/api/download/process", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    job = response.json()
    assert job["track_id"] == "track_fail"
    assert job["status"] == "failed"
    assert "Forced failure" in job["error_message"]

    response = client.get("/api/download/status")
    data = response.json()
    assert data["total_jobs"] == 1
    assert data["failed"] == 1

def test_retry_failed_jobs(monkeypatch):
    # Add and fail a job
    client.post("/api/download", headers={"X-API-Key": "test_key"}, json={"track_ids": ["track_to_retry"]})
    original_method = download_service.process_download_queue
    def mock_process_fail(*args, **kwargs):
        return original_method(*args, **kwargs, force_fail=True)
    monkeypatch.setattr(download_service, "process_download_queue", mock_process_fail)
    client.post("/api/download/process", headers={"X-API-Key": "test_key"})

    # Check it failed
    response = client.get("/api/download/status")
    assert response.json()["failed"] == 1
    assert response.json()["pending"] == 0

    # Retry
    response = client.post("/api/download/retry")
    assert response.status_code == 200
    data = response.json()
    assert data["total_jobs"] == 1
    assert data["failed"] == 0
    assert data["pending"] == 1
    assert data["jobs"][0]["status"] == "pending"

def test_process_empty_queue():
    response = client.post("/api/download/process", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json() is None
