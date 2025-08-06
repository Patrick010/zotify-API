from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.routes.downloads import download_state

client = TestClient(app)

def test_download_status():
    response = client.get("/api/downloads/status")
    assert response.status_code == 200
    assert "in_progress" in response.json()
    assert "failed" in response.json()
    assert "completed" in response.json()

def test_retry_downloads():
    # Get initial state
    initial_failed_count = len(download_state["failed"])
    assert initial_failed_count > 0

    # Retry failed downloads
    response = client.post("/api/downloads/retry", json={"track_ids": ["track_7", "track_10"]})
    assert response.status_code == 200
    assert response.json()["queued"] is True

    # Verify that the failed queue is now empty
    final_status = client.get("/api/downloads/status").json()
    assert len(final_status["failed"]) == 0
    assert "track_7" in final_status["in_progress"]
    assert "track_10" in final_status["in_progress"]
