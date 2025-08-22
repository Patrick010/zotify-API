import os
import sys
import time
import secrets
import string
import webbrowser
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
REDIRECT_URI = "http://127.0.0.1:4381/login"
AUTH_ENDPOINT = "https://accounts.spotify.com/authorize"
CALLBACK_POLL_URL = f"{API_BASE_URL}/login"  # Adjust if needed


def check_api():
    try:
        r = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if r.status_code == 200:
            print(f"[INFO] API reachable at {API_BASE_URL}")
            return True
    except requests.RequestException:
        pass  # The error is logged below
    print(f"[ERROR] Cannot reach API at {API_BASE_URL}")
    return False


def generate_state(length=32):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def build_auth_url(client_id, redirect_uri, state, scope="user-read-email"):
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": scope,
        "show_dialog": "true",
    }
    from urllib.parse import urlencode

    return f"{AUTH_ENDPOINT}?{urlencode(params)}"


def poll_callback(state, timeout=180, interval=3):
    print(f"[WAITING] Polling for callback for up to {timeout} seconds...")
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            resp = requests.get(CALLBACK_POLL_URL, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("state") == state and "code" in data:
                    print("[INFO] Received callback data:")
                    print(f"       Code: {data['code']}")
                    print(f"       State: {data['state']}")
                    return True
        except requests.RequestException:
            pass
        time.sleep(interval)
    print("[ERROR] Timeout waiting for callback.")
    return False


def main():
    if not SPOTIFY_CLIENT_ID:
        print("[ERROR] SPOTIFY_CLIENT_ID environment variable is not set.")
        sys.exit(1)
    if not check_api():
        sys.exit(1)

    state = generate_state()
    auth_url = build_auth_url(SPOTIFY_CLIENT_ID, REDIRECT_URI, state)

    print(
        "\n[STEP] Open this URL in your Windows browser to start Spotify auth flow:\n"
    )
    print(auth_url + "\n")

    print("[STEP] Then manually run 'snitch_debug.exe' on your Windows machine.")
    print(f"        It must listen on {REDIRECT_URI} to capture the callback.\n")

    try:
        webbrowser.open(auth_url)
    except Exception:
        print("[WARN] Could not open browser automatically. Open URL manually.")

    success = poll_callback(state)
    if success:
        print("[SUCCESS] Auth flow completed.")
    else:
        print("[FAILURE] Auth flow did not complete successfully.")


if __name__ == "__main__":
    main()
