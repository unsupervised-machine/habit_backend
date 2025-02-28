from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated


from config import ACCESS_TOKEN_EXPIRE_MINUTES
from crud import authenticate_user, get_current_user, register_user, get_user_by_email
from models import User, UserCreate, Token
from password_tools import create_access_token



router = APIRouter()


@router.get(path="/email/{email}", response_description="Retrieve user details by email", response_model=User, status_code=status.HTTP_200_OK)
def get_user_by_email_route(email: str):
    # Example: /auth/email/test4@gmail.com
    return get_user_by_email(email)


@router.post("/register")
def register(user: UserCreate):
    return register_user(user)


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    OAuth2 compatible token login, return an access token for future requests (send to front end to hold on to)
    :param form_data:
    :return:
    """
    # OAuth2PasswordRequestForm expects "username" but we give it an email
    user = authenticate_user(email=form_data.username, password=form_data.password)
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
    """
    Get details of current logged in user (requires token auth)
    :param current_user:
    :return:
    """
    return current_user


@router.get("/users/me/items")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.email}]