from fastapi import FastAPI
from zotify_api.routes import metadata, cache, logging, system, user, playlist, tracks, downloads, spotify, sync, stubs
from .globals import app_start_time

app = FastAPI()
from zotify_api.routes import config, network

modules = [metadata, cache, logging, system, user, playlist, tracks, downloads, sync, stubs, config, network]
for m in modules:
    app.include_router(m.router, prefix="/api")
app.include_router(spotify.router, prefix="/api/spotify")

@app.get("/ping")
async def ping():
    return {"pong": True}
