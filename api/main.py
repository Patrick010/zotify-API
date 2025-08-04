"""
Zotify API - Phase 1: Core Metadata Endpoint Stubs

To run this API server locally:
1. Install dependencies:
   pip install fastapi uvicorn
2. Start server:
   uvicorn main:app --reload --host 0.0.0.0 --port 8080
3. Access docs at:
   http://<your-ip>:8080/docs

⚠️ WARNING:
Do NOT hardcode 127.0.0.1 anywhere.
Always use --host 0.0.0.0 for dev so the API is reachable externally.
"""

from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Zotify API - Metadata Endpoints",
    version="0.1.0",
    description="Static metadata endpoints for tracks, albums, and artists"
)

# --- Pydantic Response Models ---

class TrackMetadata(BaseModel):
    id: str
    title: str
    artist: str
    album: str
    duration_sec: int

class AlbumMetadata(BaseModel):
    id: str
    title: str
    artist: str
    track_count: int

class ArtistMetadata(BaseModel):
    id: str
    name: str
    album_count: int

# --- Endpoints ---

@app.get("/tracks/{track_id}", response_model=TrackMetadata, summary="Get metadata for a track")
async def get_track(track_id: str = Path(..., min_length=3, description="Unique track ID")):
    return TrackMetadata(
        id=track_id,
        title="Static Track",
        artist="Sample Artist",
        album="Demo Album",
        duration_sec=215
    )

@app.get("/albums/{album_id}", response_model=AlbumMetadata, summary="Get metadata for an album")
async def get_album(album_id: str = Path(..., min_length=3, description="Unique album ID")):
    return AlbumMetadata(
        id=album_id,
        title="Static Album",
        artist="Sample Artist",
        track_count=10
    )

@app.get("/artists/{artist_id}", response_model=ArtistMetadata, summary="Get metadata for an artist")
async def get_artist(artist_id: str = Path(..., min_length=3, description="Unique artist ID")):
    return ArtistMetadata(
        id=artist_id,
        name="Sample Artist",
        album_count=3
    )
