import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from zotify_api.auth_state import pending_states
from zotify_api.database import crud
from zotify_api.schemas.auth import AuthStatus
from zotify_api.services.deps import get_db, get_settings
from zotify_api.services.spoti_client import SpotiClient

log = logging.getLogger(__name__)


def get_admin_api_key_header(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
) -> Optional[str]:
    return x_api_key


def require_admin_api_key(
    x_api_key: Optional[str] = Depends(get_admin_api_key_header),
    settings=Depends(get_settings),
):
    if not settings.admin_api_key:
        raise HTTPException(status_code=503, detail="Admin API key not configured")
    if x_api_key != settings.admin_api_key:
        log.warning("Unauthorized admin attempt", extra={"path": "unknown"})
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


async def refresh_spotify_token(db: Session = Depends(get_db)) -> int:
    """
    Refreshes the access token using the stored refresh token and saves the new
    token to the database. Returns the new expiration timestamp.
    """
    token = crud.get_spotify_token(db)
    if not token or not token.refresh_token:
        raise HTTPException(
            status_code=401, detail="No refresh token available to refresh with."
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
    updated_token = crud.create_or_update_spotify_token(db, token_data_to_save)
    return int(updated_token.expires_at.timestamp())


async def get_auth_status(db: Session = Depends(get_db)) -> AuthStatus:
    """
    Checks the current authentication status with Spotify by using the token
    from the database.
    """
    token = crud.get_spotify_token(db)
    if not token or not token.access_token:
        return AuthStatus(authenticated=False, token_valid=False, expires_in=0)

    expires_at = token.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= datetime.now(timezone.utc):
        return AuthStatus(authenticated=False, token_valid=False, expires_in=0)

    client = SpotiClient(access_token=token.access_token)
    try:
        user_data = await client.get_current_user()
        expires_in = token.expires_at.timestamp() - time.time()
        return AuthStatus(
            authenticated=True,
            user_id=user_data.get("id"),
            token_valid=True,
            expires_in=int(expires_in),
        )
    except HTTPException as e:
        if e.status_code == 401:
            return AuthStatus(authenticated=True, token_valid=False, expires_in=0)
        raise
    finally:
        await client.close()


async def handle_spotify_callback(
    code: str, state: str, db: Session = Depends(get_db)
) -> None:
    """
    Handles the OAuth callback, exchanges the code for tokens, and saves them
    to the database.
    """
    code_verifier = pending_states.pop(state, None)
    if not code_verifier:
        log.warning(f"Invalid or expired state received in callback: {state}")
        raise HTTPException(status_code=400, detail="Invalid or expired state token.")

    tokens = await SpotiClient.exchange_code_for_token(code, code_verifier)

    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=tokens["expires_in"] - 60
    )
    token_data_to_save = {
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"),
        "expires_at": expires_at,
    }
    crud.create_or_update_spotify_token(db, token_data_to_save)
    log.info("Successfully exchanged code for token and stored them.")
