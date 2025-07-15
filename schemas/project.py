from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel


class ProjectSchema(BaseModel):
    id: PydanticObjectId
    topic: str
    description: str
    batch: str
    contributors: List[str]
    search_tags: List[str]
    date: datetime
    image: str
    width: int
    height: int
    visibility: bool
    featured: bool
    created_at: datetime


    class Config:
        from_attributes = True


class ProjectCreateSchema(BaseModel):
    topic: str
    description: str
    batch: str
    contributors: List[str]
    search_tags: List[str]
    date: datetime
    image: str
    width: int
    height: int
    visibility: bool = True
    featured: bool = True


class ProjectUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    visibility: Optional[bool] = None
    featured: Optional[bool] = None


class ProjectListSchema(BaseModel):
    projects: List[ProjectSchema]
