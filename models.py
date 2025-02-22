from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from uuid import UUID, uuid4

# --- 1. User & Authentication ---

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: str
    name: str
    password_hash: str
    notifications_enabled: bool = True
    stripe_customer_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Create and Update models for User
class UserCreate(BaseModel):
    email: str
    name: str
    password: str  # Plaintext password; hash before storing in User.password_hash
    notifications_enabled: Optional[bool] = True
    stripe_customer_id: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None  # If updating password; plaintext to be hashed
    notifications_enabled: Optional[bool] = None
    stripe_customer_id: Optional[str] = None


# --- 2. Payment Details ---

class Payment(BaseModel):
    id: int
    user_id: UUID  # assuming it references User.id
    stripe_charge_id: str
    amount: float
    currency: str
    payment_status: str  # e.g., "paid", "failed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Create and Update models for Payment
class PaymentCreate(BaseModel):
    user_id: UUID
    stripe_charge_id: str
    amount: float
    currency: str
    payment_status: str

class PaymentUpdate(BaseModel):
    stripe_charge_id: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    payment_status: Optional[str] = None


# --- 3. Habit Structure ---

class Habit(BaseModel):
    id: int
    user_id: UUID  # references User.id
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SubHabit(BaseModel):
    id: int
    habit_id: int  # references Habit.id
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Create and Update models for Habit and SubHabit
class HabitCreate(BaseModel):
    user_id: UUID
    name: str
    description: Optional[str] = None

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class SubHabitCreate(BaseModel):
    habit_id: int
    name: str
    description: Optional[str] = None

class SubHabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# --- 4. Completion & History Tracking ---

class HabitCompletion(BaseModel):
    id: int
    user_id: UUID  # redundant but simplifies queries
    habit_id: int  # references Habit.id
    date: date  # the day the habit was completed
    completed: bool

class SubHabitCompletion(BaseModel):
    id: int
    user_id: UUID  # redundant but simplifies queries
    sub_habit_id: int  # references SubHabit.id
    date: date  # the day the sub-habit was completed
    completed: bool

# Create and Update models for HabitCompletion and SubHabitCompletion
class HabitCompletionCreate(BaseModel):
    user_id: UUID
    habit_id: int
    date: date
    completed: bool

class HabitCompletionUpdate(BaseModel):
    completed: Optional[bool] = None

class SubHabitCompletionCreate(BaseModel):
    user_id: UUID
    sub_habit_id: int
    date: date
    completed: bool

class SubHabitCompletionUpdate(BaseModel):
    completed: Optional[bool] = None
