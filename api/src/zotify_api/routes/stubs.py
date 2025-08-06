from fastapi import APIRouter, HTTPException, Depends
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(dependencies=[Depends(require_admin_api_key)])

@router.post("/download")
def download():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/download/status")
def download_status():
    raise HTTPException(status_code=501, detail="Not Implemented")
