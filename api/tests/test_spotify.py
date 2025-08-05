from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_spotify_search():
    resp = client.get("/api/spotify/search?q=abba&type=track&limit=2")
    assert resp.status_code == 200
    b = resp.json()
    assert "data" in b and isinstance(b["data"], list)
    assert all("id" in i and "name" in i for i in b["data"])
