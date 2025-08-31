import logging as py_logging
import os
import time
from typing import Any, Dict, Optional, cast

import yaml
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import ValidationError

from zotify_api.config import settings
from zotify_api.database.models import Base
from zotify_api.database.session import engine
from zotify_api.routes import (
    auth,
    cache,
    config,
    downloads,
    network,
    notifications,
    playlists,
    search,
    sync,
    system,
    tracks,
    user,
    webhooks,
)
from zotify_api.services.auth import require_admin_api_key

from .core.error_handler import (
    ErrorHandlerConfig,
    initialize_error_handler,
    register_fastapi_hooks,
    register_system_hooks,
)
from .core.logging_framework import log_event
from .core.logging_framework.filters import SensitiveDataFilter
from .core.logging_framework.schemas import LoggingFrameworkConfig
from .core.logging_framework.service import (
    get_logging_service as get_flexible_logging_service,
)
from .globals import app_start_time
from .middleware.request_id import RequestIDMiddleware

# Initialize and register the global error handler
log = py_logging.getLogger(__name__)
log.info("Initializing global error handler...")
# In a real app, this config would be loaded from a YAML file
default_error_config = ErrorHandlerConfig()
error_handler = initialize_error_handler(config=default_error_config, logger=log)
register_system_hooks(handler=error_handler)


api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)

app = FastAPI(
    title="Zotify API",
    description="A RESTful API for Zotify, a Spotify music downloader.",
    version="0.1.20",
    security=[{"APIKeyHeader": []}],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestIDMiddleware)


def initialize_logging_framework() -> None:
    """Loads config and initializes the new flexible logging framework."""
    try:
        # Construct a path to 'api/logging_framework.yml' relative to this file's location
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logging_framework.yml'))
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)

        validated_config = LoggingFrameworkConfig(**config_data)

        logging_service = get_flexible_logging_service()
        logging_service.load_config(validated_config)
        log_event(
            "Flexible logging framework initialized from config.",
            level="INFO",
            # Assumes a console sink named 'default_console' exists
            destinations=["default_console"],
        )

        # If in production, add a filter to redact sensitive data from all logs
        if settings.app_env == "production":
            py_logging.getLogger().addFilter(SensitiveDataFilter())
            log_event(
                "Production mode detected. Applying sensitive data filter to all logs.",
                level="INFO",
            )

    except (FileNotFoundError, ValidationError, yaml.YAMLError) as e:
        # Fallback to basic logging if the framework fails to initialize
        log.error(f"FATAL: Could not initialize flexible logging framework: {e}")
        log.error("Logging will be degraded. Please check logging_framework.yml.")


@app.on_event("startup")
def startup_event() -> None:
    """Application startup event handler."""
    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Register FastAPI exception handlers
    register_fastapi_hooks(app=app, handler=error_handler)

    # Initialize the new flexible logging framework
    initialize_logging_framework()


prefix = settings.api_prefix

modules = [
    auth,
    cache,
    system,
    user,
    playlists,
    tracks,
    downloads,
    sync,
    config,
    network,
    search,
    webhooks,
    notifications,
]
for m in modules:
    app.include_router(m.router, prefix=prefix)


@app.get("/ping")
async def ping() -> Dict[str, bool]:
    return {"pong": True}


@app.get("/health", tags=["health"])
async def health_check() -> Dict[str, str]:
    return {"status": "ok", "message": "API is running"}


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint() -> Dict[str, Any]:
    return app.openapi()


@app.get("/version")
async def version() -> Dict[str, Any]:
    return {
        "api": "v0.1.28",
        "cli_version": "v0.1.54",
        "build": "local",
        "uptime": time.time() - app_start_time,
    }


@app.get("/api/schema", tags=["system"], dependencies=[Depends(require_admin_api_key)])
def get_schema(request: Request, q: Optional[str] = None) -> Dict[str, Any]:
    """Returns OpenAPI spec or a specific schema fragment."""
    openapi_schema = cast(Dict[str, Any], request.app.openapi())
    if q:
        if (
            "components" in openapi_schema
            and "schemas" in openapi_schema["components"]
            and q in openapi_schema["components"]["schemas"]
        ):
            return cast(
                Dict[str, Any], openapi_schema["components"]["schemas"][q]
            )
        else:
            raise HTTPException(status_code=404, detail=f"Schema '{q}' not found.")
    return openapi_schema
