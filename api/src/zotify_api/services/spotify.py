from typing import Dict, Any
from zotify_api.services.spotify_client import SpotifyClient


def search_spotify(q: str, type: str, limit: int, offset: int):
    # TODO: Implement with SpotifyClient
    return [], 0


async def get_me() -> Dict[str, Any]:
    """
    Retrieves the current user's profile from Spotify.
    """
    client = SpotifyClient()
    try:
        user_profile = await client.get_current_user()
        return user_profile
    finally:
        await client.close()
