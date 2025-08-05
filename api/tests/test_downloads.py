from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_downloads():
    """ Test for GET /downloads """
    response = client.get("/api/downloads")
    assert response.status_code == 200
    response_json = response.json()
    assert "data" in response_json
    assert "meta" in response_json
    assert isinstance(response_json["data"], list)
    assert len(response_json["data"]) == 4

def test_get_downloads_with_limit():
    """ Test for GET /downloads with limit """
    response = client.get("/api/downloads?limit=1")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) == 1

def test_get_downloads_with_offset():
    """ Test for GET /downloads with offset """
    response = client.get("/api/downloads?offset=1")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) == 3

def test_get_downloads_with_status():
    """ Test for GET /downloads with status """
    response = client.get("/api/downloads?status=completed")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["data"]) == 1
    assert response_json["data"][0]["status"] == "completed"

def test_retry_downloads():
    response = client.post("/api/downloads/retry", json={"track_ids": ["track_7", "track_10"]})
    assert response.status_code == 200
    assert response.json()["queued"] is True
