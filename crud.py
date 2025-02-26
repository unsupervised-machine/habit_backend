from pprint import pprint

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import DESCENDING, UpdateOne
from pymongo.errors import DuplicateKeyError
from datetime import date as _date
from datetime import timedelta

from db import users_collection, habits_collection, completions_collection
from models import UserCreate, UserUpdate
from models import HabitCreate, HabitUpdate
from models import CompletionCreate, CompletionUpdate

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
        pprint(user)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return jsonable_encoder(user)
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
    try:
        habits = habits_collection.find(
            filter={"user_id": user_id},
            sort=[("sort_index", DESCENDING)],
        )
        return jsonable_encoder(habits)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching the user's habits.")



def get_habit(habit_id: str):
    try:
        habit = habits_collection.find_one(
            filter={"_id": habit_id},
            # sort=[("sort_index", DESCENDING)],
        )
        pprint(habit)
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
        completion = completions_collection.find(
            filter={"completion_id": completion_id},
            sort=[("sort_index", DESCENDING)],
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
        return habits_collection.find_one({"_id": completion_id})

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An error occurred while updating the completion.")


def get_user_habit_completions(user_id: str, habit_id: str):
    try:
        completions = completions_collection.find(
            filter={"habit_id": habit_id, "user_id": user_id},
            sort=[("date", DESCENDING)],
        )
        return jsonable_encoder(completions)
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
        today = _date.today()  # Get today's date

        # Fetch all habits
        habits = habits_collection.find({}, {"_id": 1, "user_id": 1})

        bulk_operations = []

        for habit in habits:
            habit_id = habit["_id"]
            user_id = habit["user_id"]

            # Upsert: Insert if not exists
            bulk_operations.append(
                UpdateOne(
                    {"habit_id": habit_id, "user_id": user_id, "date": today},
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