from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from uuid import uuid4

app = FastAPI(
    title="Zotify API - Search and Download Core",
    version="0.2.0",
    description="Search and download endpoints for Zotify external API"
)

class SearchResult(BaseModel):
    id: str
    type: Literal["track", "album", "playlist"]
    title: str
    artist: str

class SearchResponse(BaseModel):
    results: List[SearchResult]
    page: int
    page_size: int
    total: int

@app.get("/search", response_model=SearchResponse, summary="Search for content")
async def search(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Simulated search response for tracks, albums, or playlists.
    """
    dummy_result = SearchResult(
        id="spotify:track:dummy",
        type="track",
        title=f"Fake Track for '{q}'",
        artist="Test Artist"
    )
    return SearchResponse(
        results=[dummy_result] * page_size,
        page=page,
        page_size=page_size,
        total=200
    )

class DownloadRequest(BaseModel):
    id: str = Field(..., description="Spotify URI of the content to download")
    embed_metadata: Optional[bool] = False
    embed_coverart: Optional[bool] = False
    output_dir: Optional[str] = None

class DownloadResponse(BaseModel):
    task_id: str
    message: str

@app.post("/download/{target}", response_model=DownloadResponse, summary="Download Spotify content")
async def download_content(target: Literal["track", "album", "playlist"], req: DownloadRequest):
    """
    Stubbed download endpoint. Accepts track, album, or playlist IDs.
    """
    if not req.id.startswith("spotify:"):
        raise HTTPException(status_code=400, detail="Invalid Spotify ID format")

    return DownloadResponse(
        task_id=str(uuid4()),
        message=f"Accepted download task for {target}"
    )
