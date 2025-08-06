import uuid
import httpx
import logging
from typing import List, Dict

log = logging.getLogger(__name__)

webhooks: Dict[str, dict] = {}

def register_hook(payload: dict):
    hook_id = str(uuid.uuid4())
    webhooks[hook_id] = payload.copy()
    webhooks[hook_id]["id"] = hook_id
    return webhooks[hook_id]

def list_hooks():
    return list(webhooks.values())

def unregister_hook(hook_id: str):
    if hook_id in webhooks:
        del webhooks[hook_id]

def fire_event(event: str, data: dict):
    for hook in webhooks.values():
        if event in hook["events"]:
            try:
                httpx.post(hook["url"], json={"event": event, "data": data})
            except httpx.RequestError as e:
                log.error(f"Webhook request failed for {hook['url']}: {e}")
