from fastapi import APIRouter
from fastapi import HTTPException, Response
from pymongo import ReturnDocument
from bson import ObjectId
from database import feedback_collection

feedback = APIRouter()

@feedback.delete("/projects/{projectId}/feedback/{feedbackId}/delete", status_code=204)
async def delete_feedback(feedbackId: str):
    # Check if the feedbackId is a valid ObjectId
    if not ObjectId.is_valid(feedbackId):
        raise HTTPException(status_code=400, detail="Invalid feedbackId")

    # Try to find and delete the feedback
    result = feedback_collection.find_one_and_delete({"_id": ObjectId(feedbackId)})

    # If no feedback was found, raise a 404 error
    if result is None:
        raise HTTPException(status_code=404, detail="Feedback not found")

    # Return a 204 No Content response
    return Response(status_code=204)

@feedback.put("/projects/{projectId}/feedback/{feedbackId}/rank")
async def rank_feedback(feedbackId: str, rank: int):
    # Validate feedbackId is a valid ObjectId
    if not ObjectId.is_valid(feedbackId):
        raise HTTPException(status_code=400, detail="Invalid feedbackId")

    # Update the rank and return the updated document
    updated_feedback = feedback_collection.find_one_and_update(
        {"_id": ObjectId(feedbackId)},  # Filter by feedback ID
        {"$set": {"rank": rank}},  # Only update the rank field
        return_document=ReturnDocument.AFTER  # Return the updated document after update
    )

    # Handle case if feedback is not found
    if updated_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")

    # Return the updated feedback as a dictionary
    return updated_feedback