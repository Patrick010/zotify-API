from fastapi import FastAPI
from zotify_api.config import settings
from zotify_api.routes import metadata, cache, logging, system, user, playlist, tracks, downloads, spotify, sync, stubs, search, webhooks
from .globals import app_start_time
from .middleware.request_id import RequestIDMiddleware
from .logging_config import setup_logging

setup_logging()

app = FastAPI()
app.add_middleware(RequestIDMiddleware)

from zotify_api.routes import config, network

prefix = settings.api_prefix

modules = [metadata, cache, logging, system, user, playlist, tracks, downloads, sync, stubs, config, network]
for m in modules:
    app.include_router(m.router, prefix=prefix)
app.include_router(search.router, prefix=f"{prefix}/search")
app.include_router(webhooks.router, prefix=f"{prefix}/webhooks")
app.include_router(spotify.router, prefix=f"{prefix}/spotify")

@app.get("/ping")
async def ping():
    return {"pong": True}
