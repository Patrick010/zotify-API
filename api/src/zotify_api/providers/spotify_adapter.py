from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from .base import BaseProvider
from zotify_api.services.spoti_client import SpotiClient
from zotify_api.database import crud

class SpotifyAdapter(BaseProvider):
    """
    Provider adapter for the Spotify music service.
    Implements the BaseProvider interface and uses the SpotiClient to interact with the Spotify API.
    """

    def __init__(self, client: SpotiClient, db: Session):
        self.client = client
        self.db = db

    async def search(self, q: str, type: str, limit: int, offset: int) -> Tuple[List[Dict[str, Any]], int]:
        """ Search for tracks, albums, or artists on Spotify. """
        results = await self.client.search(q=q, type=type, limit=limit, offset=offset)
        for key in results:
            if 'items' in results[key]:
                return results[key]['items'], results[key].get('total', 0)
        return [], 0

    async def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """ Get a single playlist from Spotify. """
        return await self.client.get_playlist(playlist_id)

    async def get_playlist_tracks(self, playlist_id: str, limit: int, offset: int) -> Dict[str, Any]:
        """ Get the tracks in a playlist from Spotify. """
        return await self.client.get_playlist_tracks(playlist_id, limit=limit, offset=offset)

    async def sync_playlists(self) -> Dict[str, Any]:
        """ Fetches all of the user's playlists from Spotify and saves them to the database. """
        spotify_playlists = await self.client.get_all_current_user_playlists()
        crud.clear_all_playlists_and_tracks(self.db)
        for playlist_data in spotify_playlists:
            playlist_id = playlist_data.get("id")
            playlist_name = playlist_data.get("name")
            if not playlist_id or not playlist_name:
                continue
            track_items = playlist_data.get("tracks", {}).get("items", [])
            track_ids = [item.get("track", {}).get("id") for item in track_items if item.get("track")]
            crud.create_or_update_playlist(
                db=self.db,
                playlist_id=playlist_id,
                playlist_name=playlist_name,
                track_ids=track_ids,
            )
        return {"status": "success", "message": f"Successfully synced {len(spotify_playlists)} playlists.", "count": len(spotify_playlists)}

    # Other methods from the spotify service can be moved here as well,
    # and added to the BaseProvider interface if they are to be generic.
    # For now, we will keep the adapter focused on the methods defined in the interface.
