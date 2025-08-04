from pydantic import BaseModel
from typing import List

class RetryRequest(BaseModel):
    track_ids: List[str]
