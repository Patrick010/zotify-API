from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/user/profile")
def get_user_profile():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/user/liked")
def get_user_liked():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/user/sync_liked")
def sync_user_liked():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/user/history")
def get_user_history():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.delete("/user/history")
def delete_user_history():
    raise HTTPException(status_code=501, detail="Not Implemented")
