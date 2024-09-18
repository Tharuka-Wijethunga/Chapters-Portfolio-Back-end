from pydantic import BaseModel

class AdminSignIn(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin1", 
                "password": "securepass123"
            }
        }

class AdminData(BaseModel):
    username: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin1",
            }
        }