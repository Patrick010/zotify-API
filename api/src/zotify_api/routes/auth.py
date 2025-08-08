import logging
from fastapi import APIRouter, HTTPException
from zotify_api.services import auth_service
import time

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

log = logging.getLogger(__name__)

@router.post("/spotify/start", status_code=200)
def spotify_auth_start():
    """
    Initiates the Spotify OAuth2 PKCE flow. This endpoint generates the
    necessary state and code_challenge, stores the code_verifier, and returns
    the full authorization URL for the client to open.
    """
    log.info("Spotify authentication flow started.")
    result = auth_service.start_pkce_flow()

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result


from pydantic import BaseModel

class SpotifyCallbackPayload(BaseModel):
    code: str
    state: str

@router.post("/spotify/callback")
async def spotify_callback(payload: SpotifyCallbackPayload):
    """
    Callback endpoint for Snitch to post the captured authorization code and state.
    This endpoint then exchanges the code for an access token.
    """
    log.info(f"Received callback from Snitch for state: {payload.state}")
    result = await auth_service.exchange_code_for_token(payload.code, payload.state)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
