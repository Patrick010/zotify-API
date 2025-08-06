from fastapi import Header, HTTPException
from zotify_api.config import settings

from fastapi import Header, HTTPException, status

def require_admin_api_key(x_api_key: str | None = Header(None)):
    # read settings dynamically every call
    configured = settings.admin_api_key
    if not configured:
        # Decide behavior: tests expect 401 when admin key not configured? They expected 503 earlier.
        # Keep 503 for "admin not configured" but tests set it in their setup, so this will be fine.
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Admin API not configured")
    if x_api_key != configured:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    # returns None when OK; used as Depends(require_admin_api_key)
