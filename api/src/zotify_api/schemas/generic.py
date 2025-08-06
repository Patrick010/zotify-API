from pydantic import BaseModel
from typing import Any, Generic, TypeVar

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    status: str = "success"
    data: T
