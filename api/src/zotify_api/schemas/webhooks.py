from typing import List

from pydantic import BaseModel


class WebhookPayload(BaseModel):
    url: str
    events: List[str]


class Webhook(WebhookPayload):
    id: str


class FirePayload(BaseModel):
    event: str
    data: dict
