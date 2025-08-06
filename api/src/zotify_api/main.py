from fastapi import FastAPI
from fastapi.security.api_key import APIKeyHeader
from zotify_api.config import settings
from zotify_api.routes import metadata, cache, logging, system, user, playlist, tracks, downloads, spotify, sync, stubs, search, webhooks
from .globals import app_start_time
from .middleware.request_id import RequestIDMiddleware
from .logging_config import setup_logging

setup_logging()

api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)

app = FastAPI(
    title="Zotify API",
    description="A RESTful API for Zotify, a Spotify music downloader.",
    version="0.1.20",
    security=[{"APIKeyHeader": []}],
)
app.add_middleware(RequestIDMiddleware)

from zotify_api.routes import config, network

prefix = settings.api_prefix

modules = [metadata, cache, logging, system, user, playlist, tracks, downloads, sync, stubs, config, network, search, webhooks, spotify]
for m in modules:
    app.include_router(m.router, prefix=prefix)

@app.get("/ping")
async def ping():
    return {"pong": True}

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return app.openapi()
