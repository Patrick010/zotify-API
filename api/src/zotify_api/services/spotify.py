from typing import Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import Depends
from zotify_api.services.spoti_client import SpotiClient
from zotify_api.database import crud
from zotify_api.services.deps import get_spoti_client

async def search_spotify(q: str, type: str, limit: int, offset: int, client: SpotiClient) -> tuple[list, int]:
    results = await client.search(q=q, type=type, limit=limit, offset=offset)
    for key in results:
        if 'items' in results[key]:
            return results[key]['items'], results[key].get('total', 0)
    return [], 0

async def get_me(client: SpotiClient) -> Dict[str, Any]:
    return await client.get_current_user()

async def get_spotify_devices(client: SpotiClient) -> List[Dict[str, Any]]:
    return await client.get_devices()

async def get_playlists(limit: int, offset: int, client: SpotiClient) -> Dict[str, Any]:
    return await client.get_current_user_playlists(limit=limit, offset=offset)

async def get_playlist(playlist_id: str, client: SpotiClient) -> Dict[str, Any]:
    return await client.get_playlist(playlist_id)

async def get_playlist_tracks(playlist_id: str, limit: int, offset: int, client: SpotiClient) -> Dict[str, Any]:
    return await client.get_playlist_tracks(playlist_id, limit=limit, offset=offset)

async def create_playlist(user_id: str, name: str, public: bool, collaborative: bool, description: str, client: SpotiClient) -> Dict[str, Any]:
    return await client.create_playlist(user_id, name, public, collaborative, description)

async def update_playlist_details(playlist_id: str, name: str, public: bool, collaborative: bool, description: str, client: SpotiClient) -> None:
    await client.update_playlist_details(playlist_id, name, public, collaborative, description)

async def add_tracks_to_playlist(playlist_id: str, uris: List[str], client: SpotiClient) -> Dict[str, Any]:
    return await client.add_tracks_to_playlist(playlist_id, uris)

async def remove_tracks_from_playlist(playlist_id: str, uris: List[str], client: SpotiClient) -> Dict[str, Any]:
    return await client.remove_tracks_from_playlist(playlist_id, uris)

async def unfollow_playlist(playlist_id: str, client: SpotiClient) -> None:
    await client.unfollow_playlist(playlist_id)

async def sync_playlists(db: Session, client: SpotiClient) -> Dict[str, Any]:
    spotify_playlists = await client.get_all_current_user_playlists()
    crud.clear_all_playlists_and_tracks(db)
    for playlist_data in spotify_playlists:
        playlist_id = playlist_data.get("id")
        playlist_name = playlist_data.get("name")
        if not playlist_id or not playlist_name:
            continue
        track_items = playlist_data.get("tracks", {}).get("items", [])
        track_ids = [item.get("track", {}).get("id") for item in track_items if item.get("track")]
        crud.create_or_update_playlist(
            db=db,
            playlist_id=playlist_id,
            playlist_name=playlist_name,
            track_ids=track_ids,
        )
    return {"status": "success", "message": f"Successfully synced {len(spotify_playlists)} playlists.", "count": len(spotify_playlists)}
