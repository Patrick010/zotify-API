from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/search")
def search():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/download")
def download():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/download/status")
def download_status():
    raise HTTPException(status_code=501, detail="Not Implemented")
