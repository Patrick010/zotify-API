from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from zotify_api.config import settings
from zotify_api.routes import auth, metadata, cache, system, user, playlist, tracks, download, spotify, sync, search, webhooks, notifications
from .globals import app_start_time
from .middleware.request_id import RequestIDMiddleware
from .logging_config import setup_logging
import logging as py_logging
from .core.error_handler import (
    initialize_error_handler,
    register_system_hooks,
    register_fastapi_hooks,
    ErrorHandlerConfig,
)

from zotify_api.database.session import Base, engine

setup_logging()

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

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    register_fastapi_hooks(app=app, handler=error_handler)

from zotify_api.routes import config, network

prefix = settings.api_prefix

modules = [auth, metadata, cache, system, user, playlist, tracks, download, sync, config, network, search, webhooks, spotify, notifications]
for m in modules:
    app.include_router(m.router, prefix=prefix)

@app.get("/ping")
async def ping():
    return {"pong": True}

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "message": "API is running"}

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return app.openapi()

import time

from typing import Optional
from fastapi import Depends, HTTPException, Request
from zotify_api.services.auth import require_admin_api_key

@app.get("/version")
async def version():
    return {
        "api": "v0.1.28",
        "cli_version": "v0.1.54",
        "build": "local",
        "uptime": time.time() - app_start_time,
    }

@app.get("/api/schema", tags=["system"], dependencies=[Depends(require_admin_api_key)])
def get_schema(request: Request, q: Optional[str] = None):
    """ Returns either full OpenAPI spec or schema fragment for requested object type (via query param). """
    openapi_schema = request.app.openapi()
    if q:
        if "components" in openapi_schema and "schemas" in openapi_schema["components"] and q in openapi_schema["components"]["schemas"]:
            return openapi_schema["components"]["schemas"][q]
        else:
            raise HTTPException(status_code=404, detail=f"Schema '{q}' not found.")
    return openapi_schema
