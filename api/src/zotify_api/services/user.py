from fastapi import Depends, Header
from zotify_api.auth import get_current_user  # your existing auth dependency

def get_current_user_info(user = Depends(get_current_user)):
    # user is what your auth returns: convert to schema
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "display_name": getattr(user, "display_name", None)
    }
