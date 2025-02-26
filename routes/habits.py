from pprint import pprint

from fastapi import APIRouter, status

from models import Habit, HabitCreate, HabitUpdate
from crud import create_habit, get_habit, update_habit, delete_habit


router = APIRouter()


@router.post(path="", response_description="Create a new habit.", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_habit_route(habit: HabitCreate):
    result = create_habit(habit)
    return result


@router.get(path="/{habit_id}", response_description="Retrieve habit details by habit_id.", status_code=status.HTTP_200_OK, response_model=dict)
def get_habit_route(habit_id: str):
    result = get_habit(habit_id)
    return result


@router.patch(path="/{habit_id}", response_description="Update habit details by habit_id.", status_code=status.HTTP_200_OK, response_model=dict)
def update_habit_route(habit_id: str, habit_update: HabitUpdate):
    result = update_habit(habit_id, habit_update)
    return result


@router.delete(path="/{habit_id}", response_description="Delete a habit by habit_id.", status_code=status.HTTP_200_OK, response_model=dict)
def delete_habit_route(habit_id: str):
    result = delete_habit(habit_id)
    return result

