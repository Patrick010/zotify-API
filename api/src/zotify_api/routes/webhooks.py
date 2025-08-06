from fastapi import APIRouter, Depends, BackgroundTasks
from zotify_api.services.auth import require_admin_api_key
import zotify_api.services.webhooks as webhooks_service
from pydantic import BaseModel
from typing import List

class WebhookPayload(BaseModel):
    url: str
    events: List[str]

class FirePayload(BaseModel):
    event: str
    data: dict

router = APIRouter(prefix="/webhooks", dependencies=[Depends(require_admin_api_key)])

@router.post("/register", status_code=201)
def register_webhook(payload: WebhookPayload):
    return webhooks_service.register_hook(payload)

@router.get("", status_code=200)
def list_webhooks():
    return webhooks_service.list_hooks()

@router.delete("/{hook_id}", status_code=204)
def unregister_webhook(hook_id: str):
    webhooks_service.unregister_hook(hook_id)

@router.post("/fire")
def fire_webhook(payload: FirePayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(webhooks_service.fire_event, payload.event, payload.data)
    return {"status": "ok"}
