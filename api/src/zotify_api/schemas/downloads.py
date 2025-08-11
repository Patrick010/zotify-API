from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime
import uuid

class DownloadJobStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class DownloadJob(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    track_id: str
    status: DownloadJobStatus = DownloadJobStatus.PENDING
    progress: Optional[float] = None # JULES-NOTE: Placeholder for future progress reporting (e.g., 0.0 to 1.0).
    created_at: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None

class DownloadQueueStatus(BaseModel):
    total_jobs: int
    pending: int
    completed: int
    failed: int
    jobs: List[DownloadJob]
