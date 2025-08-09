import json
import logging
from pathlib import Path

# This module holds the shared state and constants for the authentication process.

logger = logging.getLogger(__name__)

# --- Constants ---
# In a production app, these should be loaded from a secure config (e.g., env vars)
CLIENT_ID = "65b708073fc0480ea92a077233ca87bd"
CLIENT_SECRET = "832bc60deeb147db86dd1cc521d9e4bf"
REDIRECT_URI = "http://127.0.0.1:4381/login"  # Must match Snitch listener URL
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


# --- File-based Token Storage (Temporary) ---

# Define the path for the temporary token storage file
STORAGE_DIR = Path(__file__).parent.parent / "storage"
TOKEN_FILE = STORAGE_DIR / "spotify_tokens.json"

def load_tokens():
    """Loads tokens from the JSON file if it exists."""
    if TOKEN_FILE.exists():
        logger.info(f"Loading tokens from {TOKEN_FILE}")
        with open(TOKEN_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logger.warning("Could not decode token file, starting fresh.")
                return {}
    return {}

def save_tokens(tokens):
    """Saves the given tokens dictionary to the JSON file."""
    STORAGE_DIR.mkdir(exist_ok=True)
    logger.info(f"Saving tokens to {TOKEN_FILE}")
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f, indent=4)

# Initialize the token store from the file.
# In a production environment, this should be replaced with a robust,
# persistent, and concurrency-safe storage solution like Redis or a database.
spotify_tokens = load_tokens()
if not spotify_tokens:
    spotify_tokens.update({
        "access_token": None,
        "refresh_token": None,
        "expires_at": 0
    })


# --- PKCE State Management (Ephemeral) ---

# Stores the PKCE code_verifier, indexed by the `state` parameter.
pending_states = {}  # state -> code_verifier mapping
