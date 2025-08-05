from fastapi import APIRouter
from zotify_api.models.system import SystemInfo
from zotify_api.services.system import get_system_info

router = APIRouter()

@router.get("/system", response_model=SystemInfo)
def system_route():
    return get_system_info()
