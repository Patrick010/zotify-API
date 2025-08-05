from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_system_info():
    """ Test for GET /system """
    response = client.get("/api/system")
    assert response.status_code == 200
    response_json = response.json()
    assert "uptime_seconds" in response_json
    assert "version" in response_json
    assert "env" in response_json
    assert "hostname" in response_json
    assert "python_version" in response_json
