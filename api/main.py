import sys
from pathlib import Path

# Add the parent directory to the system path to allow imports from the zotify package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
async def ping():
    """
    GET /ping

    Simple health check endpoint to verify that the API server is up and running.

    Response:
        HTTP 200 OK
        JSON body: {"pong": true}
    """
    return {"pong": True}
