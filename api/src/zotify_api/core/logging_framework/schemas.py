from pydantic import BaseModel, Field, FilePath, HttpUrl
from typing import List, Literal, Union

# Base model for common sink properties
from pydantic import constr

class BaseSinkConfig(BaseModel):
    """ Base configuration for all sinks. """
    # The name must be a valid identifier (no spaces, etc.)
    name: constr(pattern=r'^[a-zA-Z0-9_]+$')
    level: str = "INFO"

# Specific sink configurations
class ConsoleSinkConfig(BaseSinkConfig):
    """ Configuration for a console log sink. """
    type: Literal["console"]

class FileSinkConfig(BaseSinkConfig):
    """ Configuration for a file log sink with rotation. """
    type: Literal["file"]
    path: str  # Changed from FilePath to avoid existence check in unit tests
    max_bytes: int = 10485760  # 10 MB
    backup_count: int = 5

class WebhookSinkConfig(BaseSinkConfig):
    """ Configuration for a webhook log sink. """
    type: Literal["webhook"]
    url: HttpUrl

from typing import Annotated

# A union of all possible sink configurations
# The 'type' field is used by Pydantic to determine which model to use
AnySinkConfig = Annotated[
    Union[ConsoleSinkConfig, FileSinkConfig, WebhookSinkConfig],
    Field(discriminator="type")
]

# Configuration for a single trigger
class TriggerConfig(BaseModel):
    """ Defines a rule for a trigger that can initiate an action. """
    event: str
    action: str
    # Future enhancements could include more complex details here
    details: dict = Field(default_factory=dict)

# Main configuration for the logging section
class LoggingConfig(BaseModel):
    """ Defines the overall logging behavior and available sinks. """
    default_level: str = "INFO"
    sinks: List[AnySinkConfig] = Field(default_factory=list)

# Top-level configuration object for the entire logging framework
class LoggingFrameworkConfig(BaseModel):
    """ The root configuration model for the flexible logging framework. """
    logging: LoggingConfig
    triggers: List[TriggerConfig] = Field(default_factory=list)
