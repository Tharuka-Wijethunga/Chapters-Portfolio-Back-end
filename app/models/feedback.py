from pydantic import BaseModel

class Feedback(BaseModel):
    comment : str
    rank: int