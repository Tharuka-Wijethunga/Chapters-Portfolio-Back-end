from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


# class Response(BaseModel):
#     status_code: int
#     response_type: str
#     description: str
#     data: Optional[Any]

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "status_code": 200,
#                 "response_type": "success",
#                 "description": "Operation successful",
#                 "data": "Sample data",
#             }
#         }

class FeedbackUpdate(BaseModel):
    rank: int

    class Config:
        json_schema_extra = {
            "example": {
                "rank": 1,
            }
        }


class FeedbackCreate(BaseModel):
    username: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "jane.doe",
                "content": "Great project!",
            }
        }


class FeedbackResponse(BaseModel):
    id: PydanticObjectId
    project_id: str
    username: str
    content: str
    created_at: datetime
    rank: Optional[int] = None

    class Config:
        from_attributes = True
