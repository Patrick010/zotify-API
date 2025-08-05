from pydantic import BaseModel
from typing import List

class Stub(BaseModel):
    id: int
    name: str
    description: str

class StubsResponse(BaseModel):
    data: List[Stub]
