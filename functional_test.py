import pytest
import httpx

BASE_URL = "http://localhost:8000/api"  # Adjust if your host/port differ
TEST_TOKEN = "test_key"  # Replace with a valid token or mock token


@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client


def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    # Basic check for a field in response, adjust as per your API's actual health response
    json_resp = r.json()
    assert "status" in json_resp or "uptime" in json_resp


def test_oauth_spotify_integration(client):
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    r = client.get("/spotify/playlists", headers=headers)
    assert r.status_code == 200
    # Basic structure validation
    json_resp = r.json()
    assert isinstance(json_resp, dict) or isinstance(json_resp, list)


def test_error_handling(client):
    r = client.get("/nonexistent/endpoint")
    assert r.status_code == 404
    json_resp = r.json()
    assert "detail" in json_resp


def test_user_profile(client):
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    r = client.get("/users/me", headers=headers)
    assert r.status_code == 200
    json_resp = r.json()
    assert "id" in json_resp or "username" in json_resp


if __name__ == "__main__":
    pytest.main(["-v", __file__])
