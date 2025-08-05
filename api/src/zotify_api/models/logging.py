from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime

class LogUpdate(BaseModel):
    level: Optional[str] = None
    log_to_file: Optional[bool] = None
    log_file: Optional[str] = None

class LogEntry(BaseModel):
    timestamp: datetime
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]
    message: str

class LoggingResponse(BaseModel):
    data: List[LogEntry]
    meta: dict
