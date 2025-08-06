import uuid
import httpx
import logging
from typing import List, Dict

log = logging.getLogger(__name__)

webhooks: Dict[str, dict] = {}

def register_hook(payload: dict):
    hook_id = str(uuid.uuid4())
    hook = {"id": hook_id, **payload.model_dump()}
    webhooks[hook_id] = hook
    return hook

def list_hooks():
    return list(webhooks.values())

def unregister_hook(hook_id: str):
    if hook_id in webhooks:
        del webhooks[hook_id]

def fire_event(event: str, data: dict):
    hooks = list_hooks()
    for hook in hooks:
        if event in hook.get("events", []):
            try:
                httpx.post(hook["url"], json={"event": event, "data": data}, timeout=5.0)
            except Exception:
                log.exception("webhook delivery failed")
