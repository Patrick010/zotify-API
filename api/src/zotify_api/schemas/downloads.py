from pydantic import BaseModel
from typing import List, Dict

class RetryRequest(BaseModel):
    track_ids: List[str]

class DownloadStatusResponse(BaseModel):
    in_progress: List[str]
    failed: Dict[str, str]
    completed: List[str]
