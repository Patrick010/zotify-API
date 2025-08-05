from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_user_info():
    """ Test for GET /user """
    response = client.get("/api/user")
    assert response.status_code == 200
    response_json = response.json()
    assert "username" in response_json
    assert "email" in response_json

def test_get_user_profile_stub():
    response = client.get("/api/user/profile")
    assert response.status_code == 200

def test_get_user_liked_stub():
    response = client.get("/api/user/liked")
    assert response.status_code == 200

def test_sync_user_liked_stub():
    response = client.post("/api/user/sync_liked")
    assert response.status_code == 200

def test_get_user_history_stub():
    response = client.get("/api/user/history")
    assert response.status_code == 200

def test_delete_user_history_stub():
    response = client.delete("/api/user/history")
    assert response.status_code == 200
