from fastapi import APIRouter, HTTPException, status
from models import UserCreate

router = APIRouter()


@router.post("/login")
def login(username: str, password: str):
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="Not implemented")


@router.post("/register")
def register(user: UserCreate):
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="Not implemented")