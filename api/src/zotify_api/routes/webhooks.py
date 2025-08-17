from fastapi import APIRouter, Depends, BackgroundTasks
from zotify_api.services.auth import require_admin_api_key
import zotify_api.services.webhooks as webhooks_service
from zotify_api.schemas.webhooks import Webhook, WebhookPayload, FirePayload
from zotify_api.schemas.generic import StandardResponse
from typing import List, Dict, Any

router = APIRouter(prefix="/webhooks", tags=["webhooks"], dependencies=[Depends(require_admin_api_key)])

@router.post("/register", status_code=201, response_model=StandardResponse[Webhook])
def register_webhook(payload: WebhookPayload):
    hook = webhooks_service.register_hook(payload)
    return {"data": hook}

@router.get("", status_code=200, response_model=Dict[str, Any])
def list_webhooks():
    hooks = webhooks_service.list_hooks()
    return {"data": hooks, "meta": {"total": len(hooks)}}

@router.delete("/{hook_id}", status_code=204)
def unregister_webhook(hook_id: str):
    webhooks_service.unregister_hook(hook_id)
    return {}

@router.post("/fire", status_code=202)
def fire_webhook(payload: FirePayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(webhooks_service.fire_event, payload.event, payload.data)
    return {"status": "success", "message": "Webhook event fired."}
