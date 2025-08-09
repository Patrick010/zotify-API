import logging
from fastapi import Depends, Header, HTTPException
from typing import Optional
from zotify_api.services.deps import get_settings

log = logging.getLogger(__name__)

def get_admin_api_key_header(x_api_key: Optional[str] = Header(None, alias="X-API-Key")) -> Optional[str]:
    return x_api_key

from zotify_api.services.spoti_client import SpotiClient
from zotify_api.auth_state import spotify_tokens
from fastapi import HTTPException

def require_admin_api_key(x_api_key: Optional[str] = Depends(get_admin_api_key_header), settings = Depends(get_settings)):
    if not settings.admin_api_key:
        # admin key not configured
        raise HTTPException(status_code=503, detail="Admin API key not configured")
    if x_api_key != settings.admin_api_key:
        log.warning("Unauthorized admin attempt", extra={"path": "unknown"})  # improve with request path if available
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


import time
from zotify_api.schemas.auth import AuthStatus

async def refresh_spotify_token() -> int:
    """
    Uses the SpotiClient to refresh the access token.
    Returns the new expiration timestamp.
    """
    client = SpotiClient()
    try:
        await client.refresh_access_token()
        return int(spotify_tokens.get("expires_at", 0))
    finally:
        await client.close()


from zotify_api.auth_state import pending_states, save_tokens

async def get_auth_status() -> AuthStatus:
    """
    Checks the current authentication status with Spotify.
    """
    if not spotify_tokens.get("access_token"):
        return AuthStatus(authenticated=False, token_valid=False, expires_in=0)

    client = SpotiClient()
    try:
        user_data = await client.get_current_user()
        expires_in = spotify_tokens.get("expires_at", 0) - time.time()
        return AuthStatus(
            authenticated=True,
            user_id=user_data.get("id"),
            token_valid=True,
            expires_in=int(expires_in)
        )
    except HTTPException as e:
        # If get_current_user fails (e.g. token expired), we're not valid.
        if e.status_code == 401:
            return AuthStatus(authenticated=True, token_valid=False, expires_in=0)
        raise  # Re-raise other exceptions
    finally:
        await client.close()

async def handle_spotify_callback(code: str, state: str) -> None:
    """
    Handles the OAuth callback from Spotify, exchanges the code for tokens, and saves them.
    """
    code_verifier = pending_states.pop(state, None)
    if not code_verifier:
        logger.warning(f"Invalid or expired state received in callback: {state}")
        raise HTTPException(status_code=400, detail="Invalid or expired state token.")

    client = SpotiClient()
    try:
        tokens = await client.exchange_code_for_token(code, code_verifier)

        spotify_tokens.update({
            "access_token": tokens["access_token"],
            "refresh_token": tokens.get("refresh_token"),
            "expires_at": time.time() + tokens["expires_in"] - 60,
        })
        save_tokens(spotify_tokens)
        logger.info("Successfully exchanged code for token and stored them.")
    finally:
        await client.close()
