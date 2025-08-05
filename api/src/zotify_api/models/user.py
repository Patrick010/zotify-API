from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserModel(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    display_name: str | None = None
