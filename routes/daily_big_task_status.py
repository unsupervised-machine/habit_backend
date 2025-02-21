from fastapi import APIRouter, HTTPException
from models import DailyBigTaskStatus, DailyBigTaskStatusCreate, DailyBigTaskStatusUpdate
import crud

router = APIRouter(prefix="/daily_big_task_status", tags=["Daily Big Task Statuses"])

@router.post("/", response_model=DailyBigTaskStatus)
def create_daily_big_task_status_endpoint(status: DailyBigTaskStatusCreate):
    crud.create_daily_big_task_status(status.big_task_id, status.user_id, status.date.isoformat(), status.completion_value)
    created_status = crud.get_last_inserted_daily_big_task_status()  # Implement this helper if desired.
    if not created_status:
        raise HTTPException(status_code=404, detail="Daily Big Task Status not created")
    return created_status

@router.get("/{status_id}", response_model=DailyBigTaskStatus)
def get_daily_big_task_status(status_id: int):
    status = crud.get_daily_big_task_status_by_id(status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Daily Big Task Status not found")
    return status

@router.put("/{status_id}", response_model=DailyBigTaskStatus)
def update_daily_big_task_status_endpoint(status_id: int, status_update: DailyBigTaskStatusUpdate):
    crud.update_daily_big_task_status(status_id, status_update.completion_value)
    updated_status = crud.get_daily_big_task_status_by_id(status_id)
    if not updated_status:
        raise HTTPException(status_code=404, detail="Daily Big Task Status not found")
    return updated_status

@router.delete("/{status_id}")
def delete_daily_big_task_status_endpoint(status_id: int):
    crud.delete_daily_big_task_status(status_id)
    return {"detail": "Daily Big Task Status deleted"}
