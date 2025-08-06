"""
User service module.

This module contains the business logic for the user subsystem.
The functions in this module are designed to be called from the API layer.
"""
from typing import Dict, Any, List

class UserService:
    def __init__(self, user_profile: Dict[str, Any], user_liked: List[str], user_history: List[str]):
        self._user_profile = user_profile
        self._user_liked = user_liked
        self._user_history = user_history

    def get_user_profile(self) -> Dict[str, Any]:
        return self._user_profile

    def get_user_liked(self) -> List[str]:
        return self._user_liked

    def sync_user_liked(self) -> Dict[str, Any]:
        return {"status": "ok", "synced": len(self._user_liked)}

    def get_user_history(self) -> List[str]:
        return self._user_history

    def delete_user_history(self) -> None:
        self._user_history.clear()

def get_user_service():
    # This is a placeholder for a real implementation that would get the user data from a persistent storage.
    user_profile = {"name": "Test User", "email": "test@example.com"}
    user_liked = ["track1", "track2"]
    user_history = ["track3", "track4"]
    return UserService(user_profile, user_liked, user_history)
