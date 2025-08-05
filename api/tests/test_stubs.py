from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_stubs():
    response = client.get("/api/stubs")
    assert response.status_code == 200

