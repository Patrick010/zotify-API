from pydantic import BaseModel

class SyncRequest(BaseModel):
    playlist_id: str
