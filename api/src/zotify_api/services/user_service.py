"""
User service module.

This module contains the business logic for the user subsystem.
The functions in this module are designed to be called from the API layer.
"""
from typing import Dict, Any, List
import json
from pathlib import Path
import logging

log = logging.getLogger(__name__)

STORAGE_FILE = Path(__file__).parent.parent / "storage" / "user_data.json"

class UserService:
    def __init__(
        self,
        user_profile: Dict[str, Any],
        user_liked: List[str],
        user_history: List[str],
        user_preferences: Dict[str, Any],
    ):
        self._user_profile = user_profile
        self._user_liked = user_liked
        self._user_history = user_history
        self._user_preferences = user_preferences

    def _save_data(self):
        data = {
            "profile": self._user_profile,
            "liked": self._user_liked,
            "history": self._user_history,
            "preferences": self._user_preferences,
        }
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def get_user_profile(self) -> Dict[str, Any]:
        return self._user_profile

    def update_user_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        log.info(f"Updating user profile with: {profile_data}")
        self._user_profile.update(profile_data)
        self._save_data()
        log.info("User profile updated successfully.")
        return self._user_profile

    def get_user_preferences(self) -> Dict[str, Any]:
        return self._user_preferences

    def update_user_preferences(self, preferences_data: Dict[str, Any]) -> Dict[str, Any]:
        log.info(f"Updating user preferences with: {preferences_data}")
        self._user_preferences.update(preferences_data)
        self._save_data()
        log.info("User preferences updated successfully.")
        return self._user_preferences

    def get_user_liked(self) -> List[str]:
        return self._user_liked

    def sync_user_liked(self) -> Dict[str, Any]:
        # In a real implementation, this would sync with an external service.
        # For now, we just return the current state.
        return {"status": "ok", "synced": len(self._user_liked)}

    def get_user_history(self) -> List[str]:
        return self._user_history

    def delete_user_history(self) -> None:
        self._user_history.clear()
        self._save_data()

def get_user_service():
    if not STORAGE_FILE.exists():
        default_data = {
            "profile": {"name": "Test User", "email": "test@example.com"},
            "liked": ["track1", "track2"],
            "history": ["track3", "track4"],
            "preferences": {"theme": "dark", "language": "en"},
        }
        with open(STORAGE_FILE, "w") as f:
            json.dump(default_data, f, indent=4)
        return UserService(**default_data)
    else:
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)
        return UserService(
            user_profile=data.get("profile", {}),
            user_liked=data.get("liked", []),
            user_history=data.get("history", []),
            user_preferences=data.get("preferences", {}),
        )
