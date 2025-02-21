from fastapi import APIRouter, HTTPException
from models import BigTask, BigTaskCreate, BigTaskUpdate
import crud

router = APIRouter(prefix="/big_tasks", tags=["Big Tasks"])

@router.post("/", response_model=BigTask)
def create_big_task_endpoint(task: BigTaskCreate):
    crud.create_big_task(task.title, task.description, task.completion_mode, task.user_id)
    created_task = crud.get_last_inserted_big_task()  # Implement this helper in crud.py if needed.
    if not created_task:
        raise HTTPException(status_code=404, detail="Big Task not created")
    return created_task

@router.get("/{big_task_id}", response_model=BigTask)
def get_big_task(big_task_id: int):
    task = crud.get_big_task_by_id(big_task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Big Task not found")
    return task

@router.put("/{big_task_id}", response_model=BigTask)
def update_big_task_endpoint(big_task_id: int, task_update: BigTaskUpdate):
    crud.update_big_task(big_task_id, task_update.title, task_update.description, task_update.completion_mode, task_update.user_id)
    updated_task = crud.get_big_task_by_id(big_task_id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Big Task not found")
    return updated_task

@router.delete("/{big_task_id}")
def delete_big_task_endpoint(big_task_id: int):
    crud.delete_big_task(big_task_id)
    return {"detail": "Big Task deleted"}
