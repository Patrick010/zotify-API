import os
import sys
import pytest
from fastapi.testclient import TestClient
from urllib.parse import urlparse, parse_qs
import httpx

# Add the project root to the path to allow importing the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from zotify_api.main import app
from zotify_api.services import auth_service
from zotify_api.config import settings

client = TestClient(app)

@pytest.fixture
def mock_spotify_token_endpoint(respx_mock):
    """ Mocks the https://accounts.spotify.com/api/token endpoint. """
    def token_route(request: httpx.Request):
        # A real test would validate the incoming form data (code, verifier, etc.)
        return httpx.Response(
            200,
            json={
                "access_token": "mock_access_token",
                "refresh_token": "mock_refresh_token",
                "expires_in": 3600,
                "scope": "user-read-private user-read-email",
            },
        )
    respx_mock.post("https://accounts.spotify.com/api/token").mock(side_effect=token_route)


def test_full_auth_flow(mock_spotify_token_endpoint):
    """
    Tests the full authentication flow from the backend's perspective,
    simulating the role of Snitch.
    """
    # 1. Start the flow and get the authorization URL
    print("[STEP 1] Calling /auth/spotify/start to get authorization URL...")
    response = client.post("/api/auth/spotify/start")
    assert response.status_code == 200
    data = response.json()
    assert "authorization_url" in data
    auth_url = data["authorization_url"]
    print(f"[INFO] Received auth URL: {auth_url}")

    # 2. Extract and verify parameters from the URL
    parsed_url = urlparse(auth_url)
    query_params = parse_qs(parsed_url.query)

    # Check for presence of all required PKCE and OAuth params
    assert "state" in query_params
    assert "client_id" in query_params
    assert "redirect_uri" in query_params
    assert "scope" in query_params
    assert "code_challenge" in query_params
    assert "code_challenge_method" in query_params

    # Verify the values are correct
    assert query_params["client_id"][0] == settings.spotify_client_id
    assert query_params["redirect_uri"][0] == "http://127.0.0.1:4381/login"
    assert query_params["code_challenge_method"][0] == "S256"

    # The full scope string
    expected_scope = (
        "user-read-private user-read-email user-read-playback-state "
        "user-modify-playback-state user-read-currently-playing app-remote-control "
        "playlist-read-private playlist-read-collaborative playlist-modify-public "
        "playlist-modify-private user-library-read user-library-modify "
        "user-top-read user-read-recently-played user-follow-read "
        "user-follow-modify streaming ugc-image-upload"
    )
    assert query_params["scope"][0] == expected_scope

    state = query_params["state"][0]
    print(f"[INFO] Extracted and verified URL parameters. State: {state}")

    # Verify that the state and code_verifier are in our temporary store
    assert state in auth_service.state_store

    # 3. Simulate Snitch receiving the callback and POSTing to our backend
    print("[STEP 2] Simulating Snitch forwarding the callback to /auth/spotify/callback...")
    mock_auth_code = "mock_spotify_auth_code_123"
    callback_payload = {"code": mock_auth_code, "state": state}

    response = client.post("/api/auth/spotify/callback", json=callback_payload)

    # 4. Verify the outcome
    assert response.status_code == 200
    callback_data = response.json()
    print(f"[INFO] Received response from callback endpoint: {callback_data}")
    assert callback_data["status"] == "success"
    assert "token_data" in callback_data
    assert callback_data["token_data"]["access_token"] == "mock_access_token"
    print("[SUCCESS] Auth flow completed successfully.")

    # 5. Verify the state was consumed and removed from the store
    assert state not in auth_service.state_store
    print("[INFO] State correctly removed from store after use.")

def test_callback_with_invalid_state():
    """
    Tests that the callback endpoint rejects a request with an invalid state.
    """
    print("[STEP] Testing callback with an invalid state token...")
    callback_payload = {"code": "some_code", "state": "invalid-state-that-does-not-exist"}
    response = client.post("/api/auth/spotify/callback", json=callback_payload)
    assert response.status_code == 400
    assert "Invalid or expired state" in response.text
    print("[SUCCESS] Correctly rejected invalid state.")
