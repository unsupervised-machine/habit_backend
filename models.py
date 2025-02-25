import uuid
import bcrypt
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

from password_tools import hash_password, verify_password


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    hashed_password: str = Field(..., exclude=True)  # Exclude from serialization

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "first_name": "Jon",
                "last_name": "Doe",
                "email": "jdoe@gmail.com",
                "hashed_password": "hashed_password_here",
            }
        }


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str  # Accepts raw password from user input

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Jon",
                "last_name": "Doe",
                "email": "jdoe@gmail.com",
                "password": "raw_password_here",
            }
        }


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # Accepts raw password if the user wants to update it

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Jon",
                "last_name": "Doe",
                "email": "jdoe@gmail.com",
                "password": "raw_password_here",
            }
        }