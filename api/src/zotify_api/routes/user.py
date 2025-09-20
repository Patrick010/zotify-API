from typing import Any, Dict

from fastapi import APIRouter, Depends

from zotify_api.database.models import User
from zotify_api.schemas.generic import StandardResponse
from zotify_api.schemas.user import (
    SyncLikedResponse,
    UserPreferences,
    UserPreferencesUpdate,
    UserProfileResponse,
    UserProfileUpdate,
)
from zotify_api.services.deps import get_current_user_service
from zotify_api.services.jwt_service import get_current_user
from zotify_api.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile", response_model=StandardResponse[UserProfileResponse])
def get_user_profile(
    user_service: UserService = Depends(get_current_user_service),
) -> Dict[str, Any]:
    profile = user_service.get_user_profile()
    return {"data": profile}


@router.patch("/profile", response_model=StandardResponse[UserProfileResponse])
def update_user_profile(
    profile_data: UserProfileUpdate,
    user_service: UserService = Depends(get_current_user_service),
) -> Dict[str, Any]:
    profile = user_service.update_user_profile(
        profile_data.model_dump(exclude_unset=True)
    )
    return {"data": profile}


@router.get("/preferences", response_model=StandardResponse[UserPreferences])
def get_user_preferences(
    user_service: UserService = Depends(get_current_user_service),
) -> Dict[str, Any]:
    preferences = user_service.get_user_preferences()
    return {"data": preferences}


@router.patch("/preferences", response_model=StandardResponse[UserPreferences])
def update_user_preferences(
    preferences_data: UserPreferencesUpdate,
    user_service: UserService = Depends(get_current_user_service),
) -> Dict[str, Any]:
    preferences = user_service.update_user_preferences(
        preferences_data.model_dump(exclude_unset=True)
    )
    return {"data": preferences}


@router.get("/liked", response_model=Dict[str, Any])
def get_user_liked(
    user_service: UserService = Depends(get_current_user_service),
) -> Dict[str, Any]:
    items = user_service.get_user_liked()
    return {"data": items, "meta": {"total": len(items)}}


@router.post("/sync_liked", response_model=StandardResponse[SyncLikedResponse])
def sync_user_liked(
    user_service: UserService = Depends(get_current_user_service),
) -> Dict[str, Any]:
    result = user_service.sync_user_liked()
    return {"data": result}


@router.get("/history", response_model=Dict[str, Any])
def get_user_history(
    user_service: UserService = Depends(get_current_user_service),
) -> Dict[str, Any]:
    items = user_service.get_user_history()
    return {"data": items, "meta": {"total": len(items)}}


@router.delete("/history", status_code=204)
def delete_user_history(
    user_service: UserService = Depends(get_current_user_service),
) -> None:
    user_service.delete_user_history()
    return
