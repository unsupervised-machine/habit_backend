# users.py
from fastapi import APIRouter, HTTPException
from models import UserUpdate
import crud

router = APIRouter()


@router.get("/users/{user_id}")
def get_user(user_id: str):
    user = crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}")
def update_user(user_id: str, user_update: UserUpdate):
    new_password_hash = None
    if user_update.password:
        # Hash the new password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        new_password_hash = pwd_context.hash(user_update.password)
    updated_user = crud.update_user(
        user_id,
        email=user_update.email,
        password_hash=new_password_hash,
        notifications_enabled=user_update.notifications_enabled,
        stripe_customer_id=user_update.stripe_customer_id
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    success = crud.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
