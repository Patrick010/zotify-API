from zotify_api.config import settings
import time
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from datetime import datetime, timezone, timedelta

from zotify_api.database import crud
from zotify_api.database.session import get_db
from zotify_api.services.spoti_client import SpotiClient
from zotify_api.auth_state import CLIENT_ID, CLIENT_SECRET, SPOTIFY_TOKEN_URL

def get_settings():
    return settings

async def get_spoti_client(db: Session = Depends(get_db)) -> SpotiClient:
    """
    FastAPI dependency that provides a fully authenticated SpotiClient.
    It handles token loading, validation, and refreshing.
    """
    token = crud.get_spotify_token(db)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated with Spotify. Please login first.")

    if token.expires_at <= datetime.now(timezone.utc):
        # Token is expired, refresh it
        if not token.refresh_token:
            raise HTTPException(status_code=401, detail="Spotify token is expired and no refresh token is available. Please login again.")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": token.refresh_token,
            "client_id": CLIENT_ID,
        }
        if CLIENT_SECRET:
            data["client_secret"] = CLIENT_SECRET

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
                resp.raise_for_status()
                new_tokens = await resp.json()

                token_data = {
                    "access_token": new_tokens["access_token"],
                    "refresh_token": new_tokens.get("refresh_token", token.refresh_token),
                    "expires_at": datetime.now(timezone.utc) + timedelta(seconds=new_tokens["expires_in"] - 60),
                }
                token = crud.create_or_update_spotify_token(db, token_data)
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=f"Failed to refresh Spotify token: {e.response.text}")

    return SpotiClient(auth_token=token.access_token)


from zotify_api.providers.base import BaseProvider
from zotify_api.providers.spotify_adapter import SpotifyAdapter

async def get_provider(db: Session = Depends(get_db), client: SpotiClient = Depends(get_spoti_client)) -> BaseProvider:
    """
    Provider manager dependency.
    For now, it always returns the SpotifyAdapter. In the future, this could
    select a provider based on user settings or other criteria.
    """
    return SpotifyAdapter(client=client, db=db)
