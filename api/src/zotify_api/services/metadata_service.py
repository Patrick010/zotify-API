from zotify_api.schemas.metadata import MetadataUpdate

# Simulated backend storage
def get_initial_metadata():
    return {
        "abc123": {
            "title": "Track Title",
            "mood": "Chill",
            "rating": 4,
            "source": "Manual Import"
        }
    }

track_metadata = get_initial_metadata()

class MetadataService:
    def get_metadata(self, track_id: str):
        return track_metadata.get(track_id, {"track_id": track_id, "status": "not found"})

    def patch_metadata(self, track_id: str, meta: MetadataUpdate):
        if track_id not in track_metadata:
            track_metadata[track_id] = {"title": f"Track {track_id}"}
        for k, v in meta.model_dump(exclude_unset=True).items():
            track_metadata[track_id][k] = v
        return {"status": "success", "track_id": track_id}

    def _reset_data(self):
        global track_metadata
        track_metadata = get_initial_metadata()

def get_metadata_service():
    return MetadataService()
