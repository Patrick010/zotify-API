from typing import Any, Dict, List
from sqlalchemy.orm import Session
from zotify_api.database import crud, models
from zotify_api.schemas import user as user_schemas


def get_user_profile(
    db: Session, user: models.User
) -> user_schemas.UserProfileResponse:
    profile = crud.get_user_profile(db, user_id=user.id)
    if not profile:
        profile = crud.create_user_profile(db, user=user, name=user.username)

    preferences = crud.get_user_preferences(db, user_id=user.id)
    if not preferences:
        preferences = crud.create_user_preferences(db, user=user)

    return user_schemas.UserProfileResponse(
        name=profile.name,
        email=profile.email,
        preferences=user_schemas.UserPreferences.model_validate(preferences),
    )


def update_user_profile(
    db: Session, user: models.User, profile_data: user_schemas.UserProfileUpdate
) -> user_schemas.UserProfileResponse:
    profile = crud.get_user_profile(db, user_id=user.id)
    if not profile:
        profile = crud.create_user_profile(db, user=user, name=user.username)

    profile = crud.update_user_profile(
        db, db_profile=profile, name=profile_data.name, email=profile_data.email
    )

    preferences = crud.get_user_preferences(db, user_id=user.id)
    if not preferences:
        preferences = crud.create_user_preferences(db, user=user)

    return user_schemas.UserProfileResponse(
        name=profile.name,
        email=profile.email,
        preferences=user_schemas.UserPreferences.model_validate(preferences),
    )


def get_user_preferences(
    db: Session, user: models.User
) -> user_schemas.UserPreferences:
    preferences = crud.get_user_preferences(db, user_id=user.id)
    if not preferences:
        preferences = crud.create_user_preferences(db, user=user)
    return user_schemas.UserPreferences.model_validate(preferences)


def update_user_preferences(
    db: Session, user: models.User, preferences_data: user_schemas.UserPreferencesUpdate
) -> user_schemas.UserPreferences:
    preferences = crud.get_user_preferences(db, user_id=user.id)
    if not preferences:
        preferences = crud.create_user_preferences(db, user=user)

    updated_preferences = crud.update_user_preferences(
        db,
        db_preferences=preferences,
        theme=preferences_data.theme,
        language=preferences_data.language,
        notifications_enabled=preferences_data.notifications_enabled,
    )
    return user_schemas.UserPreferences.model_validate(updated_preferences)

def get_user_liked(db: Session, user: models.User) -> List[str]:
    liked_songs = crud.get_liked_songs(db, user_id=user.id)
    return [song.track_id for song in liked_songs]

def add_user_liked(db: Session, user: models.User, track_id: str) -> models.LikedSong:
    return crud.add_liked_song(db, user=user, track_id=track_id)

def get_user_history(db: Session, user: models.User) -> List[str]:
    history = crud.get_history(db, user_id=user.id)
    return [item.track_id for item in history]

def add_user_history(db: Session, user: models.User, track_id: str) -> models.History:
    return crud.add_history(db, user=user, track_id=track_id)

def clear_user_history(db: Session, user: models.User) -> int:
    return crud.delete_history(db, user_id=user.id)
