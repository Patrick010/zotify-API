import secrets
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from zotify_api.database.session import get_db
from zotify_api.providers.base import BaseProvider
from zotify_api.schemas.auth import AuthStatus, OAuthLoginResponse
from zotify_api.services.auth import get_auth_status, require_admin_api_key
from zotify_api.services.deps import get_provider_no_auth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/{provider_name}/login", response_model=OAuthLoginResponse)
async def provider_login(
    provider: BaseProvider = Depends(get_provider_no_auth),
) -> OAuthLoginResponse:
    """
    Initiates the OAuth2 login flow for a given provider.
    """
    state = secrets.token_urlsafe(16)
    auth_url = await provider.get_oauth_login_url(state)
    return OAuthLoginResponse(auth_url=auth_url)


@router.get("/{provider_name}/callback")
async def provider_callback(
    provider: BaseProvider = Depends(get_provider_no_auth),
    code: Optional[str] = None,
    error: Optional[str] = None,
    state: Optional[str] = None,
) -> HTMLResponse:
    """
    Handles the OAuth2 callback from the provider.
    """
    html_content = await provider.handle_oauth_callback(
        code=code, error=error, state=state
    )
    return HTMLResponse(content=html_content)


@router.get(
    "/status",
    response_model=AuthStatus,
    dependencies=[Depends(require_admin_api_key)],
)
async def get_status(db: Session = Depends(get_db)) -> AuthStatus:
    """Returns the current authentication status"""
    return await get_auth_status(db=db)


@router.post("/logout", status_code=204, dependencies=[Depends(require_admin_api_key)])
def logout(db: Session = Depends(get_db)) -> None:
    """
    Clears stored provider credentials from the database.
    TODO: This is currently provider-specific and should be moved to the provider layer.
    """
    from zotify_api.database import crud

    crud.delete_spotify_token(db=db)
    return
