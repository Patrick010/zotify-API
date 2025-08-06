from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/download")
def download():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/download/status")
def download_status():
    raise HTTPException(status_code=501, detail="Not Implemented")
