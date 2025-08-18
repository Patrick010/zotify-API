import logging
import secrets
import base64
import hashlib
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
import httpx
from urllib.parse import quote_plus

from zotify_api.database import crud
from zotify_api.schemas.auth import AuthStatus, RefreshResponse, SpotifyCallbackPayload, CallbackResponse, OAuthLoginResponse
from zotify_api.core.logging_framework import log_event
from zotify_api.services.auth import require_admin_api_key, refresh_spotify_token, get_auth_status
from zotify_api.services.deps import get_db
from zotify_api.auth_state import (
    pending_states, CLIENT_ID, REDIRECT_URI,
    SPOTIFY_AUTH_URL, SPOTIFY_TOKEN_URL
)


router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)


def generate_pkce_pair():
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b"=").decode()
    return code_verifier, code_challenge


@router.get("/spotify/login", response_model=OAuthLoginResponse)
def spotify_login():
    scope = "ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-follow-modify user-follow-read user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read user-read-email user-read-private"
    code_verifier, code_challenge = generate_pkce_pair()
    state = secrets.token_urlsafe(16)
    pending_states[state] = code_verifier
    auth_url = (
        f"{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={quote_plus(REDIRECT_URI)}"
        f"&scope={quote_plus(scope)}"
        f"&state={state}"
        f"&code_challenge_method=S256"
        f"&code_challenge={code_challenge}"
    )
    return {"auth_url": auth_url}


@router.get("/spotify/callback")
async def spotify_callback(code: str, state: str, db: Session = Depends(get_db)):
    if state not in pending_states:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    code_verifier = pending_states.pop(state)
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "code_verifier": code_verifier,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
            resp.raise_for_status()
            tokens = resp.json()

            token_data = {
                "access_token": tokens["access_token"],
                "refresh_token": tokens.get("refresh_token"),
                "expires_at": datetime.now(timezone.utc) + timedelta(seconds=tokens["expires_in"] - 60)
            }
            crud.create_or_update_spotify_token(db=db, token_data=token_data)

            return {"status": "success", "message": "Successfully authenticated with Spotify."}
        except httpx.HTTPStatusError as e:
            log_event(
                "Failed to get token from Spotify",
                level="ERROR",
                tags=["security"],
                details={"status_code": e.response.status_code, "response": e.response.text},
            )
            raise HTTPException(status_code=e.response.status_code, detail="Failed to retrieve token from Spotify")
        except httpx.RequestError as e:
            logger.error(f"Request to Spotify failed: {e}")
            raise HTTPException(status_code=503, detail="Could not connect to Spotify")


@router.get("/status", response_model=AuthStatus, dependencies=[Depends(require_admin_api_key)])
async def get_status(db: Session = Depends(get_db)):
    """ Returns the current authentication status """
    return await get_auth_status(db=db)

@router.post("/logout", status_code=204, dependencies=[Depends(require_admin_api_key)])
def logout(db: Session = Depends(get_db)):
    """
    Clears stored Spotify credentials from the database.

    This function deletes the token from local storage, effectively logging the user out
    from this application's perspective.
    """
    crud.delete_spotify_token(db=db)
    return {}

@router.get("/refresh", response_model=RefreshResponse, dependencies=[Depends(require_admin_api_key)])
async def refresh(db: Session = Depends(get_db)):
    """ Refreshes the Spotify access token """
    new_expires_at = await refresh_spotify_token(db=db)
    return RefreshResponse(expires_at=new_expires_at)
