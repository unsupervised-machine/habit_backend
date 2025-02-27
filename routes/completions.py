from fastapi import APIRouter, status

from models import Completion, CompletionCreate, CompletionUpdate
from crud import create_completion, get_completion, update_completion, upsert_completion, prepare_completions


router = APIRouter()


@router.post(path="", response_description="Create a new completion.", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_completion_route(completion: CompletionCreate):
    result = create_completion(completion)
    return result


@router.get(path="/{completion_id}", response_description="Retrieve completion details by completion_id.", status_code=status.HTTP_200_OK, response_model=dict)
def get_completion_route(completion_id: str):
    result = get_completion(completion_id)
    return result


@router.patch(path="/{completion_id}", response_description="Update completion details by completion_id.", status_code=status.HTTP_200_OK, response_model=dict)
def update_completion_route(completion_id: str, completion: CompletionUpdate):
    result = update_completion(completion_id, completion)
    return result


@router.post(path="/prepare_completions", response_description="Prepare uncompleted completions for current day", status_code=status.HTTP_201_CREATED, response_model=dict)
def prepare_completions_route():
    result = prepare_completions()
    return result


@router.put(path="/upsert", response_description="Preforms a completion collection upsert using user_id and habit_id", status_code=status.HTTP_201_CREATED, response_model=dict)
def upsert_completion_route(user_id, habit_id, date, completion_id: str=None, completed: bool=False):
    result = upsert_completion(user_id, habit_id, date, completion_id, completed)
    return result