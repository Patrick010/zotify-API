from fastapi import APIRouter

router = APIRouter()

@router.get("/system")
def get_system_info():
    return {"status": "System is operational"}

@router.get("/system/status")
def get_system_status():
    return {"status": "All systems nominal"}

@router.get("/system/storage")
def get_system_storage():
    return {"free_space": "100GB", "total_space": "500GB"}

@router.get("/system/logs")
def get_system_logs():
    return ["Log entry 1", "Log entry 2"]

@router.post("/system/reload")
def reload_system_config():
    return {"message": "System config reloaded"}

@router.post("/system/reset")
def reset_system_state():
    return {"message": "System state reset"}
