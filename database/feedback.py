from typing import Union
from beanie import PydanticObjectId

from models.feedback import Feedback


async def add_feedback(feedback: Feedback) -> Feedback:
    await feedback.insert()
    return feedback

async def delete_feedback(id: PydanticObjectId) -> bool:
    feedback = await Feedback.get(id)
    if feedback:
        await feedback.delete()
        return True
    return False

async def update_feedback_rank(id: PydanticObjectId, rank: int) -> Union[Feedback, None]:
    feedback = await Feedback.get(id)
    if feedback:
        feedback.rank = rank
        await feedback.save()
        return feedback
    return None