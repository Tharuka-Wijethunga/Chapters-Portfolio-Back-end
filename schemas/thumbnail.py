from pydantic import BaseModel

class thumbnail(BaseModel):
    title: str
    weburl: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Google",
                "weburl": "https://www.google.com/",
            }
        }