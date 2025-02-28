import uuid
from datetime import datetime
from datetime import date as _date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


# def object_id_str(value: ObjectId) -> str:
#     return str(value)

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
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
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    first_name: str
    last_name: str
    email: EmailStr
    password: str  # Accepts raw password from user input

    class Config:
        populate_by_name = True
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


class Habit(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str = Field(...)
    name: str = Field(...)
    description: Optional[str] = None
    sort_index: float = Field(...)
    category: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    start_date: Optional[_date] = None
    end_date: Optional[_date] = None
    archived: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "user_id": "a77de609-c04a-5b30-c46c-32537c7f2g7f",
                "name": "Morning Meditation",
                "description": "15 minutes of mindfulness meditation",
                "sort_index": 1.5,
                "category": "Wellness",
                "color": "#4287f5",
                "icon": "meditation",
                "start_date": "2025-02-25",
                "end_date": None,
                "archived": False,
                "created_at": "2025-02-25T08:00:00",
                "updated_at": "2025-02-25T08:00:00"
            }
        }


class HabitCreate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    name: str
    description: Optional[str] = None
    sort_index: float = Field(...)
    category: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    start_date: Optional[_date] = None
    end_date: Optional[_date] = None
    archived: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "a77de609-c04a-5b30-c46c-32537c7f2g7f",
                "name": "Morning Meditation",
                "description": "15 minutes of mindfulness meditation",
                "sort_index": 1.5,
                "category": "Wellness",
                "color": "#4287f5",
                "icon": "meditation",
                "start_date": "2025-02-25",
                "end_date": None,
                "archived": False
            }
        }


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sort_index: Optional[float] = None
    category: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    start_date: Optional[_date] = None
    end_date: Optional[_date] = None
    archived: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Morning Meditation",
                "description": "20 minutes of mindfulness meditation",
                "sort_index": 1.5,
                "category": "Mental Health",
                "color": "#42b0f5",
                "icon": "meditation",
                "archived": True
            }
        }


class Completion(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    habit_id: str = Field(...)
    user_id: str = Field(...)
    date: _date = Field(...)
    completed: Optional[bool] = False
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "166de609-b04a-4b30-b46c-32537c7f1f7d",
                "habit_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "user_id": "a77de609-c04a-5b30-c46c-32537c7f2g7f",
                "date": "2025-02-25",
                "completed": True,
                "timestamp": "2025-02-25T08:15:30"
            }
        }


class CompletionCreate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    habit_id: str
    user_id: str
    date: _date
    completed: Optional[bool] = False

    class Config:
        json_schema_extra = {
            "example": {
                "habit_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "user_id": "a77de609-c04a-5b30-c46c-32537c7f2g7f",
                "date": "2025-02-25",
                "completed": False
            }
        }


class CompletionUpdate(BaseModel):
    completed: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "completed": False
            }
        }


class CompletionUpsert(BaseModel):
    user_id: str
    habit_id: str
    date: str=str(_date.today())  # This ensures a YYYY-MM-DD format
    completed: bool = False