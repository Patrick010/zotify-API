from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field, HttpUrl, constr, model_validator


class BaseSinkConfig(BaseModel):
    """Base configuration for all sinks."""

    # The name must be a valid identifier (no spaces, etc.)
    name: constr(pattern=r"^[a-zA-Z0-9_]+$")
    level: str = "INFO"

    class Config:
        extra = "forbid"


# Specific sink configurations
class ConsoleSinkConfig(BaseSinkConfig):
    """Configuration for a console log sink."""

    type: Literal["console"]


class FileSinkConfig(BaseSinkConfig):
    """Configuration for a file log sink with rotation."""

    type: Literal["file"]
    path: str
    max_bytes: int = 10485760  # 10 MB
    backup_count: int = 5


class WebhookSinkConfig(BaseSinkConfig):
    """Configuration for a webhook log sink."""

    type: Literal["webhook"]
    url: HttpUrl


# A union of all possible sink configurations
# The 'type' field is used by Pydantic to determine which model to use
AnySinkConfig = Annotated[
    Union[ConsoleSinkConfig, FileSinkConfig, WebhookSinkConfig],
    Field(discriminator="type"),
]


# Configuration for a single trigger
class TriggerConfig(BaseModel):
    """Defines a rule for a trigger that can initiate an action."""

    class Config:
        extra = "forbid"

    event: Optional[str] = None
    tag: Optional[str] = None
    action: str
    details: dict = Field(default_factory=dict)

    @model_validator(mode="before")
    def check_event_or_tag(cls, values):
        if values.get("event") is not None and values.get("tag") is not None:
            raise ValueError('A trigger cannot have both an "event" and a "tag".')
        if values.get("event") is None and values.get("tag") is None:
            raise ValueError('A trigger must have either an "event" or a "tag".')
        return values


# Main configuration for the logging section
class LoggingConfig(BaseModel):
    """Defines the overall logging behavior and available sinks."""

    default_level: str = "INFO"
    sinks: List[AnySinkConfig] = Field(default_factory=list)

    class Config:
        extra = "forbid"


# Top-level configuration object for the entire logging framework
class LoggingFrameworkConfig(BaseModel):
    """The root configuration model for the flexible logging framework."""

    logging: LoggingConfig
    triggers: List[TriggerConfig] = Field(default_factory=list)

    class Config:
        extra = "forbid"
