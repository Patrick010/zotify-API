from fastapi import APIRouter

router = APIRouter()

@router.get("/stubs")
def get_stubs():
    return {"message": "This is a stub endpoint."}

@router.get("/stubs/search")
def search():
    return {"status": "Search not implemented"}

@router.post("/stubs/download")
def download():
    return {"status": "Download not implemented"}

@router.get("/stubs/download/status")
def download_status():
    return {"status": "Download status not implemented"}
