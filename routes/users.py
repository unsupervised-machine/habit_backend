from fastapi import APIRouter, status

from models import User, UserCreate, UserUpdate
from crud import create_user, get_user, update_user, delete_user
from crud import get_user_habits, get_user_habit_completions, get_user_habit_completion_streak


router = APIRouter()


@router.post(path="", response_description="Create a new user", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate):
    result = create_user(user)
    return result

@router.get(path="/{user_id}", response_description="Retrieve user details by user_id.", response_model=dict, status_code=status.HTTP_200_OK )
def get_user_route(user_id: str):
    result = get_user(user_id)
    return result

@router.patch(path="/{user_id}", response_description="Update user details by user_id.", response_model=dict, status_code=status.HTTP_200_OK)
def update_user_route(user_id: str, user: UserUpdate):
    result = update_user(user_id, user)
    return result

@router.delete(path="/{user_id}", response_description="Delete a user by user_id.", status_code=status.HTTP_200_OK, response_model=dict)
def delete_user_route(user_id: str):
    result = delete_user(user_id)
    return result


@router.get(path="/{user_id}/habits", response_description="Get all habits associated with a user_id.", status_code=status.HTTP_200_OK, response_model=list)
def get_user_habits_route(user_id: str):
    result = get_user_habits(user_id)
    return result


@router.get(path="/{user_id}/habits/{habit_id}", response_description="Get all user habit completions by user_id and habit_id.", status_code=status.HTTP_200_OK, response_model=list)
def get_user_habit_completions_route(user_id: str, habit_id: str):
    result = get_user_habit_completions(user_id, habit_id)
    return result


@router.get(path="/{user_id}/habits/{habit_id}/completion_streak", response_description="Get current streak for user habit.", status_code=status.HTTP_200_OK, response_model=dict)
def get_user_habit_completion_streak_route(user_id: str, habit_id: str):
    result = get_user_habit_completion_streak(user_id, habit_id)
    return result