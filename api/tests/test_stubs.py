from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)


def test_download_stub():
    response = client.post("/api/download")
    assert response.status_code == 501

def test_download_status_stub():
    response = client.get("/api/download/status")
    assert response.status_code == 501
