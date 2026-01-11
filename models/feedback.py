from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class Feedback(Document):
    project_id: str
    username: str
    content: str
    rank: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "feedback"
