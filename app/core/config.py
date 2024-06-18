# app/core/config.py

from starlette.config import Config
from dotenv import load_dotenv

load_dotenv()
config = Config()

# MongoDB Configuration
MONGODB_URI = config("MONGODB_URI")
MONGODB_DB = config("MONGODB_DB")