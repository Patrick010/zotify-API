import logging
import time
import secrets
import base64
import hashlib
from fastapi import APIRouter, HTTPException, Request, Response
from typing import Optional
import httpx
from zotify_api.schemas.spotify import SpotifyDevices, OAuthLoginResponse, TokenStatus
from urllib.parse import quote_plus

# Import the shared state and constants
from zotify_api.auth_state import (
    spotify_tokens, pending_states, save_tokens,
    CLIENT_ID, CLIENT_SECRET, REDIRECT_URI,
    SPOTIFY_AUTH_URL, SPOTIFY_TOKEN_URL, SPOTIFY_API_BASE
)

router = APIRouter(prefix="/spotify", tags=["spotify"])
logger = logging.getLogger(__name__)


def generate_pkce_pair():
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b"=").decode()
    return code_verifier, code_challenge


@router.get("/login", response_model=OAuthLoginResponse)
def spotify_login():
    scope = (
        "app-remote-control playlist-modify playlist-modify-private playlist-modify-public "
        "playlist-read playlist-read-collaborative playlist-read-private streaming "
        "ugc-image-upload user-follow-modify user-follow-read user-library-modify user-library-read "
        "user-modify user-modify-playback-state user-modify-private user-personalized user-read-birthdate "
        "user-read-currently-playing user-read-email user-read-play-history user-read-playback-position "
        "user-read-playback-state user-read-private user-read-recently-played user-top-read"
    )
    code_verifier, code_challenge = generate_pkce_pair()
    state = secrets.token_urlsafe(16)

    # Store the code_verifier indexed by state for callback verification
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


@router.get("/callback")
async def spotify_callback(code: str, state: str, response: Response):
    """
    Callback endpoint for Spotify OAuth2 flow.
    """
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
            tokens = await resp.json()

            # Persist tokens
            spotify_tokens["access_token"] = tokens["access_token"]
            spotify_tokens["refresh_token"] = tokens.get("refresh_token")
            spotify_tokens["expires_at"] = time.time() + tokens["expires_in"] - 60  # 60s buffer
            save_tokens(spotify_tokens)

            return {"status": "success", "message": "Successfully authenticated with Spotify."}
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to get token from Spotify: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail="Failed to retrieve token from Spotify")
        except httpx.RequestError as e:
            logger.error(f"Request to Spotify failed: {e}")
            raise HTTPException(status_code=503, detail="Could not connect to Spotify")


@router.get("/token_status", response_model=TokenStatus)
def token_status():
    valid = spotify_tokens["access_token"] is not None and spotify_tokens["expires_at"] > time.time()
    expires_in = max(0, int(spotify_tokens["expires_at"] - time.time()))
    return {"access_token_valid": valid, "expires_in_seconds": expires_in}


async def refresh_token_if_needed():
    if spotify_tokens["expires_at"] > time.time():
        return  # Token still valid

    if not spotify_tokens["refresh_token"]:
        raise HTTPException(401, "No refresh token available")

    data = {
        "grant_type": "refresh_token",
        "refresh_token": spotify_tokens["refresh_token"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        resp = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(401, "Spotify token refresh failed")
        tokens = resp.json()
        spotify_tokens["access_token"] = tokens["access_token"]
        spotify_tokens["expires_at"] = time.time() + tokens["expires_in"] - 60
        save_tokens(spotify_tokens)


@router.post("/sync_playlists")
async def sync_playlists():
    await refresh_token_if_needed()
    # TODO: implement playlist sync logic here
    return {"status": "Playlists synced (stub)"}


@router.get("/metadata/{track_id}")
async def fetch_metadata(track_id: str):
    logger.info(f"Fetching metadata for track: {track_id}")
    await refresh_token_if_needed()
    headers = {"Authorization": f"Bearer {spotify_tokens['access_token']}"}
    async with httpx.AsyncClient() as client:
        url = f"{SPOTIFY_API_BASE}/tracks/{track_id}"
        logger.info(f"Requesting metadata from {url}")
        resp = await client.get(url, headers=headers)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch track metadata: {await resp.text()}")
            raise HTTPException(resp.status_code, "Failed to fetch track metadata")
        data = await resp.json()
        logger.info(f"Received metadata: {data}")
        return data


@router.get("/playlists")
def get_spotify_playlists():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/playlists/{playlist_id}")
def get_spotify_playlist(playlist_id: str):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.delete("/playlists/{playlist_id}")
def delete_spotify_playlist(playlist_id: str):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/playlists/{playlist_id}/tracks")
def get_spotify_playlist_tracks(playlist_id: str):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/playlists/{playlist_id}/sync")
def sync_spotify_playlist(playlist_id: str):
    raise HTTPException(status_code=501, detail="Not Implemented")

from zotify_api.services.auth import require_admin_api_key
from fastapi import Depends

@router.put("/playlists/{playlist_id}/metadata")
def update_spotify_playlist_metadata(playlist_id: str):
    raise HTTPException(status_code=501, detail="Not Implemented")

from zotify_api.services import spotify as spotify_service

@router.get("/me", dependencies=[Depends(require_admin_api_key)])
async def get_me():
    """ Returns raw Spotify /v1/me profile. For debugging and verification. """
    return await spotify_service.get_me()

@router.get("/devices", response_model=SpotifyDevices, dependencies=[Depends(require_admin_api_key)])
async def get_devices():
    """ Wraps Spotify /v1/me/player/devices. Lists all playback devices. """
    devices = await spotify_service.get_spotify_devices()
    return {"devices": devices}
