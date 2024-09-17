from beanie import Document
from pydantic import BaseModel

class Admin(Document):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {                
                "username": "admin1",                
                "password": "securepass123",            
            }
        }

    class Settings:
        name = "admin"

class AdminSignIn(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {"username": "admin1", "password": "securepass123"}
        }