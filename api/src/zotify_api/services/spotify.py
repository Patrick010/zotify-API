from typing import Dict, Any
from zotify_api.services.spoti_client import SpotiClient


async def search_spotify(q: str, type: str, limit: int, offset: int) -> tuple[list, int]:
    """
    Performs a search on Spotify using the SpotiClient.
    """
    client = SpotiClient()
    try:
        results = await client.search(q=q, type=type, limit=limit, offset=offset)
        # The search endpoint returns a dictionary with keys like 'tracks', 'artists', etc.
        # Each of these contains a paging object. We need to extract the items.
        # For simplicity, we'll just return the items from the first key found.
        for key in results:
            if 'items' in results[key]:
                return results[key]['items'], results[key].get('total', 0)
        return [], 0
    finally:
        await client.close()


from typing import Dict, Any, List

async def get_me() -> Dict[str, Any]:
    """
    Retrieves the current user's profile from Spotify.
    """
    client = SpotiClient()
    try:
        user_profile = await client.get_current_user()
        return user_profile
    finally:
        await client.close()


async def get_spotify_devices() -> List[Dict[str, Any]]:
    """
    Retrieves the list of available playback devices from Spotify.
    """
    client = SpotiClient()
    try:
        devices = await client.get_devices()
        return devices
    finally:
        await client.close()


async def get_playlists(limit: int, offset: int) -> Dict[str, Any]:
    client = SpotiClient()
    try:
        return await client.get_current_user_playlists(limit=limit, offset=offset)
    finally:
        await client.close()

async def get_playlist(playlist_id: str) -> Dict[str, Any]:
    client = SpotiClient()
    try:
        return await client.get_playlist(playlist_id)
    finally:
        await client.close()

async def get_playlist_tracks(playlist_id: str, limit: int, offset: int) -> Dict[str, Any]:
    client = SpotiClient()
    try:
        return await client.get_playlist_tracks(playlist_id, limit=limit, offset=offset)
    finally:
        await client.close()

async def create_playlist(user_id: str, name: str, public: bool, collaborative: bool, description: str) -> Dict[str, Any]:
    client = SpotiClient()
    try:
        return await client.create_playlist(user_id, name, public, collaborative, description)
    finally:
        await client.close()

async def update_playlist_details(playlist_id: str, name: str, public: bool, collaborative: bool, description: str) -> None:
    client = SpotiClient()
    try:
        await client.update_playlist_details(playlist_id, name, public, collaborative, description)
    finally:
        await client.close()

async def add_tracks_to_playlist(playlist_id: str, uris: List[str]) -> Dict[str, Any]:
    client = SpotiClient()
    try:
        return await client.add_tracks_to_playlist(playlist_id, uris)
    finally:
        await client.close()

async def remove_tracks_from_playlist(playlist_id: str, uris: List[str]) -> Dict[str, Any]:
    client = SpotiClient()
    try:
        return await client.remove_tracks_from_playlist(playlist_id, uris)
    finally:
        await client.close()

import json
from pathlib import Path

async def unfollow_playlist(playlist_id: str) -> None:
    client = SpotiClient()
    try:
        await client.unfollow_playlist(playlist_id)
    finally:
        await client.close()

async def sync_playlists() -> Dict[str, Any]:
    """
    Fetches all of the user's playlists from Spotify and saves them to a local JSON file.
    """
    client = SpotiClient()
    try:
        playlists = await client.get_all_current_user_playlists()

        # Define the storage path and save the playlists
        storage_path = Path("api/api/storage/playlists.json")
        storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(storage_path, "w") as f:
            json.dump(playlists, f, indent=4)

        return {"status": "success", "message": f"Successfully synced {len(playlists)} playlists.", "count": len(playlists)}
    finally:
        await client.close()
