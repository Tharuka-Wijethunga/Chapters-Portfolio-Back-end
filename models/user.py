from datetime import datetime
from beanie import Document
from pydantic import EmailStr, Field


class User(Document):
    fullname: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "user"
        
    def to_user_data(self):
        return {
            "fullname": self.fullname,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
