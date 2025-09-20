from typing import Any, Dict

from fastapi import APIRouter, Depends

from zotify_api.database.models import User
from zotify_api.schemas.generic import StandardResponse
from zotify_api.schemas.user import (
    UserPreferences,
    UserProfileResponse,
    UserProfileUpdate,
)
from zotify_api.services import user_service
from zotify_api.services.jwt_service import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile", response_model=StandardResponse[UserProfileResponse])
def get_user_profile(
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    user_data = user_service.get_user(current_user.username)
    if not user_data:
        # This should not happen if the user is authenticated
        return {"data": {}}
    profile = UserProfileResponse(**user_data["profile"], preferences=user_data["preferences"])
    return {"data": profile}


@router.patch("/profile", response_model=StandardResponse[UserProfileResponse])
def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    user_service.update_user(
        current_user.username, {"profile": profile_data.model_dump(exclude_unset=True)}
    )
    user_data = user_service.get_user(current_user.username)
    if not user_data:
        return {"data": {}}
    profile = UserProfileResponse(**user_data["profile"], preferences=user_data["preferences"])
    return {"data": profile}


@router.get("/preferences", response_model=StandardResponse[UserPreferences])
def get_user_preferences(
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    user_data = user_service.get_user(current_user.username)
    if not user_data:
        return {"data": {}}
    return {"data": user_data["preferences"]}


@router.patch("/preferences", response_model=StandardResponse[UserPreferences])
def update_user_preferences(
    preferences_data: UserPreferences,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    user_service.update_user(
        current_user.username, {"preferences": preferences_data.model_dump(exclude_unset=True)}
    )
    user_data = user_service.get_user(current_user.username)
    if not user_data:
        return {"data": {}}
    return {"data": user_data["preferences"]}


@router.get("/liked", response_model=Dict[str, Any])
def get_user_liked(
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    user_data = user_service.get_user(current_user.username)
    if not user_data:
        return {"data": [], "meta": {"total": 0}}
    items = user_data["liked"]
    return {"data": items, "meta": {"total": len(items)}}


@router.get("/history", response_model=Dict[str, Any])
def get_user_history(
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    user_data = user_service.get_user(current_user.username)
    if not user_data:
        return {"data": [], "meta": {"total": 0}}
    items = user_data["history"]
    return {"data": items, "meta": {"total": len(items)}}


@router.delete("/history", status_code=204)
def delete_user_history(
    current_user: User = Depends(get_current_user),
) -> None:
    user_data = user_service.get_user(current_user.username)
    if user_data:
        user_data["history"].clear()
        user_service.update_user(current_user.username, user_data)
    return
