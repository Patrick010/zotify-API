# tests/test_user_service.py

import pytest
from api.src.zotify_api.services import user_service

@pytest.fixture(autouse=True)
def clear_users():
    """
    Clear in-memory or test DB users before each test.
    Adjust if using database integration.
    """
    user_service.clear_all_users()
    yield
    user_service.clear_all_users()

def test_get_user_existing():
    username = "alice"
    user_service.create_user(username, {"bio": "Test bio"})
    user_data = user_service.get_user(username)
    assert user_data is not None
    assert user_data["bio"] == "Test bio"

def test_get_user_nonexistent():
    user_data = user_service.get_user("ghost")
    assert user_data is None

def test_update_user_existing():
    username = "bob"
    user_service.create_user(username, {"bio": "Old bio"})
    updated = user_service.update_user(username, {"bio": "New bio"})
    user_data = user_service.get_user(username)
    assert updated is True
    assert user_data["bio"] == "New bio"

def test_update_user_nonexistent():
    updated = user_service.update_user("ghost", {"bio": "Anything"})
    assert updated is False

def test_multiple_users_independent():
    user_service.create_user("alice", {"bio": "Alice bio"})
    user_service.create_user("bob", {"bio": "Bob bio"})
    alice_data = user_service.get_user("alice")
    bob_data = user_service.get_user("bob")
    assert alice_data["bio"] == "Alice bio"
    assert bob_data["bio"] == "Bob bio"
