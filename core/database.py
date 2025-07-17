from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from models.admin import Admin
from models.user import User
from models.feedback import Feedback
from models.project import Project
from core.config import settings

# Global database client
client = AsyncIOMotorClient(settings.MONGODB_URI)


async def init_db():
    """Initialize database connection and set up ODM."""
    try:
        await init_beanie(
            database=client[settings.MONGODB_DB],
            document_models=[Admin, User, Feedback, Project]
        )
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e


async def close_db_connection():
    """Close database connection."""
    client.close()


def get_database():
    """Get database instance."""
    return client[settings.MONGODB_DB]
