# backend/models.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Reminder models
class ReminderBase(BaseModel):
    text: str
    due_date: datetime
    completed: bool = False

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True

class ReminderUpdate(BaseModel):
    text: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None

# User models
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True

# Model for login (if you want a separate model)
class Login(BaseModel):
    email: str
    password: str


# ----------------------------
# Big Task models
# ----------------------------
class BigTaskBase(BaseModel):
    title: str
    description: str
    completion_mode: str  # Expected values: ALL, ANY, or PARTIAL

class BigTaskCreate(BigTaskBase):
    pass

class BigTask(BigTaskBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class BigTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completion_mode: Optional[str] = None

# ----------------------------
# Sub Task models
# ----------------------------
class SubTaskBase(BaseModel):
    big_task_id: int
    title: str
    description: str
    completion_mode: str  # Expected values: FULL or PARTIAL

class SubTaskCreate(SubTaskBase):
    pass

class SubTask(SubTaskBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class SubTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completion_mode: Optional[str] = None

# ----------------------------
# Daily Big Task Status models
# ----------------------------
class DailyBigTaskStatusBase(BaseModel):
    big_task_id: int
    datetime: datetime
    completion_value: str  # e.g., "True", "False", or "Partial"

class DailyBigTaskStatusCreate(DailyBigTaskStatusBase):
    pass

class DailyBigTaskStatus(DailyBigTaskStatusBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class DailyBigTaskStatusUpdate(BaseModel):
    completion_value: Optional[str] = None

# ----------------------------
# Daily Sub Task Status models
# ----------------------------
class DailySubTaskStatusBase(BaseModel):
    sub_task_id: int
    datetime: datetime
    completion_value: str  # e.g., "True", "False", or "Partial"

class DailySubTaskStatusCreate(DailySubTaskStatusBase):
    pass

class DailySubTaskStatus(DailySubTaskStatusBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class DailySubTaskStatusUpdate(BaseModel):
    completion_value: Optional[str] = None

# ----------------------------
# Big Task Attribute models
# ----------------------------
class BigTaskAttributeBase(BaseModel):
    big_task_id: int
    attribute_key: str  # e.g., "Book Name"
    attribute_value: str  # e.g., "The Great Gatsby"

class BigTaskAttributeCreate(BigTaskAttributeBase):
    pass

class BigTaskAttribute(BigTaskAttributeBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class BigTaskAttributeUpdate(BaseModel):
    attribute_key: Optional[str] = None
    attribute_value: Optional[str] = None

# ----------------------------
# Sub Task Attribute models
# ----------------------------
class SubTaskAttributeBase(BaseModel):
    sub_task_id: int
    attribute_key: str  # e.g., "pages"
    attribute_value: str  # e.g., "5"

class SubTaskAttributeCreate(SubTaskAttributeBase):
    pass

class SubTaskAttribute(SubTaskAttributeBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class SubTaskAttributeUpdate(BaseModel):
    attribute_key: Optional[str] = None
    attribute_value: Optional[str] = None