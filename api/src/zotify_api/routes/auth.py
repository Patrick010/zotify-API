import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from zotify_api.database import crud
from zotify_api.schemas.auth import AuthStatus, RefreshResponse, SpotifyCallbackPayload, CallbackResponse
from zotify_api.services.auth import require_admin_api_key, refresh_spotify_token, get_auth_status, handle_spotify_callback
from zotify_api.services.deps import get_db


router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

@router.post("/spotify/callback", response_model=CallbackResponse)
async def spotify_callback(payload: SpotifyCallbackPayload, db: Session = Depends(get_db)):
    """
    Handles the secure callback from the Snitch service after user authentication.
    """
    await handle_spotify_callback(code=payload.code, state=payload.state, db=db)
    return {"status": "success"}

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
