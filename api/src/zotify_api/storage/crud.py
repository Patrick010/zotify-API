import json
from typing import List, Dict

STORAGE_FILE = "api/storage/playlists.json"

def get_playlists_db() -> List[Dict]:
    """Reads the playlists from the JSON file."""
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_playlists_db(db: List[Dict]):
    """Saves the playlists to the JSON file."""
    with open(STORAGE_FILE, "w") as f:
        json.dump(db, f, indent=2)
