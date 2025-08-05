from pydantic import BaseModel, ConfigDict
from typing import List

class SystemInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str
    free_space: str
    total_space: str
    logs: List[str]
