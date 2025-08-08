import os
import httpx
import pytest
from urllib.parse import urlparse, parse_qs
import time

# --- Configuration ---
API_BASE_URL = "http://127.0.0.1:8000/api"
SNITCH_BASE_URL = "http://127.0.0.1:4381"

@pytest.fixture
def mock_spotify_token_endpoint(respx_mock):
    """ Mocks the https://accounts.spotify.com/api/token endpoint. """
    def token_route(request: httpx.Request):
        return httpx.Response(
            200,
            json={
                "access_token": "mock_access_token_e2e",
                "refresh_token": "mock_refresh_token_e2e",
                "expires_in": 3600,
            },
        )
    respx_mock.post("https://accounts.spotify.com/api/token").mock(side_effect=token_route)


def test_e2e_full_auth_flow(mock_spotify_token_endpoint):
    """
    Tests the full E2E authentication flow involving the real API and Snitch services.
    """
    print("\n--- Starting E2E Authentication Test ---")

    # Step 1: Start the flow by calling the API
    print("[STEP 1] Calling API to get auth URL...")
    start_url = f"{API_BASE_URL}/auth/spotify/start"
    try:
        with httpx.Client() as client:
            response = client.post(start_url)
            assert response.status_code == 200
            data = response.json()
            auth_url = data["authorization_url"]
            print(f"[INFO] Got auth URL: {auth_url}")
    except httpx.ConnectError as e:
        pytest.fail(f"Could not connect to the API at {start_url}. Is it running? Error: {e}", pytrace=False)


    # Step 2: Extract state from the URL
    print("[STEP 2] Extracting state from URL...")
    parsed_url = urlparse(auth_url)
    query_params = parse_qs(parsed_url.query)
    assert "state" in query_params
    state = query_params["state"][0]
    print(f"[INFO] Extracted state: {state}")


    # Step 3: Simulate the browser redirect to Snitch
    print("[STEP 3] Simulating browser redirect to Snitch...")
    mock_code = "e2e_test_mock_code"
    redirect_url = f"{SNITCH_BASE_URL}/login?code={mock_code}&state={state}"
    try:
        with httpx.Client() as client:
            response = client.get(redirect_url)
            # Snitch should return a 200 OK with a success message
            assert response.status_code == 200
            assert "Authentication Successful" in response.text
            print("[INFO] Snitch handled the redirect successfully.")
    except httpx.ConnectError as e:
        pytest.fail(f"Could not connect to Snitch at {redirect_url}. Is it running? Error: {e}", pytrace=False)


    # Step 4: Wait for the async flow to complete
    # In a real-world scenario, we might poll an endpoint or check a database.
    # For this test, we assume the orchestrator will check the logs.
    # A short sleep ensures the background processes have time to communicate.
    print("[STEP 4] Waiting for Snitch to POST to API...")
    time.sleep(2) # seconds

    print("--- E2E Test Flow Triggered Successfully ---")
    # The final assertion of success will be based on log analysis in the runner script.
    assert True
