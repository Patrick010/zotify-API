from pydantic import BaseModel, Field
from typing import List, Dict

class RetryRequest(BaseModel):
    track_ids: List[str] = Field(..., description="A list of track IDs to retry.")

class DownloadStatusResponse(BaseModel):
    in_progress: List[str] = Field(..., description="A list of tracks currently being downloaded.")
    failed: Dict[str, str] = Field(..., description="A dictionary of failed downloads, with the track ID as the key and the error message as the value.")
    completed: List[str] = Field(..., description="A list of completed downloads.")
