from pydantic import BaseModel


class Notification(BaseModel):
    id: str
    user_id: str
    message: str
    read: bool


class NotificationCreate(BaseModel):
    user_id: str
    message: str


class NotificationUpdate(BaseModel):
    read: bool
