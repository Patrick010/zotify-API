from pydantic import BaseModel
from typing import List

class WebhookPayload(BaseModel):
    url: str
    events: List[str]

class Webhook(WebhookPayload):
    id: str

class FirePayload(BaseModel):
    event: str
    data: dict
