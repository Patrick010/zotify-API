from fastapi import APIRouter

router = APIRouter()

@router.get("/user")
def get_user_info():
    return {"username": "dummy_user", "email": "dummy@example.com"}

@router.get("/user/profile")
def get_user_profile():
    return {"username": "dummy_user", "email": "dummy@example.com", "settings": {}}

@router.get("/user/liked")
def get_user_liked():
    return ["track1", "track2"]

@router.post("/user/sync_liked")
def sync_user_liked():
    return {"status": "Liked songs synced"}

@router.get("/user/history")
def get_user_history():
    return ["track3", "track4"]

@router.delete("/user/history")
def delete_user_history():
    return {"status": "History cleared"}
