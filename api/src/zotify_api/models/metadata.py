from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MetadataUpdate(BaseModel):
    mood: Optional[str] = None
    rating: Optional[int] = None
    source: Optional[str] = None

class MetadataResponse(BaseModel):
    total_tracks: int
    total_playlists: int
    last_updated: datetime
    library_size_mb: float
