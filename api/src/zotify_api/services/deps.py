import logging
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from zotify_api.config import settings
from zotify_api.database import crud
from zotify_api.database.session import get_db
from zotify_api.providers.base import BaseProvider
from zotify_api.providers.spotify_connector import SpotifyConnector
from zotify_api.services.spoti_client import SpotiClient

logger = logging.getLogger(__name__)


def get_settings():
    return settings


async def get_spoti_client(db: Session = Depends(get_db)) -> SpotiClient:
    """
    FastAPI dependency that provides a fully authenticated SpotiClient.
    It handles token loading, validation, and refreshing.
    """
    token = crud.get_spotify_token(db)
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated with Spotify. Please login first.",
        )

    if token.expires_at <= datetime.now(timezone.utc):
        logger.info("Spotify token expired, refreshing...")
        if not token.refresh_token:
            raise HTTPException(
                status_code=401,
                detail=(
                    "Spotify token is expired and no refresh token is available. "
                    "Please login again."
                ),
            )

        new_token_data = await SpotiClient.refresh_access_token(token.refresh_token)

        expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=new_token_data["expires_in"] - 60
        )
        token_data_to_save = {
            "access_token": new_token_data["access_token"],
            "refresh_token": new_token_data.get("refresh_token", token.refresh_token),
            "expires_at": expires_at,
        }
        token = crud.create_or_update_spotify_token(db, token_data_to_save)

    return SpotiClient(
        access_token=token.access_token, refresh_token=token.refresh_token
    )


async def get_provider(
    db: Session = Depends(get_db), client: SpotiClient = Depends(get_spoti_client)
) -> BaseProvider:
    """
    Provider manager dependency for routes that require prior authentication.
    For now, it always returns the SpotifyConnector. In the future, this could
    select a provider based on user settings or other criteria.
    """
    return SpotifyConnector(client=client, db=db)


def get_provider_no_auth(
    provider_name: str, db: Session = Depends(get_db)
) -> BaseProvider:
    """
    Provider manager dependency for routes that do not require prior authentication,
    such as the OAuth login and callback endpoints.
    """
    if provider_name == "spotify":
        return SpotifyConnector(db=db)
    raise HTTPException(
        status_code=404, detail=f"Provider '{provider_name}' not found."
    )
