import uuid
from pprint import pprint

from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from pymongo import DESCENDING, UpdateOne
from pymongo.errors import DuplicateKeyError
from datetime import date as _date
from datetime import timedelta, datetime
from jwt.exceptions import InvalidTokenError
from typing import Annotated


from db import users_collection, habits_collection, completions_collection
from password_tools import verify_password, create_access_token, decode_token, oauth2_scheme, get_password_hash
from models import TokenData
from models import User, UserCreate, UserUpdate
from models import HabitCreate, HabitUpdate
from models import CompletionCreate, CompletionUpdate, CompletionUpsert


# ----------------------
# User Auth Operations
# ----------------------
def register_user(user_form: UserCreate):
    user_data = {
        **user_form.model_dump(exclude={"password"}),
        "hashed_password": get_password_hash(user_form.password)
    }
    result = users_collection.insert_one(user_data)
    return {"id": str(result.inserted_id)}





def authenticate_user(email: str, password: str):
    """
    uses user email and password to fetch user details (including _id)
    :param email:
    :param password:
    :return:
    """
    user = get_user_by_email(email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Extracts the user from a JWT token without OAuth2 dependency."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


# ----------------------
# User CRUD Operations
# ----------------------
def create_user(user: UserCreate):
    # Convert the Pydantic model to a JSON-serializable dict.
    user_data = jsonable_encoder(user)

    try:
        result = users_collection.insert_one(user_data)
        # Convert ObjectId to string before returning
        return {"id": str(result.inserted_id)}
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with that email already exists.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")


def get_user(user_id: str):
    try:
        # Retrieve the user document from the collection.
        user = users_collection.find_one({"_id": user_id})
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return jsonable_encoder(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while fetching the user: {str(e)}")


def get_user_by_email(email: str):
    try:
        # Retrieve the user document from the collection.
        user = users_collection.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return User(**jsonable_encoder(user))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while fetching the user: {str(e)}")



def update_user(user_id: str, user: UserUpdate):
    # Convert the Pydantic model to a dict, excluding fields that were not provided
    update_data = user.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided.")

    try:
        # Perform the update using the $set operator to update only provided fields.
        result = users_collection.update_one({"_id": user_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return users_collection.find_one({"_id": user_id})

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while updating the user.")


def delete_user(user_id: str):
    try:
        result = users_collection.delete_one({"_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return {"message": "User deleted successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting user: {str(e)}")


# ----------------------
# Habit CRUD Operations
# ----------------------
def create_habit(habit: HabitCreate):
    habit_data = jsonable_encoder(habit)

    # Find the current highest sort_index
    max_sort_index = habits_collection.find_one(
        filter={"user_id": habit_data["user_id"]},
        sort=[("sort_index", DESCENDING)],
        projection={"sort_index": 1}
    )
    # Determine new sort_index
    highest_sort_index = max_sort_index.get("sort_index", 0) if max_sort_index else 0
    habit_data["sort_index"] = highest_sort_index + 1  # Ensure it's the highest

    try:
        result = habits_collection.insert_one(habit_data)
        # Convert ObjectId to string before returning
        return {"id": str(result.inserted_id)}
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Habit with that id already exists.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the habit.")


def get_user_habits(user_id: str):
    # Returns list of dict objects
    try:
        habits = habits_collection.find(
            filter={"user_id": user_id},
            sort=[("sort_index", DESCENDING)],
        )
        return list(habits)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching the user's habits.")


def get_user_dashboard_data(user_id: str):
    """
    Retrieves all active habits (not archived) for a given user_id and fetches their completion values for today's date.

    Make sure to run prepare_completions at least once a day to avoid null completed values.
    :param user_id:
    :return:
    """
    today_date = _date.today().strftime("%Y-%m-%d")

    # Fetch all habits that are not archived for the given user_id
    habits = list(habits_collection.find(filter={"user_id": user_id, "archived": {"$ne": True}}))

    habit_ids = [habit["_id"] for habit in habits]


    # Fetch today's completions for the retrieved habit_ids
    completions = completions_collection.find(filter={"habit_id": {"$in": habit_ids}, "date": today_date},
                                      projection={"habit_id": 1, "completed": 1, "_id": 0})


    completion_map = {completion["habit_id"]: completion["completed"] for completion in completions}

    # Attach completion values and date to habits
    for habit in habits:
        habit["completed"] = completion_map.get(habit["_id"], None)
        habit["today_date"] = today_date

    return habits



def get_habit(habit_id: str):
    try:
        habit = habits_collection.find_one(
            filter={"_id": habit_id},
            # sort=[("sort_index", DESCENDING)],
        )
        return jsonable_encoder(habit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while fetching the habit.")


def update_habit(habit_id: str, habit: HabitUpdate):
    update_data = habit.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided.")

    try:
        result = habits_collection.update_one({"_id": habit_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found.")
        return habits_collection.find_one({"_id": habit_id})

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while updating the habit.")


def delete_habit(habit_id: str):
    try:
        result = habits_collection.delete_one({"_id": habit_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habit not found.")
        return {"message": "Habit deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while deleting habit.")


# ----------------------
# Completion CRUD Operations
# ----------------------
def create_completion(completion: CompletionCreate):
    completion_data = jsonable_encoder(completion)

    try:
        result = completions_collection.insert_one(completion_data)
        # Convert ObjectId to string before returning
        return {"id": str(result.inserted_id)}
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Completion with that id already exists.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the completion.")


def get_completion(completion_id: str):
    try:
        completion = completions_collection.find_one(
            filter={"_id": completion_id},
        )
        return jsonable_encoder(completion)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while fetching the completion.")


def update_completion(completion_id: str, completion: CompletionUpdate):
    update_data = completion.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided.")

    try:
        result = completions_collection.update_one({"_id": completion_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Completion not found.")
        return completions_collection.find_one({"_id": completion_id})

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while updating the completion.")


def upsert_completion(request: CompletionUpsert):
    timestamp = datetime.now()

    upsert_object = {
        "habit_id": request.habit_id,
        "user_id": request.user_id,
        "date": request.date,
    }

    update_fields = {
        "$set": {
            "completed": request.completed,
            "timestamp": timestamp
        }
    }

    result = completions_collection.update_one(upsert_object, update_fields, upsert=True)

    return {"message": f"Attempted upsert with habit_id: {request.habit_id}, user_id: {request.user_id}, date {request.date}"}







def get_user_habit_completions(user_id: str, habit_id: str):
    try:
        # need to convert Cursor object to list
        completions = completions_collection.find(
            filter={"habit_id": habit_id, "user_id": user_id},
            sort=[("date", DESCENDING)],
        )

        return list(completions)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while fetching the completions.")


def get_user_habit_completion_streak(user_id: str, habit_id: str):
    try:
        today = _date.today()  # Get today's date (date object)

        # Fetch completions sorted by date (most recent first)
        completions = completions_collection.find(
            {"habit_id": habit_id, "user_id": user_id, "completed": True},
            sort=[("date", DESCENDING)]
        )

        streak = 0
        expected_date = today  # Start checking from today

        for completion in completions:
            completion_date = completion["date"]
            if isinstance(completion_date, str):
                completion_date = datetime.strptime(completion_date, "%Y-%m-%d").date()

            if completion_date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)  # Move to the previous day
            elif completion_date < expected_date:  # Gap found, streak breaks
                break

        return {"streak": streak}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while calculating the streak: {str(e)}"
        )


def prepare_completions():
    # If a completion for today exists, it won’t be modified.
    # If a completion for today doesn’t exist, it creates a new one.
    try:
        # today = _date.today()  # Get today's date
        # today_datetime = datetime.now()
        today_str = _date.today().strftime("%Y-%m-%d")


        # Fetch all habits
        habits = habits_collection.find({}, {"_id": 1, "user_id": 1})

        bulk_operations = []

        for habit in habits:
            habit_id = habit["_id"]
            user_id = habit["user_id"]

            # Upsert: Insert if not exists
            bulk_operations.append(
                UpdateOne(
                    {"habit_id": habit_id, "user_id": user_id, "date": today_str},
                    {"$setOnInsert": {"completed": False}},
                    upsert=True
                )
            )

        if bulk_operations:
            completions_collection.bulk_write(bulk_operations)

        return {"message": "Today's completions prepared successfully."}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while preparing completions: {str(e)}"
        )