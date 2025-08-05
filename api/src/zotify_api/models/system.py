from pydantic import BaseModel, ConfigDict, Field
from typing import List

class SystemInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str = Field(..., min_length=3, max_length=50)
    free_space: str = Field(..., pattern=r"^\d+GB$")
    total_space: str = Field(..., pattern=r"^\d+GB$")
    logs: List[str] = []
