from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "ai_portal"

    class Config:
        env_file = ".env"

database_settings = DatabaseSettings()