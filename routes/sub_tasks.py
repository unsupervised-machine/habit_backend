from fastapi import APIRouter, HTTPException
from models import SubTask, SubTaskCreate, SubTaskUpdate
import crud

router = APIRouter(prefix="/sub_tasks", tags=["Sub Tasks"])

@router.post("/", response_model=SubTask)
def create_sub_task_endpoint(task: SubTaskCreate):
    crud.create_sub_task(task.big_task_id, task.title, task.description, task.completion_mode, task.user_id)
    created_task = crud.get_last_inserted_sub_task()  # Implement this helper if desired.
    if not created_task:
        raise HTTPException(status_code=404, detail="Sub Task not created")
    return created_task

@router.get("/{sub_task_id}", response_model=SubTask)
def get_sub_task(sub_task_id: int):
    task = crud.get_sub_task_by_id(sub_task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Sub Task not found")
    return task

@router.put("/{sub_task_id}", response_model=SubTask)
def update_sub_task_endpoint(sub_task_id: int, task_update: SubTaskUpdate):
    crud.update_sub_task(sub_task_id, task_update.title, task_update.description, task_update.completion_mode, task_update.user_id)
    updated_task = crud.get_sub_task_by_id(sub_task_id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Sub Task not found")
    return updated_task

@router.delete("/{sub_task_id}")
def delete_sub_task_endpoint(sub_task_id: int):
    crud.delete_sub_task(sub_task_id)
    return {"detail": "Sub Task deleted"}
