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
