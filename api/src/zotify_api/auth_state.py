import logging

# This module holds the shared constants for the authentication process.
# The state management (tokens, PKCE state) is now handled by the
# database layer and the respective API routes.

logger = logging.getLogger(__name__)

# --- Constants ---
# In a production app, these should be loaded from a secure config (e.g., env vars)
CLIENT_ID = "65b708073fc0480ea92a077233ca87bd"
CLIENT_SECRET = "832bc60deeb147db86dd1cc521d9e4bf"
REDIRECT_URI = "http://127.0.0.1:4381/login"  # Must match Snitch listener URL
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


# --- PKCE State Management (Ephemeral) ---
# This is kept in memory as it's only needed for the duration of a single
# OAuth2 login flow. A more robust solution for a multi-replica setup
# might use a shared cache like Redis.
pending_states = {}  # state -> code_verifier mapping
