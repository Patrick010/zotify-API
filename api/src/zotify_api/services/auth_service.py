import logging
import secrets
import string
import httpx
from pkce import get_code_challenge, generate_code_verifier

log = logging.getLogger(__name__)

# This is a temporary, in-memory store. In a real application, this MUST be
# replaced with a secure, persistent, and concurrency-safe store (e.g., Redis, DB).
state_store = {}

# Constants - In a real app, these would come from config
CLIENT_ID = "65b708073fc0480ea92a077233ca87bd" # Example client ID from prompt
REDIRECT_URI = "http://127.0.0.1:4381/login"
SCOPES = "user-read-private user-read-email" # Example scopes

def generate_secure_token(length=32):
    """Generates a URL-safe random token."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def start_pkce_flow():
    """
    Generates state and PKCE codes for the Spotify OAuth flow.
    """
    state = generate_secure_token()
    code_verifier = generate_code_verifier(length=128)
    code_challenge = get_code_challenge(code_verifier)

    # Store the verifier for the callback
    state_store[state] = code_verifier
    log.info(f"Generated state and stored code_verifier for state: {state}")

    # Construct the authorization URL
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
        "state": state,
        "scope": SCOPES,
    }

    import urllib.parse
    full_auth_url = f"{auth_url}?{urllib.parse.urlencode(params)}"

    return {"authorization_url": full_auth_url}


async def exchange_code_for_token(code: str, state: str):
    """
    Exchanges the authorization code for an access token using PKCE.
    """
    log.info(f"Attempting to exchange code for state: {state}")
    code_verifier = state_store.pop(state, None)

    if not code_verifier:
        log.warning(f"Invalid or expired state received: {state}")
        return {"error": "Invalid or expired state token."}

    token_url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "code_verifier": code_verifier,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data, headers=headers)

    if response.status_code != 200:
        log.error(f"Failed to exchange token. Spotify responded with {response.status_code}: {response.text}")
        return {"error": "Failed to exchange authorization code for a token."}

    token_data = response.json()
    log.info("Successfully exchanged code for token.")

    # In a real app, you would securely store the access_token, refresh_token, etc.
    # For now, we just return them.
    return {"status": "success", "token_data": token_data}
