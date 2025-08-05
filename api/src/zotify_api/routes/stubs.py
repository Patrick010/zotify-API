from fastapi import APIRouter
from zotify_api.models.stubs import Stub, StubsResponse
from typing import List

router = APIRouter()

mock_stubs = [
    Stub(id=1, name="sample1", description="Dev fixture A"),
    Stub(id=2, name="sample2", description="Dev fixture B"),
]

@router.get("/stubs", response_model=StubsResponse, summary="Get all stubs")
def get_stubs():
    return {"data": mock_stubs}
