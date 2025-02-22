# completions.py
from fastapi import APIRouter, HTTPException
from models import HabitCompletionCreate, HabitCompletionUpdate, SubHabitCompletionCreate, SubHabitCompletionUpdate
import crud

router = APIRouter()

# --- Habit Completions Endpoints ---
@router.post("/habits", status_code=201)
def create_habit_completion(completion: HabitCompletionCreate):
    completion_id = crud.create_habit_completion(completion.user_id, completion.habit_id, completion.date, completion.completed)
    return {"message": "Habit completion recorded", "completion_id": completion_id}

@router.get("/habits/{completion_id}")
def get_habit_completion(completion_id: int):
    completion = crud.get_habit_completion_by_id(completion_id)
    if not completion:
        raise HTTPException(status_code=404, detail="Habit completion not found")
    return completion

@router.put("/habits/{completion_id}")
def update_habit_completion(completion_id: int, update: HabitCompletionUpdate):
    updated = crud.update_habit_completion(completion_id, update.completed)
    if not updated:
        raise HTTPException(status_code=404, detail="Habit completion not found")
    return updated

@router.delete("/habits/{completion_id}")
def delete_habit_completion(completion_id: int):
    if not crud.delete_habit_completion(completion_id):
        raise HTTPException(status_code=404, detail="Habit completion not found")
    return {"message": "Habit completion deleted successfully"}

# --- Sub-Habit Completions Endpoints ---
@router.post("/sub-habits", status_code=201)
def create_sub_habit_completion(completion: SubHabitCompletionCreate):
    completion_id = crud.create_sub_habit_completion(completion.sub_habit_id, completion.date, completion.completed, completion.user_id)
    return {"message": "Sub-habit completion recorded", "completion_id": completion_id}

@router.get("/sub-habits/{completion_id}")
def get_sub_habit_completion(completion_id: int):
    completion = crud.get_sub_habit_completion_by_id(completion_id)
    if not completion:
        raise HTTPException(status_code=404, detail="Sub-habit completion not found")
    return completion

@router.put("/sub-habits/{completion_id}")
def update_sub_habit_completion(completion_id: int, update: SubHabitCompletionUpdate):
    updated = crud.update_sub_habit_completion(completion_id, update.completed)
    if not updated:
        raise HTTPException(status_code=404, detail="Sub-habit completion not found")
    return updated

@router.delete("/sub-habits/{completion_id}")
def delete_sub_habit_completion(completion_id: int):
    if not crud.delete_sub_habit_completion(completion_id):
        raise HTTPException(status_code=404, detail="Sub-habit completion not found")
    return {"message": "Sub-habit completion deleted successfully"}
