from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MetadataResponse(BaseModel):
    total_tracks: int
    total_playlists: int
    last_updated: Optional[datetime]
    library_size_mb: float
    warning: Optional[str] = None
