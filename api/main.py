from fastapi import FastAPI
from .routes import playlist

app = FastAPI(
    title="Zotify API",
    version="0.1.3",
    description="A REST API for the Zotify music and podcast downloader."
)

app.include_router(playlist.router)
