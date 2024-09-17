from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from models.admin import Admin
from models.user import User
from models.student import Student
from models.project import Project

class Settings(BaseSettings):
    # database configurations
    MONGODB_URI: str = None
    MONGODB_DB: str
    # JWT
    secret_key: str = "secret"
    algorithm: str = "HS256"
    expires_in: int = 3600

    class Config:
        env_file = ".env"
        from_attributes = True

async def initiate_database():
    client = AsyncIOMotorClient(Settings().MONGODB_URI)
    await init_beanie(
        database=client[Settings().MONGODB_DB],
        document_models=[Admin, User, Student, Project]
    )