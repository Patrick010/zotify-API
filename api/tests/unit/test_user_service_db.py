import pytest
from sqlalchemy.orm import Session

from zotify_api.database import crud
from zotify_api.schemas import user as user_schemas
from zotify_api.services import user_service


@pytest.fixture
def test_user_in_db(test_db_session: Session):
    user_in = user_schemas.UserCreate(username="testuser", password="password123")
    user = crud.create_user(db=test_db_session, user=user_in)
    return user


def test_get_user_profile(test_db_session: Session, test_user_in_db):
    profile = user_service.get_user_profile(db=test_db_session, user=test_user_in_db)
    assert profile.name == "testuser"
    assert profile.email is None


def test_update_user_profile(test_db_session: Session, test_user_in_db):
    profile_update = user_schemas.UserProfileUpdate(name="newname", email="new@email.com")
    profile = user_service.update_user_profile(
        db=test_db_session, user=test_user_in_db, profile_data=profile_update
    )
    assert profile.name == "newname"
    assert profile.email == "new@email.com"


def test_get_user_preferences(test_db_session: Session, test_user_in_db):
    preferences = user_service.get_user_preferences(db=test_db_session, user=test_user_in_db)
    assert preferences.theme == "dark"
    assert preferences.language == "en"


def test_update_user_preferences(test_db_session: Session, test_user_in_db):
    preferences_update = user_schemas.UserPreferencesUpdate(theme="light", language="fr")
    preferences = user_service.update_user_preferences(
        db=test_db_session, user=test_user_in_db, preferences_data=preferences_update
    )
    assert preferences.theme == "light"
    assert preferences.language == "fr"


def test_liked_songs(test_db_session: Session, test_user_in_db):
    liked_songs = user_service.get_user_liked(db=test_db_session, user=test_user_in_db)
    assert liked_songs == []

    user_service.add_user_liked(db=test_db_session, user=test_user_in_db, track_id="track1")
    liked_songs = user_service.get_user_liked(db=test_db_session, user=test_user_in_db)
    assert liked_songs == ["track1"]


def test_history(test_db_session: Session, test_user_in_db):
    history = user_service.get_user_history(db=test_db_session, user=test_user_in_db)
    assert history == []

    user_service.add_user_history(db=test_db_session, user=test_user_in_db, track_id="track1")
    history = user_service.get_user_history(db=test_db_session, user=test_user_in_db)
    assert history == ["track1"]

    user_service.clear_user_history(db=test_db_session, user=test_user_in_db)
    history = user_service.get_user_history(db=test_db_session, user=test_user_in_db)
    assert history == []
