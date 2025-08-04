"""
Zotify API - Phase 0 Proof of Concept

Instructions:

1. Make sure Python 3.8+ is installed.
2. Install required packages via pip:

   pip install fastapi uvicorn

3. Run the API server with a configurable host and port (default is 127.0.0.1:8000):

   uvicorn main:app --reload --host 0.0.0.0 --port 8080

   Replace `0.0.0.0` with your desired bind address (e.g. LAN IP) to allow access from other machines.
   Adjust the port as needed.

4. Test the endpoint from a browser or curl:

   http://<your-host>:<your-port>/ping

   Expected response: {"pong": true}
---

File: main.py
"""

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
