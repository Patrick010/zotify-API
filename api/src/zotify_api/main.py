from fastapi import FastAPI
from zotify_api.routes import playlist, config, tracks, logging, cache, network, sync, downloads, metadata, spotify

app = FastAPI(
    title="Zotify API",
    version="0.1.3",
    description="A REST API for the Zotify music and podcast downloader."
)

app.include_router(playlist.router, prefix="/api")
app.include_router(config.router, prefix="/api")
app.include_router(tracks.router, prefix="/api")
app.include_router(logging.router, prefix="/api")
app.include_router(cache.router, prefix="/api")
app.include_router(network.router, prefix="/api")
app.include_router(sync.router, prefix="/api")
app.include_router(downloads.router, prefix="/api")
app.include_router(metadata.router, prefix="/api")
app.include_router(spotify.router, prefix="/api")

@app.get("/ping")
async def ping():
    return {"pong": True}
