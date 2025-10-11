# ID: API-076
from typing import Optional

from pydantic import BaseModel


class LogUpdate(BaseModel):
    level: Optional[str] = None
    log_to_file: Optional[bool] = None
    log_file: Optional[str] = None


class LoggingConfigResponse(BaseModel):
    level: str
    log_to_file: bool
    log_file: Optional[str] = None
