import json
from typing import List
from uuid import uuid4
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from starlette.responses import Response

from zotify_api.models.playlist import Playlist, PlaylistCreate, TrackRequest
from zotify_api import database

router = APIRouter()

@router.get("/playlist", response_model=List[Playlist], summary="Get all playlists")
async def get_playlists(db: List[dict] = Depends(database.get_db)):
    if not db:
        return [
            {"id": "dummy-playlist-1", "name": "My Dummy Playlist", "tracks": ["track1", "track2"]},
            {"id": "dummy-playlist-2", "name": "Another Dummy Playlist", "tracks": ["track3"]}
        ]
    return db

@router.delete("/playlist", status_code=204, summary="Delete all playlists")
async def delete_all_playlists(db: List[dict] = Depends(database.get_db)):
    db.clear()
    database.save_db(db)
    return Response(status_code=204)

@router.post("/playlist", response_model=Playlist, status_code=201, summary="Create a new playlist")
async def create_playlist(playlist_in: PlaylistCreate, db: List[dict] = Depends(database.get_db)):
    new_playlist = Playlist(id=str(uuid4()), name=playlist_in.name, tracks=[])
    db.append(new_playlist.model_dump())
    database.save_db(db)
    return new_playlist

@router.delete("/playlist/{playlist_id}", status_code=204, summary="Delete a playlist by ID")
async def delete_playlist(playlist_id: str, db: List[dict] = Depends(database.get_db)):
    playlist_to_delete = next((p for p in db if p["id"] == playlist_id), None)
    if not playlist_to_delete:
        raise HTTPException(status_code=404, detail="Playlist not found")

    db_after_delete = [p for p in db if p["id"] != playlist_id]
    database.save_db(db_after_delete)
    return Response(status_code=204)

@router.post("/playlist/{playlist_id}/tracks", response_model=Playlist, summary="Add tracks to a playlist")
async def add_tracks_to_playlist(playlist_id: str, tracks_in: TrackRequest, db: List[dict] = Depends(database.get_db)):
    playlist_to_update = next((p for p in db if p["id"] == playlist_id), None)
    if not playlist_to_update:
        raise HTTPException(status_code=404, detail="Playlist not found")

    # Add only unique tracks
    existing_tracks = set(playlist_to_update["tracks"])
    for track_id in tracks_in.track_ids:
        if track_id not in existing_tracks:
            playlist_to_update["tracks"].append(track_id)
            existing_tracks.add(track_id)

    database.save_db(db)
    return playlist_to_update

@router.delete("/playlist/{playlist_id}/tracks", response_model=Playlist, summary="Remove tracks from a playlist")
async def remove_tracks_from_playlist(playlist_id: str, tracks_in: TrackRequest, db: List[dict] = Depends(database.get_db)):
    playlist_to_update = next((p for p in db if p["id"] == playlist_id), None)
    if not playlist_to_update:
        raise HTTPException(status_code=404, detail="Playlist not found")

    tracks_to_remove = set(tracks_in.track_ids)
    playlist_to_update["tracks"] = [t for t in playlist_to_update["tracks"] if t not in tracks_to_remove]
    database.save_db(db)
    return playlist_to_update

@router.get("/playlist/{playlist_id}/export", summary="Export a playlist")
async def export_playlist(playlist_id: str, format: str = "json", db: List[dict] = Depends(database.get_db)):
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

@router.post("/playlist/import", response_model=Playlist, status_code=201, summary="Import a playlist from a .json or .m3u file")
async def import_playlist(file: UploadFile = File(...), db: List[dict] = Depends(database.get_db)):
    if file.filename.endswith(".json"):
        try:
            contents = await file.read()
            data = json.loads(contents)
            playlist = Playlist(**data)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON format or structure.")
    elif file.filename.endswith(".m3u"):
        try:
            contents = await file.read()
            track_ids = [line.strip() for line in contents.decode("utf-8").splitlines() if line.strip() and not line.startswith("#")]
            playlist_name = file.filename[:-4]
            playlist = Playlist(id=str(uuid4()), name=playlist_name, tracks=track_ids)
        except Exception:
            raise HTTPException(status_code=400, detail="Could not parse M3U file.")
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Only .json and .m3u files are supported.")

    db.append(playlist.model_dump())
    database.save_db(db)
    return playlist
