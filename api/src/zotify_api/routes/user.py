from fastapi import APIRouter, Depends
from zotify_api.models.user import UserModel
from zotify_api.services.user import get_current_user_info

router = APIRouter()

@router.get("/user", response_model=UserModel)
def user_route(user = Depends(get_current_user_info)):
    return user
