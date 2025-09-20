import pytest
import requests_mock
import json
from GonkCLI.modules.jwt_mock import JWTClient

API_BASE_URL = "http://localhost:8000"

@pytest.fixture
def client():
    return JWTClient(api_base_url=API_BASE_URL)

def test_login(client: JWTClient, requests_mock):
    # Mock the login endpoint
    requests_mock.post(f"{API_BASE_URL}/api/auth/login", json={"access_token": "test_token", "token_type": "bearer"})

    token = client.login("testuser", "password")
    assert token == "test_token"
    assert client.token == "test_token"

def test_get_profile(client: JWTClient, requests_mock):
    client.token = "test_token"
    # Mock the profile endpoint
    requests_mock.get(f"{API_BASE_URL}/api/user/profile", json={"name": "testuser", "email": "test@test.com"})

    profile = client.get_profile()
    assert profile["name"] == "testuser"

    # Check that the auth header was sent
    assert requests_mock.last_request.headers["Authorization"] == "Bearer test_token"

def test_update_preferences(client: JWTClient, requests_mock):
    client.token = "test_token"
    # Mock the preferences endpoint
    requests_mock.patch(f"{API_BASE_URL}/api/user/preferences", json={"theme": "light", "language": "fr", "notifications_enabled": False})

    prefs = client.update_preferences(theme="light", notifications_enabled=False)
    assert prefs["theme"] == "light"
    assert prefs["notifications_enabled"] is False

    # Check that the auth header and payload were sent correctly
    assert requests_mock.last_request.headers["Authorization"] == "Bearer test_token"
    assert requests_mock.last_request.json() == {"theme": "light", "notifications_enabled": False}

def test_get_liked_tracks(client: JWTClient, requests_mock):
    client.token = "test_token"
    requests_mock.get(f"{API_BASE_URL}/api/user/liked", json=["track1", "track2"])

    liked = client.get_liked_tracks()
    assert liked == ["track1", "track2"]

def test_get_history(client: JWTClient, requests_mock):
    client.token = "test_token"
    requests_mock.get(f"{API_BASE_URL}/api/user/history", json=["track3", "track4"])

    history = client.get_history()
    assert history == ["track3", "track4"]

def test_clear_history(client: JWTClient, requests_mock):
    client.token = "test_token"
    requests_mock.delete(f"{API_BASE_URL}/api/user/history", status_code=204)

    success = client.clear_history()
    assert success is True
