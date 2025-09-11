from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserSignUp(BaseModel):
    fullname: str
    email: EmailStr
    password: str = Field(..., min_length=8)

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
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class KeycloakUser(BaseModel):
    user_id: str
    email: EmailStr
    name: str | None = None
    preferred_username: str
    roles: list[str] = []