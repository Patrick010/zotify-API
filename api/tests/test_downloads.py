from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_downloads():
    resp = client.get("/api/downloads")
    assert resp.status_code == 200
    body = resp.json()
    assert "data" in body and "meta" in body
    assert isinstance(body["data"], list)
    for item in body["data"]:
        assert "id" in item and "filename" in item and "status" in item
        assert 0.0 <= item["progress"] <= 100.0
