from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_cache():
    resp = client.get("/api/cache")
    assert resp.status_code == 200
    b = resp.json()
    assert isinstance(b["total_items"], int)
    assert 0.0 <= float(b["hit_rate"]) <= 100.0
