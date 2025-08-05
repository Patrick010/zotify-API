from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_cache_integration(monkeypatch):
    monkeypatch.setattr("zotify_api.routes.cache.get_cache_stats", lambda: {
        "total_items": 12, "memory_usage_mb": 10.5, "hit_rate": 95.0, "last_cleared": "2025-08-01T00:00:00Z"
    })
    r = client.get("/api/cache")
    assert r.status_code == 200
    body = r.json()
    assert body["total_items"] == 12
