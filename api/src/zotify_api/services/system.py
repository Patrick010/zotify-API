import time
import socket
import sys
from zotify_api.globals import app_start_time
from zotify_api.config import settings

def get_system_info():
    uptime_seconds = time.time() - app_start_time
    return {
        "uptime_seconds": round(uptime_seconds, 2),
        "version": settings.app_version,
        "env": settings.app_env,
        "hostname": socket.gethostname(),
        "python_version": sys.version.split()[0]
    }
