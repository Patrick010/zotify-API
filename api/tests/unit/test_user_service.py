from typing import Any, Dict
import pytest
from zotify_api.services.user_service import UserService

@pytest.fixture
def user_data() -> Dict[str, Any]:
    """Provides a dictionary with mock data for multiple users."""
    return {
        "testuser1": {
            "profile": {"name": "Test User 1", "email": "test1@example.com"},
            "liked": ["track1", "track2"],
            "history": ["track3", "track4"],
            "preferences": {"theme": "dark", "language": "en"},
            "notifications": [],
        },
        "testuser2": {
            "profile": {"name": "Test User 2", "email": "test2@example.com"},
            "liked": ["trackA", "trackB"],
            "history": ["trackC", "trackD"],
            "preferences": {"theme": "light", "language": "fr"},
            "notifications": [],
        },
    }

def test_get_user_profile(user_data: Dict[str, Any]) -> None:
    """Tests that the profile for a specific user is correctly fetched."""
    service = UserService(username="testuser1", data=user_data, storage_file=None)
    profile = service.get_user_profile()
    assert profile == user_data["testuser1"]["profile"]

    service_user2 = UserService(username="testuser2", data=user_data, storage_file=None)
    profile_user2 = service_user2.get_user_profile()
    assert profile_user2 == user_data["testuser2"]["profile"]

def test_update_user_profile(user_data: Dict[str, Any]) -> None:
    """Tests that updating a user's profile only affects that user."""
    service = UserService(username="testuser1", data=user_data, storage_file=None)
    update_data = {"name": "New Name"}
    service.update_user_profile(update_data)

    # Verify testuser1 was updated
    assert service.get_user_profile()["name"] == "New Name"

    # Verify testuser2 was not affected
    service_user2 = UserService(username="testuser2", data=user_data, storage_file=None)
    assert service_user2.get_user_profile()["name"] == "Test User 2"

def test_get_user_liked(user_data: Dict[str, Any]) -> None:
    """Tests fetching liked tracks for a specific user."""
    service = UserService(username="testuser1", data=user_data, storage_file=None)
    liked = service.get_user_liked()
    assert liked == user_data["testuser1"]["liked"]

def test_get_user_history(user_data: Dict[str, Any]) -> None:
    """Tests fetching history for a specific user."""
    service = UserService(username="testuser1", data=user_data, storage_file=None)
    history = service.get_user_history()
    assert history == user_data["testuser1"]["history"]

def test_delete_user_history(user_data: Dict[str, Any]) -> None:
    """Tests that deleting history only affects the specific user."""
    service = UserService(username="testuser1", data=user_data, storage_file=None)
    service.delete_user_history()

    # Verify testuser1's history is empty
    assert service.get_user_history() == []

    # Verify testuser2's history is not affected
    service_user2 = UserService(username="testuser2", data=user_data, storage_file=None)
    assert service_user2.get_user_history() == ["trackC", "trackD"]

def test_get_user_preferences(user_data: Dict[str, Any]) -> None:
    """Tests fetching preferences for a specific user."""
    service = UserService(username="testuser1", data=user_data, storage_file=None)
    preferences = service.get_user_preferences()
    assert preferences == user_data["testuser1"]["preferences"]

def test_update_user_preferences(user_data: Dict[str, Any]) -> None:
    """Tests that updating preferences only affects the specific user."""
    service = UserService(username="testuser1", data=user_data, storage_file=None)
    update_data = {"theme": "blue"}
    service.update_user_preferences(update_data)

    # Verify testuser1 was updated
    assert service.get_user_preferences()["theme"] == "blue"

    # Verify testuser2 was not affected
    service_user2 = UserService(username="testuser2", data=user_data, storage_file=None)
    assert service_user2.get_user_preferences()["theme"] == "light"

def test_new_user_creation() -> None:
    """Tests that a new user is created with default data if not present."""
    data = {}
    service = UserService(username="newuser", data=data, storage_file=None)
    profile = service.get_user_profile()
    assert profile["name"] == "newuser"
    assert "email" in profile
    assert service.get_user_liked() == []
    assert service.get_user_history() == []
    assert service.get_user_preferences() == {"theme": "dark", "language": "en"}
