import json
from typing import List, Dict
import os

STORAGE_DIR = "api/storage"
STORAGE_FILE = os.path.join(STORAGE_DIR, "playlists.json")

def get_db() -> List[Dict]:
    """Dependency function to get the database."""
    try:
        with open(STORAGE_FILE, "r") as f:
            db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        db = []
    return db

def save_db(db: List[Dict]):
    """Saves the entire database back to the file."""
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with open(STORAGE_FILE, "w") as f:
        json.dump(db, f, indent=2)
