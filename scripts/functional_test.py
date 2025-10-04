import pytest
import httpx

BASE_URL = "http://localhost:8000"
TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTc1OTYwMzU4NH0.u8Bf9jls8JqbOB9IVve67vPAONHhLtkramhe1cYSApI"


@pytest.fixture
def client():
    # allow_redirects=True will handle the 307 from FastAPI
    with httpx.Client(base_url=BASE_URL, follow_redirects=True) as client:
        yield client


def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    json_resp = r.json()
    assert json_resp.get("status") == "ok"


def test_get_playlists(client):
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    r = client.get("/api/playlists/", headers=headers)
    assert r.status_code == 200
    json_resp = r.json()
    assert "data" in json_resp
    assert isinstance(json_resp["data"], list)


def test_error_handling(client):
    r = client.get("/api/nonexistent/endpoint")
    assert r.status_code == 404
    json_resp = r.json()
    assert "detail" in json_resp


def test_get_user_profile(client):
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    r = client.get("/api/user/profile", headers=headers)
    assert r.status_code == 200
    json_resp = r.json()
    # The user service returns 'email', not 'id', at the top level.
    assert "email" in json_resp


if __name__ == "__main__":
    pytest.main(["-v", __file__])
