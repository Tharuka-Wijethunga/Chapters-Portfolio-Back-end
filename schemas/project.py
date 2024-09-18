from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from beanie import PydanticObjectId

class ProjectSchema(BaseModel):
    id: PydanticObjectId
    name: str
    description: str
    image: str
    visibility: bool
    featured: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes=True

class ProjectCreateSchema(BaseModel):
    name: str
    description: str
    image: str
    visibility: bool = True
    featured: bool = False

class ProjectUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    visibility: Optional[bool] = None
    featured: Optional[bool] = None

class ProjectListSchema(BaseModel):
    projects: List[ProjectSchema]
    total: int
    page: int
    page_size: int