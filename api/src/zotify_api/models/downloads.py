from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class DownloadStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class DownloadItem(BaseModel):
    id: UUID
    filename: str
    status: DownloadStatus
    progress: float = Field(..., ge=0.0, le=100.0)
    started_at: datetime
    finished_at: Optional[datetime] = None

class DownloadsResponseMeta(BaseModel):
    total: int
    limit: int
    offset: int

class DownloadsResponse(BaseModel):
    data: List[DownloadItem]
    meta: DownloadsResponseMeta

class RetryRequest(BaseModel):
    track_ids: List[str]
