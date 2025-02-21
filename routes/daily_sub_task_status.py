from fastapi import APIRouter, HTTPException
from models import DailySubTaskStatus, DailySubTaskStatusCreate, DailySubTaskStatusUpdate
import crud

router = APIRouter(prefix="/daily_sub_task_status", tags=["Daily Sub Task Statuses"])

@router.post("/", response_model=DailySubTaskStatus)
def create_daily_sub_task_status_endpoint(status: DailySubTaskStatusCreate):
    crud.create_daily_sub_task_status(status.sub_task_id, status.user_id, status.date.isoformat(), status.completion_value)
    created_status = crud.get_last_inserted_daily_sub_task_status()  # Implement this helper if desired.
    if not created_status:
        raise HTTPException(status_code=404, detail="Daily Sub Task Status not created")
    return created_status

@router.get("/{status_id}", response_model=DailySubTaskStatus)
def get_daily_sub_task_status(status_id: int):
    status = crud.get_daily_sub_task_status_by_id(status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Daily Sub Task Status not found")
    return status

@router.put("/{status_id}", response_model=DailySubTaskStatus)
def update_daily_sub_task_status_endpoint(status_id: int, status_update: DailySubTaskStatusUpdate):
    crud.update_daily_sub_task_status(status_id, status_update.completion_value)
    updated_status = crud.get_daily_sub_task_status_by_id(status_id)
    if not updated_status:
        raise HTTPException(status_code=404, detail="Daily Sub Task Status not found")
    return updated_status

@router.delete("/{status_id}")
def delete_daily_sub_task_status_endpoint(status_id: int):
    crud.delete_daily_sub_task_status(status_id)
    return {"detail": "Daily Sub Task Status deleted"}
