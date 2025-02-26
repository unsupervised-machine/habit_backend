from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError

from db import users_collection
from models import User, UserCreate, UserUpdate

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with that information already exists.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the user.")


def get_user(user_id: str):
    try:
        # Retrieve the user document from the collection.
        user = users_collection.find_one({"_id": user_id})
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return jsonable_encoder(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching the user.")


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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )

