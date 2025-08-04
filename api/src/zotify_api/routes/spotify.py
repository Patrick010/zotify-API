import logging
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from pydantic import BaseModel
from typing import Optional, List
import httpx
import time

from zotify_api.models.spotify import OAuthLoginResponse, TokenStatus

router = APIRouter(prefix="/spotify")
logger = logging.getLogger(__name__)

# In-memory token store (replace with secure DB in prod)
spotify_tokens = {
    "access_token": None,
    "refresh_token": None,
    "expires_at": 0
}

CLIENT_ID = "65b708073fc0480ea92a077233ca87bd"
CLIENT_SECRET = "your_spotify_client_secret"
REDIRECT_URI = "http://localhost:8080/api/spotify/callback"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


@router.get("/login", response_model=OAuthLoginResponse)
def spotify_login():
    scope = "playlist-read-private playlist-modify-private playlist-modify-public user-library-read user-library-modify"
    auth_url = (
        f"{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}"
        f"&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}"
    )
    return {"auth_url": auth_url}


@router.get("/callback")
async def spotify_callback(code: Optional[str] = None):
    logger.info(f"Received callback with code: {code}")
    if not code:
        logger.error("Missing code query parameter")
        raise HTTPException(400, "Missing code query parameter")

    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        logger.info(f"Requesting tokens from {SPOTIFY_TOKEN_URL}")
        resp = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
        if resp.status_code != 200:
            logger.error(f"Failed to get tokens: {resp.text}")
            raise HTTPException(400, f"Failed to get tokens: {resp.text}")
        tokens = await resp.json()
        logger.info(f"Received tokens: {tokens}")
        spotify_tokens.update({
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "expires_at": time.time() + tokens["expires_in"] - 60,
        })
    logger.info("Spotify tokens stored")
    return {"status": "Spotify tokens stored"}


@router.get("/token_status", response_model=TokenStatus)
def token_status():
    valid = spotify_tokens["access_token"] is not None and spotify_tokens["expires_at"] > time.time()
    expires_in = max(0, int(spotify_tokens["expires_at"] - time.time()))
    return {"access_token_valid": valid, "expires_in_seconds": expires_in}


async def refresh_token_if_needed():
    if spotify_tokens["expires_at"] > time.time():
        return  # still valid

    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": spotify_tokens["refresh_token"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
        if resp.status_code != 200:
            # handle token refresh failure here (notify user, log, etc)
            raise HTTPException(401, "Spotify token refresh failed")
        tokens = resp.json()
        spotify_tokens["access_token"] = tokens["access_token"]
        spotify_tokens["expires_at"] = time.time() + tokens["expires_in"] - 60


# Playlist sync example stub
@router.post("/sync_playlists")
async def sync_playlists():
    await refresh_token_if_needed()
    # Fetch Spotify playlists, local playlists
    # Reconcile differences (create/update/delete)
    # Return sync summary and any conflicts
    return {"status": "Playlists synced (stub)"}


# Metadata fetch example stub
@router.get("/metadata/{track_id}")
async def fetch_metadata(track_id: str):
    logger.info(f"Fetching metadata for track: {track_id}")
    await refresh_token_if_needed()
    headers = {"Authorization": f"Bearer {spotify_tokens['access_token']}"}
    async with httpx.AsyncClient() as client:
        logger.info(f"Requesting metadata from {SPOTIFY_API_BASE}/tracks/{track_id}")
        resp = await client.get(f"{SPOTIFY_API_BASE}/tracks/{track_id}", headers=headers)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch track metadata: {resp.text}")
            raise HTTPException(resp.status_code, "Failed to fetch track metadata")
        logger.info(f"Received metadata: {resp.json()}")
        return await resp.json()

@router.post("/playlist/sync")
async def playlist_sync():
    await refresh_token_if_needed()
    # Fetch Spotify playlists, local playlists
    # Reconcile differences (create/update/delete)
    # Return sync summary and any conflicts
    return {"status": "Playlists synced (stub)"}
