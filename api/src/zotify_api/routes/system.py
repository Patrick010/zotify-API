from fastapi import APIRouter, HTTPException, Depends
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(dependencies=[Depends(require_admin_api_key)])

@router.get("/system/status")
def get_system_status():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/system/storage")
def get_system_storage():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/system/logs")
def get_system_logs():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/system/reload")
def reload_system_config():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/system/reset")
def reset_system_state():
    raise HTTPException(status_code=501, detail="Not Implemented")
