import logging
from fastapi import APIRouter, HTTPException
from zotify_api.services import auth_service
import time

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

log = logging.getLogger(__name__)

@router.post("/login", status_code=202)
def login_start():
    """
    Initiates the Spotify OAuth2 authentication flow by launching the Snitch
    helper and returning the Spotify authorization URL.
    """
    log.info("Authentication flow started.")
    result = auth_service.start_authentication_flow()

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    # This is a simplified example. In a real app, you'd manage the thread
    # and the captured code more robustly, perhaps with a background task system.
    ipc_server_thread = result.pop("ipc_server_thread")

    # For this example, we'll just wait a bit for the code to be captured.
    # A real implementation would use a more sophisticated mechanism.
    ipc_server_thread.join(timeout=125) # Wait max 2 minutes for Snitch

    if ipc_server_thread.is_alive():
        log.warning("IPC server timed out waiting for code from Snitch.")
        # The IPC server's handle_request will exit, so the thread will stop.
        raise HTTPException(status_code=408, detail="Request timed out waiting for OAuth code.")

    captured_code = ipc_server_thread.captured_code
    if not captured_code:
        log.error("IPC server finished but no code was captured.")
        raise HTTPException(status_code=500, detail="Failed to capture OAuth code.")

    log.info(f"Successfully captured OAuth code: {captured_code}")
    # Here, you would exchange the code for a token with Spotify.
    return {"status": "success", "message": "OAuth code captured. Token exchange would happen here."}
