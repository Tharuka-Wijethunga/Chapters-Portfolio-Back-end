from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Project(Document):
    name: str
    description: str
    image: str
    visibility: bool = True
    featured: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "projects"

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    visibility: Optional[bool] = None
    featured: Optional[bool] = None

class ProjectSearch(BaseModel):
    query: str
