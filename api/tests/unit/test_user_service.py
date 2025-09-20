import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from zotify_api.database import crud, models
from zotify_api.services import user_service
from zotify_api.schemas import user as user_schemas

@pytest.fixture
def mock_crud(monkeypatch):
    mocks = {
        "get_user_profile": MagicMock(),
        "create_user_profile": MagicMock(),
        "update_user_profile": MagicMock(),
        "get_user_preferences": MagicMock(),
        "create_user_preferences": MagicMock(),
        "update_user_preferences": MagicMock(),
        "get_liked_songs": MagicMock(),
        "add_liked_song": MagicMock(),
        "get_history": MagicMock(),
        "add_history": MagicMock(),
        "delete_history": MagicMock(),
    }
    for func, mock in mocks.items():
        monkeypatch.setattr(crud, func, mock)
    return mocks

def test_get_user_profile(mock_crud, test_db_session: Session):
    user = models.User(id="user1", username="test", hashed_password="pw")
    mock_crud["get_user_profile"].return_value = models.UserProfile(user_id="user1", name="test")
    mock_crud["get_user_preferences"].return_value = models.UserPreferences(user_id="user1", theme="dark", language="en")
    user_service.get_user_profile(db=test_db_session, user=user)

    mock_crud["get_user_profile"].assert_called_once()
    _, kwargs = mock_crud["get_user_profile"].call_args
    assert kwargs["user_id"] == "user1"

    mock_crud["get_user_preferences"].assert_called_once()
    _, kwargs = mock_crud["get_user_preferences"].call_args
    assert kwargs["user_id"] == "user1"

def test_update_user_profile(mock_crud, test_db_session: Session):
    user = models.User(id="user1", username="test", hashed_password="pw")
    profile_data = user_schemas.UserProfileUpdate(name="new_name", email="new_email@test.com")
    profile = models.UserProfile(user_id="user1", name="test")
    mock_crud["get_user_profile"].return_value = profile
    mock_crud["get_user_preferences"].return_value = models.UserPreferences(user_id="user1", theme="dark", language="en")
    mock_crud["update_user_profile"].return_value = models.UserProfile(user_id="user1", name="new_name", email="new_email@test.com")
    user_service.update_user_profile(db=test_db_session, user=user, profile_data=profile_data)
    mock_crud["update_user_profile"].assert_called_once()
    call_args, call_kwargs = mock_crud["update_user_profile"].call_args
    assert call_kwargs['db_profile'] == profile
    assert call_kwargs['name'] == "new_name"
    assert call_kwargs['email'] == "new_email@test.com"


def test_get_user_preferences(mock_crud, test_db_session: Session):
    user = models.User(id="user1", username="test", hashed_password="pw")
    mock_crud["get_user_preferences"].return_value = models.UserPreferences(user_id="user1", theme="dark", language="en")
    user_service.get_user_preferences(db=test_db_session, user=user)
    mock_crud["get_user_preferences"].assert_called_once()
    _, kwargs = mock_crud["get_user_preferences"].call_args
    assert kwargs["user_id"] == "user1"

def test_update_user_preferences(mock_crud, test_db_session: Session):
    user = models.User(id="user1", username="test", hashed_password="pw")
    preferences_data = user_schemas.UserPreferencesUpdate(theme="light", language="fr")
    preferences = models.UserPreferences(user_id="user1", theme="dark", language="en")
    mock_crud["get_user_preferences"].return_value = preferences
    mock_crud["update_user_preferences"].return_value = models.UserPreferences(user_id="user1", theme="light", language="fr")
    user_service.update_user_preferences(db=test_db_session, user=user, preferences_data=preferences_data)
    mock_crud["update_user_preferences"].assert_called_once()
    call_args, call_kwargs = mock_crud["update_user_preferences"].call_args
    assert call_kwargs['db_preferences'] == preferences
    assert call_kwargs['theme'] == "light"
    assert call_kwargs['language'] == "fr"

def test_get_user_liked(mock_crud, test_db_session: Session):
    user = models.User(id="user1", username="test", hashed_password="pw")
    user_service.get_user_liked(db=test_db_session, user=user)
    mock_crud["get_liked_songs"].assert_called_once()
    _, kwargs = mock_crud["get_liked_songs"].call_args
    assert kwargs["user_id"] == "user1"

def test_add_user_liked(mock_crud, test_db_session: Session):
    user = models.User(id="user1", username="test", hashed_password="pw")
    user_service.add_user_liked(db=test_db_session, user=user, track_id="track1")
    mock_crud["add_liked_song"].assert_called_once()
    _, kwargs = mock_crud["add_liked_song"].call_args
    assert kwargs["user"] == user
    assert kwargs["track_id"] == "track1"

def test_get_user_history(mock_crud, test_db_session: Session):
    user = models.User(id="user1", username="test", hashed_password="pw")
    user_service.get_user_history(db=test_db_session, user=user)
    mock_crud["get_history"].assert_called_once()
    _, kwargs = mock_crud["get_history"].call_args
    assert kwargs["user_id"] == "user1"

def test_add_user_history(mock_crud, test_db_session: Session):
    user = models.User(id="user1", username="test", hashed_password="pw")
    user_service.add_user_history(db=test_db_session, user=user, track_id="track1")
    mock_crud["add_history"].assert_called_once()
    _, kwargs = mock_crud["add_history"].call_args
    assert kwargs["user"] == user
    assert kwargs["track_id"] == "track1"

def test_clear_user_history(mock_crud, test_db_session: Session):
    user = models.User(id="user1", username="test", hashed_password="pw")
    user_service.clear_user_history(db=test_db_session, user=user)
    mock_crud["delete_history"].assert_called_once()
    _, kwargs = mock_crud["delete_history"].call_args
    assert kwargs["user_id"] == "user1"
