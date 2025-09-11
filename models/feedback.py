from typing import Optional
from beanie import Document


class Feedback(Document):
    project_id: str
    content: str
    rank: Optional[int] = None

    class Settings:
        name = "feedback"
