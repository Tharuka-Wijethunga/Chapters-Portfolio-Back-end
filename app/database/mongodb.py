from motor.motor_asyncio import AsyncIOMotorClient
from app.config.database import database_settings

client = AsyncIOMotorClient(database_settings.MONGODB_URL)
db = client[database_settings.DATABASE_NAME]