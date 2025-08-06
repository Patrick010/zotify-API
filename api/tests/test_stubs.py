from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)


def test_download_stub(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.post("/api/download", headers={"X-API-Key": "test_key"})
    assert response.status_code == 501

def test_download_status_stub(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.get("/api/download/status", headers={"X-API-Key": "test_key"})
    assert response.status_code == 501
