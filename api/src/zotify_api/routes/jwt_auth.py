from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from zotify_api.database import crud
from zotify_api.database.session import get_db
from zotify_api.schemas import user as user_schema
from zotify_api.schemas.auth import Token
from zotify_api.services import jwt_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    crud.create_user(db=db, user=user)
    return {"msg": "User registered successfully"}


@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not jwt_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
