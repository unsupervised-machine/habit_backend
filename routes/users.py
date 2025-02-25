# users.py
from fastapi import APIRouter, HTTPException, status
from models import UserUpdate, User
from routes.auth import get_password_hash
import crud

router = APIRouter()

@router.post(path="", response_description="Create a new user.", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_user(email, name, password):
    try:
        hashed_password = get_password_hash(password)
        user_id = crud.create_user(email=email, name=name, password_hash=hashed_password)
        return {"message": "User created successfully", "user_id": user_id}
    except Exception as e:
        return {"message": str(e)}

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
