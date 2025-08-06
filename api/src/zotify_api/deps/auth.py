from fastapi import Header, HTTPException, status
from zotify_api.config import settings

def require_admin_api_key(x_api_key: str | None = Header(None)):
    configured = settings.admin_api_key
    if not configured:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Admin API not configured")
    if x_api_key != configured:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid API key")
    return True
