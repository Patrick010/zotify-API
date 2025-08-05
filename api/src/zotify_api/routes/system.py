from fastapi import APIRouter
from zotify_api.models.system import SystemInfo

router = APIRouter()

mock_system_info = SystemInfo(
    status="System is operational",
    free_space="100GB",
    total_space="500GB",
    logs=["Log entry 1", "Log entry 2"],
)

@router.get("/system", response_model=SystemInfo)
def get_system_info():
    return mock_system_info

@router.get("/system/status")
def get_system_status():
    return {"status": mock_system_info.status}

@router.get("/system/storage")
def get_system_storage():
    return {"free_space": mock_system_info.free_space, "total_space": mock_system_info.total_space}

@router.get("/system/logs")
def get_system_logs():
    return mock_system_info.logs

@router.post("/system/reload")
def reload_system_config():
    return {"message": "System config reloaded"}

@router.post("/system/reset")
def reset_system_state():
    return {"message": "System state reset"}
