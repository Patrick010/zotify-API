from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_logging_filter(monkeypatch):
    def fake_read(limit, level):
        if level == "ERROR":
            return [{"timestamp":"2025-08-01T00:00:00Z","level":"ERROR","message":"err"}]
        return []
    monkeypatch.setattr("zotify_api.routes.logging.read_recent_logs", fake_read)
    r = client.get("/api/logging?level=ERROR")
    assert r.status_code == 200
    data = r.json()["data"]
    assert data and data[0]["level"] == "ERROR"
