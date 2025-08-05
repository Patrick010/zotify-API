from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_stubs():
    response = client.get("/api/stubs")
    assert response.status_code == 200

def test_search_stub():
    response = client.get("/api/stubs/search")
    assert response.status_code == 200

def test_download_stub():
    response = client.post("/api/stubs/download")
    assert response.status_code == 200

def test_download_status_stub():
    response = client.get("/api/stubs/download/status")
    assert response.status_code == 200
