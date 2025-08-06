import pytest
from zotify_api.services.user_service import UserService

@pytest.fixture
def user_data():
    return {
        "user_profile": {"name": "Test User", "email": "test@example.com"},
        "user_liked": ["track1", "track2"],
        "user_history": ["track3", "track4"]
    }

def test_get_user_profile(user_data):
    service = UserService(**user_data)
    profile = service.get_user_profile()
    assert profile == user_data["user_profile"]

def test_get_user_liked(user_data):
    service = UserService(**user_data)
    liked = service.get_user_liked()
    assert liked == user_data["user_liked"]

def test_sync_user_liked(user_data):
    service = UserService(**user_data)
    result = service.sync_user_liked()
    assert result["status"] == "ok"
    assert result["synced"] == 2

def test_get_user_history(user_data):
    service = UserService(**user_data)
    history = service.get_user_history()
    assert history == user_data["user_history"]

def test_delete_user_history(user_data):
    service = UserService(**user_data)
    service.delete_user_history()
    assert service.get_user_history() == []
