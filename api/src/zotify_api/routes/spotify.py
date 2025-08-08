import logging
import time
import secrets
import base64
import hashlib
import urllib.parse

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import httpx

router = APIRouter(prefix="/spotify")
logger = logging.getLogger(__name__)

# In-memory token store (replace with secure DB in prod)
spotify_tokens = {
    "access_token": None,
    "refresh_token": None,
    "expires_at": 0,
    "code_verifier": None,  # PKCE code verifier stored temporarily
}

CLIENT_ID = "65b708073fc0480ea92a077233ca87bd"
CLIENT_SECRET = "832bc60deeb147db86dd1cc521d9e4bf"
REDIRECT_URI = "http://127.0.0.1:4381/login"  # must match Snitch listener URL

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


def generate_code_verifier() -> str:
    # Random 43-128 char string, URL safe base64
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(64)).rstrip(b"=").decode("utf-8")
    return verifier


def generate_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")
    return challenge


@router.get("/login")
def spotify_login():
    scope = (
        "app-remote-control playlist-modify playlist-modify-private playlist-modify-public "
        "playlist-read playlist-read-collaborative playlist-read-private streaming "
        "ugc-image-upload user-follow-modify user-follow-read user-library-modify user-library-read "
        "user-modify user-modify-playback-state user-modify-private user-personalized user-read-birthdate "
        "user-read-currently-playing user-read-email user-read-play-history user-read-playback-position "
        "user-read-playback-state user-read-private user-read-recently-played user-top-read"
    )
    code_verifier = generate_code_verifier()
    spotify_tokens["code_verifier"] = code_verifier
    code_challenge = generate_code_challenge(code_verifier)

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
    }
    url = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"
    logger.info(f"Generated Spotify auth URL: {url}")
    return {"auth_url": url}


@router.get("/callback")
async def spotify_callback(code: Optional[str] = Query(None)):
    logger.info(f"Received callback with code: {code}")
    if not code:
        logger.error("Missing code query parameter")
        raise HTTPException(400, "Missing code query parameter")
    if not spotify_tokens.get("code_verifier"):
        logger.error("Missing stored PKCE code_verifier")
        raise HTTPException(400, "PKCE code verifier not found. Please restart the login process.")

    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "code_verifier": spotify_tokens["code_verifier"],
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        logger.info(f"Requesting tokens from {SPOTIFY_TOKEN_URL}")
        resp = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
        if resp.status_code != 200:
            logger.error(f"Failed to get tokens: {await resp.text()}")
            raise HTTPException(400, f"Failed to get tokens: {await resp.text()}")
        tokens = await resp.json()
        logger.info(f"Received tokens: {tokens}")
        spotify_tokens.update({
            "access_token": tokens["access_token"],
            "refresh_token": tokens.get("refresh_token", spotify_tokens.get("refresh_token")),
            "expires_at": time.time() + tokens["expires_in"] - 60,
            "code_verifier": None,  # clear code_verifier after use
        })
    logger.info("Spotify tokens stored")
    return {"status": "Spotify tokens stored"}


@router.get("/token_status")
def token_status():
    valid = spotify_tokens["access_token"] is not None and spotify_tokens["expires_at"] > time.time()
    expires_in = max(0, int(spotify_tokens["expires_at"] - time.time()))
    return {"access_token_valid": valid, "expires_in_seconds": expires_in}


async def refresh_token_if_needed():
    if spotify_tokens["expires_at"] > time.time():
        return  # still valid
    if not spotify_tokens["refresh_token"]:
        logger.error("No refresh token available")
        raise HTTPException(401, "No refresh token available, please reauthenticate")

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
            logger.error(f"Spotify token refresh failed: {await resp.text()}")
            raise HTTPException(401, "Spotify token refresh failed")
        tokens = await resp.json()
        spotify_tokens["access_token"] = tokens["access_token"]
        spotify_tokens["expires_at"] = time.time() + tokens["expires_in"] - 60
        logger.info("Spotify token refreshed")


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

@router.put("/playlists/{playlist_id}/metadata")
def update_spotify_playlist_metadata(playlist_id: str):
    raise HTTPException(status_code=501, detail="Not Implemented")
