from typing import Any, Dict, List, Literal

from pydantic import BaseModel, Field


class ActionConfig(BaseModel):
    """
    Configuration for a single action to be performed when a trigger matches.
    """
    type: str  # e.g., "log_critical", "webhook"
    details: Dict[str, Any] = Field(default_factory=dict)

class TriggerConfig(BaseModel):
    """
    Configuration for a trigger that maps an exception type to a list of actions.
    """
    exception_type: str
    actions: List[ActionConfig]

class ErrorHandlerConfig(BaseModel):
    """
    Root configuration model for the Generic Error Handler.
    """
    verbosity: Literal["debug", "production"] = "production"
    triggers: List[TriggerConfig] = Field(default_factory=list)
