import logging
import time
import httpx
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from zotify_api.auth_state import (
    spotify_tokens, pending_states, save_tokens,
    CLIENT_ID, REDIRECT_URI, SPOTIFY_TOKEN_URL
)


router = APIRouter(prefix="/auth")
logger = logging.getLogger(__name__)


class SpotifyCallbackPayload(BaseModel):
    code: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)

class CallbackResponse(BaseModel):
    status: str


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

    # 3. Store tokens in our in-memory store
    spotify_tokens.update({
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"), # Refresh token is optional
        "expires_at": time.time() + tokens["expires_in"] - 60,
    })
    save_tokens(spotify_tokens)
    logger.info("Successfully exchanged code for token and stored them.")

    # 4. Respond with minimal success message
    return {"status": "success"}
