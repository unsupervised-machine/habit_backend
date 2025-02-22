# habits.py
from fastapi import APIRouter, HTTPException
from models import HabitCreate, HabitUpdate, SubHabitCreate, SubHabitUpdate
import crud

router = APIRouter()


# --- Habit Endpoints ---
@router.post("", status_code=201)
def create_habit(habit: HabitCreate):
    habit_id = crud.create_habit(habit.user_id, habit.name, habit.description)
    return {"message": "Habit created successfully", "habit_id": habit_id}

@router.get("/{habit_id}")
def get_habit(habit_id: int):
    habit = crud.get_habit_by_id(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.put("/{habit_id}")
def update_habit(habit_id: int, habit_update: HabitUpdate):
    updated_habit = crud.update_habit(habit_id, habit_update.name, habit_update.description)
    if not updated_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return updated_habit

@router.delete("/{habit_id}")
def delete_habit(habit_id: int):
    success = crud.delete_habit(habit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found")
    return {"message": "Habit deleted successfully"}

# --- Sub-Habit Endpoints ---
@router.post("/{habit_id}/sub-habits", status_code=201)
def create_sub_habit(habit_id: int, sub_habit: SubHabitCreate):
    if sub_habit.habit_id != habit_id:
        raise HTTPException(status_code=400, detail="Mismatch between route and body habit_id")
    sub_habit_id = crud.create_sub_habit(habit_id, sub_habit.name, sub_habit.description)
    return {"message": "Sub-habit created successfully", "sub_habit_id": sub_habit_id}

@router.get("/sub-habits/{sub_habit_id}")
def get_sub_habit(sub_habit_id: int):
    sub_habit = crud.get_sub_habit_by_id(sub_habit_id)
    if not sub_habit:
        raise HTTPException(status_code=404, detail="Sub-habit not found")
    return sub_habit

@router.put("/sub-habits/{sub_habit_id}")
def update_sub_habit(sub_habit_id: int, sub_habit_update: SubHabitUpdate):
    updated_sub_habit = crud.update_sub_habit(sub_habit_id, sub_habit_update.name, sub_habit_update.description)
    if not updated_sub_habit:
        raise HTTPException(status_code=404, detail="Sub-habit not found")
    return updated_sub_habit

@router.delete("/sub-habits/{sub_habit_id}")
def delete_sub_habit(sub_habit_id: int):
    success = crud.delete_sub_habit(sub_habit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sub-habit not found")
    return {"message": "Sub-habit deleted successfully"}
