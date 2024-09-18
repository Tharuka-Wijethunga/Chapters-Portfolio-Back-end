from beanie import Document
from pydantic import BaseModel, EmailStr

class User(Document):
    fullname: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Tharindu S",
                "email": "tharindus@example.com",
                "password": "securepass123",
            }
        }

    class Settings:
        name = "user"

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "tharindus@example.com", 
                "password": "securepass123"
            }
        }