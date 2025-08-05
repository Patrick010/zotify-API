from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_logging():
    resp = client.get("/api/logging")
    assert resp.status_code == 200
    for e in resp.json()["data"]:
        assert e["level"] in ("DEBUG","INFO","WARNING","ERROR")
