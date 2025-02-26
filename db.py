from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

# Create a MongoDB client
client = MongoClient(MONGO_URI)

# Access the database
db = client[DATABASE_NAME]

# Collections
users_collection = db["users"]
habits_collection = db["habits"]
completions_collection = db["completions"]