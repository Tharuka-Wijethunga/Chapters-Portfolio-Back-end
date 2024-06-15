from fastapi import APIRouter
from bson import ObjectId

from models.feedback import Feedback

feedback = APIRouter()

@feedback.delete("/projects/{projectId}/feedback/{feedbackId}/delete")
async def delete_feedback(projectId: str, feedbackId: str):
    # .find_one_and_delete({"_id": ObjectId(feedbackId)})
    return {"message": "Deleted", "projectId" : projectId, "feedbackId" : feedbackId}

@feedback.put("/projects/{projectId}/feedback/{feedbackId}/rank")
async def rank_feedback(projectId: str, feedbackId: str, rank: int):
    # .find_one_and_update({"_id": ObjectId(feedbackId)}, {"$set": dict(rank)})
    return {"message": "Rank Updated", "projectId" : projectId, "feedbackId" : feedbackId}