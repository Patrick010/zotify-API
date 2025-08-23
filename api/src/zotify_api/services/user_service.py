"""
User service module.

This module contains the business logic for the user subsystem.
The functions in this module are designed to be called from the API layer.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, cast

log = logging.getLogger(__name__)

STORAGE_FILE = Path(__file__).parent.parent / "storage" / "user_data.json"


class UserService:
    def __init__(
        self,
        user_profile: Dict[str, Any],
        user_liked: List[str],
        user_history: List[str],
        user_preferences: Dict[str, Any],
        notifications: List[Dict[str, Any]],
        storage_file: Path | None = None,
    ):
        self._user_profile = user_profile
        self._user_liked = user_liked
        self._user_history = user_history
        self._user_preferences = user_preferences
        self._notifications = notifications
        self._storage_file = storage_file

    def _save_data(self) -> None:
        if self._storage_file:
            data = {
                "profile": self._user_profile,
                "liked": self._user_liked,
                "history": self._user_history,
                "preferences": self._user_preferences,
                "notifications": self._notifications,
            }
            with open(self._storage_file, "w") as f:
                json.dump(data, f, indent=4)

    def get_user_profile(self) -> Dict[str, Any]:
        return {**self._user_profile, "preferences": self._user_preferences}

    def update_user_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        log.info(f"Updating user profile with: {profile_data}")
        self._user_profile.update(profile_data)
        self._save_data()
        log.info("User profile updated successfully.")
        return {**self._user_profile, "preferences": self._user_preferences}

    def get_user_preferences(self) -> Dict[str, Any]:
        return self._user_preferences

    def update_user_preferences(
        self, preferences_data: Dict[str, Any]
    ) -> Dict[str, Any]:
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

    def get_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        return [n for n in self._notifications if n["user_id"] == user_id]

    def add_notification(self, notification: Dict[str, Any]) -> None:
        self._notifications.append(notification)
        self._save_data()

    def mark_notification_as_read(
        self, notification_id: str, read: bool = True
    ) -> None:
        for n in self._notifications:
            if n["id"] == notification_id:
                n["read"] = read
                break
        self._save_data()


def get_user_service() -> "UserService":
    if not STORAGE_FILE.parent.exists():
        STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not STORAGE_FILE.exists():
        default_data: Dict[str, Any] = {
            "profile": {"name": "Test User", "email": "test@example.com"},
            "liked": ["track1", "track2"],
            "history": ["track3", "track4"],
            "preferences": {"theme": "dark", "language": "en"},
            "notifications": [],
        }
        with open(STORAGE_FILE, "w") as f:
            json.dump(default_data, f, indent=4)
        return UserService(
            user_profile=cast(Dict[str, Any], default_data["profile"]),
            user_liked=cast(List[str], default_data["liked"]),
            user_history=cast(List[str], default_data["history"]),
            user_preferences=cast(Dict[str, Any], default_data["preferences"]),
            notifications=cast(List[Dict[str, Any]], default_data["notifications"]),
            storage_file=STORAGE_FILE,
        )
    else:
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)
        return UserService(
            user_profile=cast(Dict[str, Any], data.get("profile", {})),
            user_liked=cast(List[str], data.get("liked", [])),
            user_history=cast(List[str], data.get("history", [])),
            user_preferences=cast(Dict[str, Any], data.get("preferences", {})),
            notifications=cast(List[Dict[str, Any]], data.get("notifications", [])),
            storage_file=STORAGE_FILE,
        )
