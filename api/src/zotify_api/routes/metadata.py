from fastapi import APIRouter, Depends
from zotify_api.schemas.metadata import MetadataUpdate, MetadataResponse, MetadataPatchResponse
from zotify_api.services.metadata_service import MetadataService, get_metadata_service

router = APIRouter()

@router.get(
    "/metadata/{track_id}",
    response_model=MetadataResponse,
    summary="Get extended metadata for a track"
)
def get_metadata(
    track_id: str,
    metadata_service: MetadataService = Depends(get_metadata_service)
):
    """
    Retrieves extended metadata for a specific track.

    - **track_id**: The ID of the track to retrieve metadata for.
    """
    return metadata_service.get_metadata(track_id)

@router.patch(
    "/metadata/{track_id}",
    response_model=MetadataPatchResponse,
    summary="Update extended metadata for a track"
)
def patch_metadata(
    track_id: str,
    meta: MetadataUpdate,
    metadata_service: MetadataService = Depends(get_metadata_service)
):
    """
    Updates extended metadata for a specific track.

    - **track_id**: The ID of the track to update.
    - **meta**: A `MetadataUpdate` object with the fields to update.
    """
    return metadata_service.patch_metadata(track_id, meta)
