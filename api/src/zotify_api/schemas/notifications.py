# ID: API-079
from pydantic import BaseModel


class Notification(BaseModel):
    id: int
    user_id: str
    message: str
    read: bool


class NotificationCreate(BaseModel):
    message: str


class NotificationUpdate(BaseModel):
    read: bool
