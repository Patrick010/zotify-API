import logging
import time
import httpx
from fastapi import APIRouter, HTTPException, Request
from zotify_api.auth_state import (
    spotify_tokens, pending_states, save_tokens,
    CLIENT_ID, REDIRECT_URI, SPOTIFY_TOKEN_URL, CLIENT_SECRET, SPOTIFY_API_BASE
)
from zotify_api.schemas.auth import AuthStatus, RefreshResponse, SpotifyCallbackPayload, CallbackResponse
from zotify_api.services.auth import require_admin_api_key
from fastapi import Depends


router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

@router.post("/spotify/callback", response_model=CallbackResponse)
async def spotify_callback(payload: SpotifyCallbackPayload):
    """
    Handles the secure callback from the Snitch service after user authentication.
    """
    logger.info(f"POST /auth/spotify/callback received for state: {payload.state}")

    # 1. Validate state and retrieve PKCE code verifier
    code_verifier = pending_states.pop(payload.state, None)
    if not code_verifier:
        logger.warning(f"Invalid or expired state received in callback: {payload.state}")
        raise HTTPException(status_code=400, detail="Invalid or expired state token.")

    # 2. Exchange authorization code for tokens
    data = {
        "grant_type": "authorization_code",
        "code": payload.code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "code_verifier": code_verifier,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
            resp.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            tokens = resp.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to exchange token. Spotify responded with {e.response.status_code}: {e.response.text}")
            raise HTTPException(status_code=400, detail=f"Failed to exchange code for token: {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Failed to connect to Spotify token endpoint: {e}")
            raise HTTPException(status_code=503, detail="Service unavailable: Could not connect to Spotify.")

    # 3. Store tokens
    spotify_tokens.update({
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"), # Refresh token is optional
        "expires_at": time.time() + tokens["expires_in"] - 60,
    })
    save_tokens(spotify_tokens)
    logger.info("Successfully exchanged code for token and stored them.")

    # 4. Respond with minimal success message
    return {"status": "success"}

@router.get("/status", response_model=AuthStatus, dependencies=[Depends(require_admin_api_key)])
async def get_status():
    """ Returns the current authentication status """
    if not spotify_tokens.get("access_token"):
        return AuthStatus(authenticated=False, token_valid=False, expires_in=0)

    headers = {"Authorization": f"Bearer {spotify_tokens['access_token']}"}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{SPOTIFY_API_BASE}/me", headers=headers)
            if resp.status_code == 200:
                user_data = resp.json()
                expires_in = spotify_tokens.get("expires_at", 0) - time.time()
                return AuthStatus(
                    authenticated=True,
                    user_id=user_data.get("id"),
                    token_valid=True,
                    expires_in=int(expires_in)
                )
            else:
                return AuthStatus(authenticated=True, token_valid=False, expires_in=0)
        except httpx.RequestError:
            return AuthStatus(authenticated=True, token_valid=False, expires_in=0)

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
    if not spotify_tokens.get("refresh_token"):
        raise HTTPException(status_code=400, detail="No refresh token available.")

    data = {
        "grant_type": "refresh_token",
        "refresh_token": spotify_tokens["refresh_token"],
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(SPOTIFY_TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
            resp.raise_for_status()
            new_tokens = resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=400, detail=f"Failed to refresh token: {e.response.text}")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Service unavailable: Could not connect to Spotify.")

    spotify_tokens["access_token"] = new_tokens["access_token"]
    spotify_tokens["expires_at"] = time.time() + new_tokens["expires_in"] - 60
    if "refresh_token" in new_tokens:
        spotify_tokens["refresh_token"] = new_tokens["refresh_token"]

    save_tokens(spotify_tokens)

    return RefreshResponse(expires_at=int(spotify_tokens["expires_at"]))
