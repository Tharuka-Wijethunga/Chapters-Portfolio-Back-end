from typing import Optional
from pydantic import BaseModel


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


class FeedbackResponse(BaseModel):
    id: str
    project_id: str
    content: str
    rank: Optional[int] = None
