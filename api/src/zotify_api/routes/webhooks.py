from typing import Any, Dict

from fastapi import APIRouter, BackgroundTasks, Depends

import zotify_api.services.webhooks as webhooks_service
from zotify_api.schemas.generic import StandardResponse
from zotify_api.schemas.webhooks import FirePayload, Webhook, WebhookPayload
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(
    prefix="/webhooks", tags=["webhooks"], dependencies=[Depends(require_admin_api_key)]
)


@router.post("/register", status_code=201, response_model=StandardResponse[Webhook])
def register_webhook(payload: WebhookPayload) -> Dict[str, Any]:
    hook = webhooks_service.register_hook(payload)
    return {"data": hook}


@router.get("", status_code=200, response_model=Dict[str, Any])
def list_webhooks() -> Dict[str, Any]:
    hooks = webhooks_service.list_hooks()
    return {"data": hooks, "meta": {"total": len(hooks)}}


@router.delete("/{hook_id}", status_code=204)
def unregister_webhook(hook_id: str) -> Dict[str, Any]:
    webhooks_service.unregister_hook(hook_id)
    return {}


@router.post("/fire", status_code=202)
def fire_webhook(
    payload: FirePayload, background_tasks: BackgroundTasks
) -> Dict[str, str]:
    background_tasks.add_task(webhooks_service.fire_event, payload.event, payload.data)
    return {"status": "success", "message": "Webhook event fired."}
