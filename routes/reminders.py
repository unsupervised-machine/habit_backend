from fastapi import APIRouter, HTTPException, Depends
from models import Reminder, ReminderCreate, ReminderUpdate
import crud
from routes.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=list[Reminder])
def read_reminders(current_user: dict = Depends(get_current_user)):
    reminders = crud.get_reminders_by_user(current_user["id"])
    return [dict(row) for row in reminders]

@router.post("/", status_code=201)
def add_reminder(reminder: ReminderCreate, current_user: dict = Depends(get_current_user)):
    text = reminder.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    # Pass reminder.due_date (converted to ISO format) to the CRUD function
    crud.create_reminder(
        text=text,
        due_date=reminder.due_date.isoformat(),
        completed=False,
        user_id=current_user["id"])
    return {"message": "Reminder added successfully"}

@router.delete("/{reminder_id}", status_code=200)
def remove_reminder(reminder_id: int, current_user: dict = Depends(get_current_user)):
    crud.delete_reminder(reminder_id, current_user["id"])
    return {"message": "Reminder deleted successfully"}


@router.put("/{reminder_id}", status_code=200)
def update_reminder_endpoint(
        reminder_id: int,
        reminder: ReminderUpdate,
        current_user: dict = Depends(get_current_user)
):
    # For this example, require that all fields are provided.
    if reminder.text is None or reminder.due_date is None or reminder.completed is None:
        raise HTTPException(status_code=400, detail="All fields (text, due_date, completed) must be provided")

    updated_rows = crud.update_reminder(
        reminder_id,
        reminder.text,
        reminder.due_date.isoformat(),  # Convert datetime to ISO string
        current_user["id"],
        reminder.completed
    )
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return {"message": "Reminder updated successfully"}
