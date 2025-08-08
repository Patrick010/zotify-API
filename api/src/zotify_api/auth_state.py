import json
import logging
from pathlib import Path

# This module holds the shared, in-memory state for the authentication process.

logger = logging.getLogger(__name__)

# Define the path for the temporary token storage file
STORAGE_DIR = Path(__file__).parent.parent / "storage"
TOKEN_FILE = STORAGE_DIR / "spotify_tokens.json"

# --- Token Management ---

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


# --- PKCE State Management ---

# Stores the PKCE code_verifier, indexed by the `state` parameter.
# This is used to verify the callback request. This store is ephemeral and
# does not need to be persisted.
pending_states = {}  # state -> code_verifier mapping
