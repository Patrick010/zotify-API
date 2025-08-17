import pytest
from zotify_api.services.metadata_service import MetadataService
from zotify_api.schemas.metadata import MetadataUpdate

@pytest.fixture
def metadata_service():
    service = MetadataService()
    service._reset_data()
    return service

def test_get_metadata_exists(metadata_service):
    metadata = metadata_service.get_metadata("abc123")
    assert metadata["title"] == "Track Title"
    assert metadata["mood"] == "Chill"

def test_get_metadata_not_exists(metadata_service):
    metadata = metadata_service.get_metadata("nonexistent")
    assert metadata["status"] == "not found"

def test_patch_metadata_exists(metadata_service):
    update_data = MetadataUpdate(mood="Energetic", rating=5)
    response = metadata_service.patch_metadata("abc123", update_data)
    assert response["status"] == "success"

    metadata = metadata_service.get_metadata("abc123")
    assert metadata["mood"] == "Energetic"
    assert metadata["rating"] == 5

def test_patch_metadata_not_exists(metadata_service):
    update_data = MetadataUpdate(mood="Happy")
    response = metadata_service.patch_metadata("new_track", update_data)
    assert response["status"] == "success"

    metadata = metadata_service.get_metadata("new_track")
    assert metadata["title"] == "Track new_track"
    assert metadata["mood"] == "Happy"
