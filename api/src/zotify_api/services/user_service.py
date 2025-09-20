"""
User service module.

This module contains the business logic for the user subsystem.
The functions in this module are designed to be called from the API layer.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

log = logging.getLogger(__name__)

STORAGE_FILE = Path(__file__).parent.parent / "storage" / "user_data.json"


def _read_data() -> Dict[str, Any]:
    if not STORAGE_FILE.exists():
        return {"users": {}}
    try:
        with open(STORAGE_FILE, "r") as f:
            data = json.load(f)
            if "users" not in data:
                data["users"] = {}
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return {"users": {}}


def _write_data(data: Dict[str, Any]) -> None:
    if not STORAGE_FILE.parent.exists():
        STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def clear_all_users() -> None:
    _write_data({"users": {}})


def create_user(username: str, user_data: Dict[str, Any]) -> None:
    data = _read_data()
    if username not in data["users"]:
        data["users"][username] = user_data
        _write_data(data)


def get_user(username: str) -> Optional[Dict[str, Any]]:
    data = _read_data()
    return data["users"].get(username)


def update_user(username: str, user_data: Dict[str, Any]) -> bool:
    data = _read_data()
    if username in data["users"]:
        data["users"][username].update(user_data)
        _write_data(data)
        return True
    return False
