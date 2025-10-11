# ID: OPS-009
import pytest
import httpx

import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

def get_test_token():
    """Reads the test token from the .gonk_token file."""
    token_path = Path.home() / ".gonk_token"
    if not token_path.exists():
        return None
    return token_path.read_text().strip()

TEST_TOKEN = get_test_token()
auth_skip_condition = pytest.mark.skipif(not TEST_TOKEN, reason="Test token not found. Generate one with 'GonkCLI login'.")


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


@auth_skip_condition
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


@auth_skip_condition
def test_get_user_profile(client):
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    r = client.get("/api/user/profile", headers=headers)
    assert r.status_code == 200
    json_resp = r.json()
    # The user service returns 'email', not 'id', at the top level.
    assert "email" in json_resp


if __name__ == "__main__":
    pytest.main(["-v", __file__])
