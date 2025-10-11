# ID: API-070
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from zotify_api.database import models
from zotify_api.database.session import get_db
from zotify_api.schemas import user as user_schemas
from zotify_api.services import user_service
from zotify_api.services.jwt_service import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile", response_model=user_schemas.UserProfileResponse)
def get_user_profile(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    return user_service.get_user_profile(db, user=current_user)


@router.patch("/profile", response_model=user_schemas.UserProfileResponse)
def update_user_profile(
    profile_data: user_schemas.UserProfileUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    return user_service.update_user_profile(db, user=current_user, profile_data=profile_data)


@router.get("/preferences", response_model=user_schemas.UserPreferences)
def get_user_preferences(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    return user_service.get_user_preferences(db, user=current_user)


@router.patch("/preferences", response_model=user_schemas.UserPreferences)
def update_user_preferences(
    preferences_data: user_schemas.UserPreferencesUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    return user_service.update_user_preferences(
        db, user=current_user, preferences_data=preferences_data
    )


@router.get("/liked", response_model=List[str])
def get_user_liked(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    return user_service.get_user_liked(db, user=current_user)


@router.post("/liked/{track_id}", response_model=user_schemas.LikedSong)
def add_user_liked(
    track_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    return user_service.add_user_liked(db, user=current_user, track_id=track_id)


@router.get("/history", response_model=List[str])
def get_user_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    return user_service.get_user_history(db, user=current_user)


@router.post("/history/{track_id}", response_model=user_schemas.History)
def add_user_history(
    track_id: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    return user_service.add_user_history(db, user=current_user, track_id=track_id)


@router.delete("/history", status_code=204)
def delete_user_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    user_service.clear_user_history(db, user=current_user)
    return
