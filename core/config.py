from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chapters Portfolio API"
    
    # MongoDB settings
    MONGODB_URI: str
    MONGODB_DB: str
    
    # Keycloak Settings
    KEYCLOAK_URL: str
    REALM: str
    CLIENT_ID: str
    CLIENT_SECRET: str

    # Auth toggles
    DISABLE_AUTH: bool = True
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:3000",  # React default port
        "http://localhost:8000",  # FastAPI default port
    ]
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
