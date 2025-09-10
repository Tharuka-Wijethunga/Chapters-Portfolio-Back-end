from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings

from models.feedback import Feedback
from models.project import Project


class Settings(BaseSettings):
    # database configurations
    MONGODB_URI: str = None
    MONGODB_DB: str

    KEYCLOAK_URL: str = None
    REALM: str = None
    CLIENT_ID: str = None
    CLIENT_SECRET: str = None

    class Config:
        env_file = ".env"
        from_attributes = True

async def initiate_database():
    client = AsyncIOMotorClient(Settings().MONGODB_URI)
    await init_beanie(
        database=client[Settings().MONGODB_DB],
        document_models=[Feedback, Project]
    )

settings = Settings()