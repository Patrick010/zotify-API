import logging
import time
import httpx
from fastapi import APIRouter, HTTPException, Request
from zotify_api.auth_state import (
    spotify_tokens, pending_states, save_tokens,
    CLIENT_ID, REDIRECT_URI, SPOTIFY_TOKEN_URL, CLIENT_SECRET, SPOTIFY_API_BASE
)
from zotify_api.schemas.auth import AuthStatus, RefreshResponse, SpotifyCallbackPayload, CallbackResponse
from zotify_api.services.auth import require_admin_api_key, refresh_spotify_token, get_auth_status, handle_spotify_callback
from fastapi import Depends


router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

@router.post("/spotify/callback", response_model=CallbackResponse)
async def spotify_callback(payload: SpotifyCallbackPayload):
    """
    Handles the secure callback from the Snitch service after user authentication.
    """
    await handle_spotify_callback(code=payload.code, state=payload.state)
    return {"status": "success"}

@router.get("/status", response_model=AuthStatus, dependencies=[Depends(require_admin_api_key)])
async def get_status():
    """ Returns the current authentication status """
    return await get_auth_status()

@router.post("/logout", status_code=204, dependencies=[Depends(require_admin_api_key)])
def logout():
    """
    Clears stored Spotify credentials.

    Note: Spotify does not provide an API endpoint to invalidate access tokens.
    This function clears the tokens from local storage, effectively logging the user out
    from this application's perspective.
    """
    spotify_tokens.update({
        "access_token": None,
        "refresh_token": None,
        "expires_at": 0,
    })
    save_tokens(spotify_tokens)
    return {}

@router.get("/refresh", response_model=RefreshResponse, dependencies=[Depends(require_admin_api_key)])
async def refresh():
    """ Refreshes the Spotify access token """
    new_expires_at = await refresh_spotify_token()
    return RefreshResponse(expires_at=new_expires_at)
