from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_sync():
    resp = client.get("/api/sync")
    assert resp.status_code == 200
    for job in resp.json()["data"]:
        assert job["status"] in ("pending","running","completed","failed")
