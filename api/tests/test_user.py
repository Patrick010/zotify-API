from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

import uuid

def test_get_user_info():
    """ Test for GET /user """
    response = client.get("/api/user", headers={"X-Test-User": str(uuid.uuid4())})
    assert response.status_code == 200
    response_json = response.json()
    assert "username" in response_json
    assert "email" in response_json
