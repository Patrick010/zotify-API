from fastapi import APIRouter
from zotify_api.models.user import User
from typing import List

router = APIRouter()

mock_user = User(
    id="dummy-user",
    username="dummy_user",
    email="dummy@example.com",
    liked_tracks=["track1", "track2"],
    history=["track3", "track4"],
    settings={"theme": "dark"}
)

@router.get("/user", response_model=User)
def get_user_info():
    return mock_user

@router.get("/user/profile", response_model=User)
def get_user_profile():
    return mock_user

@router.get("/user/liked", response_model=List[str])
def get_user_liked():
    return mock_user.liked_tracks

@router.post("/user/sync_liked")
def sync_user_liked():
    return {"status": "Liked songs synced"}

@router.get("/user/history", response_model=List[str])
def get_user_history():
    return mock_user.history

@router.delete("/user/history")
def delete_user_history():
    mock_user.history = []
    return {"status": "History cleared"}
