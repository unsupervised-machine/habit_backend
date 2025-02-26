from fastapi import APIRouter, status

from models import User, UserCreate, UserUpdate
from crud import create_user, get_user, update_user, delete_user


router = APIRouter()


@router.post(path="", response_description="Create a new user", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate):
    result = create_user(user)
    return result

@router.get(path="/{user_id}", response_description="Retrieve user information by userId.", response_model=User, status_code=status.HTTP_200_OK )
def get_user_route(user_id: str):
    result = get_user(user_id)
    return result

@router.patch(path="/{user_id}", response_description="Update user information by userId.", response_model=User, status_code=status.HTTP_200_OK)
def update_user_route(user_id: str, user: UserUpdate):
    result = update_user(user_id, user)
    return result

@router.delete(path="/{user_id}", response_description="Delete a user by userId.", status_code=status.HTTP_200_OK, response_model=dict)
def delete_user_route(user_id: str):
    result = delete_user(user_id)
    return result