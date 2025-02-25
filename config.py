import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
