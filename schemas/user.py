from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignUp(BaseModel):
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

class UserData(BaseModel):
    fullname: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Tharindu S",
                "email": "tharindus@example.com",
            }
        }