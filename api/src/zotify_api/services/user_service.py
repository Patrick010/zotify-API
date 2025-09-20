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
    def __init__(self, username: str, data: Dict[str, Any], storage_file: Path):
        self._username = username
        self._data = data
        self._storage_file = storage_file
        if self._username not in self._data:
            self._data[self._username] = {
                "profile": {"name": self._username, "email": ""},
                "liked": [],
                "history": [],
                "preferences": {"theme": "dark", "language": "en"},
                "notifications": [],
            }

    def _save_data(self) -> None:
        with open(self._storage_file, "w") as f:
            json.dump(self._data, f, indent=4)

    def get_user_profile(self) -> Dict[str, Any]:
        return self._data[self._username]["profile"]

    def update_user_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        log.info(f"Updating user profile for {self._username} with: {profile_data}")
        self._data[self._username]["profile"].update(profile_data)
        self._save_data()
        log.info("User profile updated successfully.")
        return self._data[self._username]["profile"]

    def get_user_preferences(self) -> Dict[str, Any]:
        return self._data[self._username]["preferences"]

    def update_user_preferences(
        self, preferences_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        log.info(f"Updating user preferences for {self._username} with: {preferences_data}")
        self._data[self._username]["preferences"].update(preferences_data)
        self._save_data()
        log.info("User preferences updated successfully.")
        return self._data[self._username]["preferences"]

    def get_user_liked(self) -> List[str]:
        return self._data[self._username]["liked"]

    def sync_user_liked(self) -> Dict[str, Any]:
        # In a real implementation, this would sync with an external service.
        # For now, we just return the current state.
        return {"status": "ok", "synced": len(self._data[self._username]["liked"])}

    def get_user_history(self) -> List[str]:
        return self._data[self._username]["history"]

    def delete_user_history(self) -> None:
        self._data[self._username]["history"].clear()
        self._save_data()

    def get_notifications(self) -> List[Dict[str, Any]]:
        return self._data[self._username]["notifications"]

    def add_notification(self, notification: Dict[str, Any]) -> None:
        self._data[self._username]["notifications"].append(notification)
        self._save_data()

    def mark_notification_as_read(
        self, notification_id: str, read: bool = True
    ) -> None:
        for n in self._data[self._username]["notifications"]:
            if n["id"] == notification_id:
                n["read"] = read
                break
        self._save_data()


def get_user_service(username: str) -> "UserService":
    if not STORAGE_FILE.parent.exists():
        STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not STORAGE_FILE.exists():
        data: Dict[str, Any] = {}
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=4)
    else:
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)

    return UserService(username, data, STORAGE_FILE)
