import json
from typing import List
from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from starlette.responses import Response

from ..models.playlist import Playlist, PlaylistCreate, TrackRequest
from ..storage.crud import get_playlists_db, save_playlists_db

router = APIRouter()

@router.get("/playlists", response_model=List[Playlist], summary="Get all playlists")
async def get_playlists():
    return get_playlists_db()

@router.post("/playlists", response_model=Playlist, status_code=201, summary="Create a new playlist")
async def create_playlist(playlist_in: PlaylistCreate):
    db = get_playlists_db()
    new_playlist = Playlist(id=str(uuid4()), name=playlist_in.name, tracks=[])
    db.append(new_playlist.dict())
    save_playlists_db(db)
    return new_playlist

@router.delete("/playlists/{playlist_id}", status_code=204, summary="Delete a playlist by ID")
async def delete_playlist(playlist_id: str):
    db = get_playlists_db()
    playlist_to_delete = next((p for p in db if p["id"] == playlist_id), None)
    if not playlist_to_delete:
        raise HTTPException(status_code=404, detail="Playlist not found")

    db = [p for p in db if p["id"] != playlist_id]
    save_playlists_db(db)
    return Response(status_code=204)

@router.post("/playlists/{playlist_id}/tracks", response_model=Playlist, summary="Add tracks to a playlist")
async def add_tracks_to_playlist(playlist_id: str, tracks_in: TrackRequest):
    db = get_playlists_db()
    playlist_to_update = next((p for p in db if p["id"] == playlist_id), None)
    if not playlist_to_update:
        raise HTTPException(status_code=404, detail="Playlist not found")

    playlist_to_update["tracks"].extend(tracks_in.track_ids)
    save_playlists_db(db)
    return playlist_to_update

@router.delete("/playlists/{playlist_id}/tracks", response_model=Playlist, summary="Remove tracks from a playlist")
async def remove_tracks_from_playlist(playlist_id: str, tracks_in: TrackRequest):
    db = get_playlists_db()
    playlist_to_update = next((p for p in db if p["id"] == playlist_id), None)
    if not playlist_to_update:
        raise HTTPException(status_code=404, detail="Playlist not found")

    playlist_to_update["tracks"] = [t for t in playlist_to_update["tracks"] if t not in tracks_in.track_ids]
    save_playlists_db(db)
    return playlist_to_update

@router.get("/playlists/{playlist_id}/export", summary="Export a playlist")
async def export_playlist(playlist_id: str, format: str = "json"):
    db = get_playlists_db()
    playlist = next((p for p in db if p["id"] == playlist_id), None)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    if format == "json":
        return Response(content=json.dumps(playlist, indent=2), media_type="application/json", headers={"Content-Disposition": f"attachment; filename={playlist['name']}.json"})
    elif format == "m3u":
        m3u_content = "\n".join(playlist["tracks"])
        return Response(content=m3u_content, media_type="audio/x-m3u", headers={"Content-Disposition": f"attachment; filename={playlist['name']}.m3u"})
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")

@router.post("/playlists/import", response_model=Playlist, status_code=201, summary="Import a playlist from a .json file")
async def import_playlist(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .json files are supported.")

    try:
        contents = await file.read()
        data = json.loads(contents)
        playlist = Playlist(**data)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON format or structure.")

    db = get_playlists_db()
    db.append(playlist.dict())
    save_playlists_db(db)
    return playlist
