from typing import Any, Dict

from fastapi import APIRouter, Depends

from zotify_api.schemas.generic import StandardResponse
from zotify_api.schemas.user import (
    SyncLikedResponse,
    UserPreferences,
    UserPreferencesUpdate,
    UserProfileResponse,
    UserProfileUpdate,
)
from zotify_api.services.user_service import UserService, get_user_service

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile", response_model=StandardResponse[UserProfileResponse])
def get_user_profile(user_service: UserService = Depends(get_user_service)):
    profile = user_service.get_user_profile()
    return {"data": profile}


@router.patch("/profile", response_model=StandardResponse[UserProfileResponse])
def update_user_profile(
    profile_data: UserProfileUpdate,
    user_service: UserService = Depends(get_user_service),
):
    profile = user_service.update_user_profile(
        profile_data.model_dump(exclude_unset=True)
    )
    return {"data": profile}


@router.get("/preferences", response_model=StandardResponse[UserPreferences])
def get_user_preferences(user_service: UserService = Depends(get_user_service)):
    preferences = user_service.get_user_preferences()
    return {"data": preferences}


@router.patch("/preferences", response_model=StandardResponse[UserPreferences])
def update_user_preferences(
    preferences_data: UserPreferencesUpdate,
    user_service: UserService = Depends(get_user_service),
):
    preferences = user_service.update_user_preferences(
        preferences_data.model_dump(exclude_unset=True)
    )
    return {"data": preferences}


@router.get("/liked", response_model=Dict[str, Any])
def get_user_liked(user_service: UserService = Depends(get_user_service)):
    items = user_service.get_user_liked()
    return {"data": items, "meta": {"total": len(items)}}


@router.post("/sync_liked", response_model=StandardResponse[SyncLikedResponse])
def sync_user_liked(user_service: UserService = Depends(get_user_service)):
    result = user_service.sync_user_liked()
    return {"data": result}


@router.get("/history", response_model=Dict[str, Any])
def get_user_history(user_service: UserService = Depends(get_user_service)):
    items = user_service.get_user_history()
    return {"data": items, "meta": {"total": len(items)}}


@router.delete("/history", status_code=204)
def delete_user_history(user_service: UserService = Depends(get_user_service)):
    user_service.delete_user_history()
    return {}
