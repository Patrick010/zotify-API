from fastapi import FastAPI
from zotify_api.routes import playlist

app = FastAPI(
    title="Zotify API",
    version="0.1.3",
    description="A REST API for the Zotify music and podcast downloader."
)

app.include_router(playlist.router)

@app.get("/ping")
async def ping():
    return {"pong": True}
