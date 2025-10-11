# ID: API-104
import logging
import uuid
from typing import Any, Dict, List

import httpx
from pydantic import BaseModel

log = logging.getLogger(__name__)

webhooks: Dict[str, Dict[str, Any]] = {}


def register_hook(payload: BaseModel) -> Dict[str, Any]:
    hook_id = str(uuid.uuid4())
    hook = {"id": hook_id, **payload.model_dump()}
    webhooks[hook_id] = hook
    return hook


def list_hooks() -> List[Dict[str, Any]]:
    return list(webhooks.values())


def unregister_hook(hook_id: str) -> None:
    if hook_id in webhooks:
        del webhooks[hook_id]


def fire_event(event: str, data: Dict[str, Any]) -> None:
    hooks = list_hooks()
    for hook in hooks:
        if event in hook.get("events", []):
            try:
                httpx.post(
                    hook["url"], json={"event": event, "data": data}, timeout=5.0
                )
            except Exception:
                log.exception("webhook delivery failed")
