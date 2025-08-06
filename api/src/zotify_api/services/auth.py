import logging
from fastapi import Depends, Header, HTTPException
from typing import Optional
from zotify_api.services.deps import get_settings

log = logging.getLogger(__name__)

def get_admin_api_key_header(x_api_key: Optional[str] = Header(None, alias="X-API-Key")) -> Optional[str]:
    return x_api_key

def require_admin_api_key(x_api_key: Optional[str] = Depends(get_admin_api_key_header), settings = Depends(get_settings)):
    if not settings.admin_api_key:
        # admin key not configured
        raise HTTPException(status_code=503, detail="Admin API key not configured")
    if x_api_key != settings.admin_api_key:
        log.warning("Unauthorized admin attempt", extra={"path": "unknown"})  # improve with request path if available
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
