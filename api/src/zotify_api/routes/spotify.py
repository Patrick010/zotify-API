import logging
import time
import secrets
import base64
import hashlib
from fastapi import APIRouter, HTTPException, Response, Depends, Query, Body
from typing import List
import httpx
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from zotify_api.schemas.spotify import (
    SpotifyDevices, OAuthLoginResponse, TokenStatus, Playlist, PlaylistTracks,
    CreatePlaylistRequest, AddTracksRequest, RemoveTracksRequest
)
from urllib.parse import quote_plus

from zotify_api.auth_state import (
    pending_states, CLIENT_ID, REDIRECT_URI,
    SPOTIFY_AUTH_URL, SPOTIFY_TOKEN_URL
)
from zotify_api.services import spotify as spotify_service
from zotify_api.database.session import get_db
from zotify_api.database import crud
from zotify_api.services.auth import require_admin_api_key
from zotify_api.services.deps import get_spoti_client
from zotify_api.services.spoti_client import SpotiClient

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
    scope = "user-read-private user-read-email playlist-read-private"
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


@router.get("/callback")
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
            tokens = await resp.json()

            token_data = {
                "access_token": tokens["access_token"],
                "refresh_token": tokens.get("refresh_token"),
                "expires_at": datetime.now(timezone.utc) + timedelta(seconds=tokens["expires_in"] - 60)
            }
            crud.create_or_update_spotify_token(db=db, token_data=token_data)

            return {"status": "success", "message": "Successfully authenticated with Spotify."}
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to get token from Spotify: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail="Failed to retrieve token from Spotify")
        except httpx.RequestError as e:
            logger.error(f"Request to Spotify failed: {e}")
            raise HTTPException(status_code=503, detail="Could not connect to Spotify")


@router.get("/token_status", response_model=TokenStatus)
def token_status(db: Session = Depends(get_db)):
    token = crud.get_spotify_token(db)
    if not token:
        return {"access_token_valid": False, "expires_in_seconds": 0}

    valid = token.expires_at > datetime.now(timezone.utc)
    expires_in = max(0, int((token.expires_at - datetime.now(timezone.utc)).total_seconds()))
    return {"access_token_valid": valid, "expires_in_seconds": expires_in}


@router.post("/sync_playlists", dependencies=[Depends(require_admin_api_key)])
async def sync_playlists_route(db: Session = Depends(get_db), client: SpotiClient = Depends(get_spoti_client)):
    return await spotify_service.sync_playlists(db=db, client=client)


@router.get("/playlists", response_model=dict, dependencies=[Depends(require_admin_api_key)])
async def get_spotify_playlists(
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    client: SpotiClient = Depends(get_spoti_client)
):
    return await spotify_service.get_playlists(limit=limit, offset=offset, client=client)


@router.post("/playlists", response_model=Playlist, status_code=201, dependencies=[Depends(require_admin_api_key)])
async def create_spotify_playlist(
    request: CreatePlaylistRequest = Body(...),
    client: SpotiClient = Depends(get_spoti_client)
):
    me = await spotify_service.get_me(client)
    user_id = me.get("id")
    if not user_id:
        raise HTTPException(status_code=500, detail="Could not determine user ID to create playlist.")
    return await spotify_service.create_playlist(
        user_id=user_id, name=request.name, public=request.public,
        collaborative=request.collaborative, description=request.description, client=client
    )

@router.get("/playlists/{playlist_id}", response_model=Playlist, dependencies=[Depends(require_admin_api_key)])
async def get_spotify_playlist(playlist_id: str, client: SpotiClient = Depends(get_spoti_client)):
    return await spotify_service.get_playlist(playlist_id, client)


@router.put("/playlists/{playlist_id}", status_code=204, dependencies=[Depends(require_admin_api_key)])
async def update_spotify_playlist_metadata(
    playlist_id: str,
    request: CreatePlaylistRequest = Body(...),
    client: SpotiClient = Depends(get_spoti_client)
):
    await spotify_service.update_playlist_details(
        playlist_id=playlist_id, name=request.name, public=request.public,
        collaborative=request.collaborative, description=request.description, client=client
    )

@router.delete("/playlists/{playlist_id}", status_code=204, dependencies=[Depends(require_admin_api_key)])
async def delete_spotify_playlist(playlist_id: str, client: SpotiClient = Depends(get_spoti_client)):
    await spotify_service.unfollow_playlist(playlist_id, client)


@router.get("/playlists/{playlist_id}/tracks", response_model=PlaylistTracks, dependencies=[Depends(require_admin_api_key)])
async def get_spotify_playlist_tracks(
    playlist_id: str,
    limit: int = Query(100, ge=1, le=100),
    offset: int = Query(0, ge=0),
    client: SpotiClient = Depends(get_spoti_client)
):
    return await spotify_service.get_playlist_tracks(playlist_id, limit=limit, offset=offset, client=client)


@router.post("/playlists/{playlist_id}/tracks", status_code=201, dependencies=[Depends(require_admin_api_key)])
async def add_tracks_to_spotify_playlist(
    playlist_id: str,
    request: AddTracksRequest = Body(...),
    client: SpotiClient = Depends(get_spoti_client)
):
    return await spotify_service.add_tracks_to_playlist(playlist_id, request.uris, client)


@router.delete("/playlists/{playlist_id}/tracks", dependencies=[Depends(require_admin_api_key)])
async def remove_tracks_from_spotify_playlist(
    playlist_id: str,
    request: RemoveTracksRequest = Body(...),
    client: SpotiClient = Depends(get_spoti_client)
):
    return await spotify_service.remove_tracks_from_playlist(playlist_id, request.uris, client)


@router.get("/me", dependencies=[Depends(require_admin_api_key)])
async def get_me_route(client: SpotiClient = Depends(get_spoti_client)):
    return await spotify_service.get_me(client)


@router.get("/devices", response_model=SpotifyDevices, dependencies=[Depends(require_admin_api_key)])
async def get_devices(client: SpotiClient = Depends(get_spoti_client)):
    devices = await spotify_service.get_spotify_devices(client)
    return {"devices": devices}
