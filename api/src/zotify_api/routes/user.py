from fastapi import APIRouter, Depends
from zotify_api.schemas.user import UserProfileResponse, UserLikedResponse, UserHistoryResponse, SyncLikedResponse
from zotify_api.services.user_service import UserService, get_user_service

router = APIRouter(prefix="/user")

@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(user_service: UserService = Depends(get_user_service)):
    return user_service.get_user_profile()

@router.get("/liked", response_model=UserLikedResponse)
def get_user_liked(user_service: UserService = Depends(get_user_service)):
    return {"items": user_service.get_user_liked()}

@router.post("/sync_liked", response_model=SyncLikedResponse)
def sync_user_liked(user_service: UserService = Depends(get_user_service)):
    return user_service.sync_user_liked()

@router.get("/history", response_model=UserHistoryResponse)
def get_user_history(user_service: UserService = Depends(get_user_service)):
    return {"items": user_service.get_user_history()}

@router.delete("/history", status_code=204)
def delete_user_history(user_service: UserService = Depends(get_user_service)):
    user_service.delete_user_history()
    return {}
