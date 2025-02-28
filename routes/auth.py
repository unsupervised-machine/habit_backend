from pprint import pprint

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated


from config import ACCESS_TOKEN_EXPIRE_MINUTES
from crud import authenticate_user, get_current_user, register_user
from models import User, UserCreate, Token
from password_tools import create_access_token



router = APIRouter()


@router.post("/register")
def register(user: UserCreate):
    return register_user(user)


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    # OAuth2PasswordRequestForm expects "username" but we will treat it as email
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.get("/users/me/items")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.email}]