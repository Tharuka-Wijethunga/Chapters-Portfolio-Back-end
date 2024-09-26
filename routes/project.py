from fastapi import APIRouter, HTTPException, Query, Body, Depends, Response
from typing import List, Optional
from bson import ObjectId

from auth.jwt_bearer import JWTBearer
from models.project import Project, ProjectUpdate
from models.feedback import Feedback
from schemas.project import *
from schemas.feedback import FeedbackUpdate, FeedbackResponse
from database.project import *
from database.feedback import *

router = APIRouter()

admin_jwt_bearer = JWTBearer(allowed_roles=["admin"])
user_jwt_bearer = JWTBearer(allowed_roles=["user", "admin"])


# Project routes

@router.get("/all", response_model=ProjectListSchema)
async def list_projects(
    name: Optional[str] = Query(None),
    visibility: Optional[bool] = Query(None),
    sort_field: Optional[str] = Query(None),
    sort_direction: Optional[str] = Query("ascending"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    projects = await get_projects(name, visibility, sort_field, sort_direction, page, page_size)
    total = await Project.count()
    return ProjectListSchema(
        projects=[ProjectSchema.from_orm(project) for project in projects],
        total=total,
        page=page,
        page_size=page_size
    )

@router.get("/{projectId}", response_model=ProjectSchema)
async def get_project_by_id(projectId: str):
    project = await get_project(projectId)
    if project:
        return ProjectSchema.from_orm(project)
    raise HTTPException(status_code=404, detail="Project not found")

@router.post("/create", response_model=ProjectSchema, dependencies=[Depends(user_jwt_bearer)])
async def create_new_project(project: ProjectCreateSchema):
    new_project = Project(**project.dict())
    created_project = await create_project(new_project)
    return ProjectSchema.from_orm(created_project)

@router.put("/{projectId}", response_model=ProjectSchema, dependencies=[Depends(user_jwt_bearer)])
async def update_existing_project(projectId: str, project_update: ProjectUpdateSchema):
    updated_project = await update_project(projectId, ProjectUpdate(**project_update.dict(exclude_unset=True)))
    if updated_project:
        return ProjectSchema.from_orm(updated_project)
    raise HTTPException(status_code=404, detail="Project not found")

@router.delete("/{projectId}", status_code=204, dependencies=[Depends(user_jwt_bearer)])
async def delete_existing_project(projectId: str):
    deleted = await delete_project(projectId)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")

@router.get("/search", response_model=List[ProjectSchema])
async def search_projects_by_query(query: str):
    projects = await search_projects(query)
    return [ProjectSchema.from_orm(project) for project in projects]

@router.put("/{projectId}/featured", response_model=ProjectSchema, dependencies=[Depends(admin_jwt_bearer)])
async def set_project_featured_status(projectId: str, featured: bool = Body(...)):
    updated_project = await set_featured_status(projectId, featured)
    if updated_project:
        return ProjectSchema.from_orm(updated_project)
    raise HTTPException(status_code=404, detail="Project not found")


# Feedback routes

@router.post("/{projectId}/feedback", response_model=FeedbackResponse, dependencies=[Depends(user_jwt_bearer)])
async def add_feedback(projectId: str, feedback: str):
   # Validate projectId
    if not ObjectId.is_valid(projectId):
        raise HTTPException(status_code=400, detail="Invalid projectId")
    
    # Check if project exists
    project = await Project.get(ObjectId(projectId))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create new feedback
    new_feedback = Feedback(project_id=projectId, content=feedback)

    try:
        await new_feedback.insert()
        if not new_feedback.id:
            raise HTTPException(status_code=404, detail="Failed to save feedback")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    # Return the newly created feedback as the response
    return FeedbackResponse(**new_feedback.dict())

@router.delete("/feedback/{feedbackId}/delete", status_code=204, dependencies=[Depends(user_jwt_bearer)])
async def delete_feedback(feedbackId: str):
    if not ObjectId.is_valid(feedbackId):
        raise HTTPException(status_code=400, detail="Invalid feedbackId")

    feedback = await Feedback.get(ObjectId(feedbackId))
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")

    await feedback.delete()
    return Response(status_code=204)

@router.put("/feedback/{feedbackId}/rank", response_model=FeedbackResponse, dependencies=[Depends(admin_jwt_bearer)])
async def rank_feedback(feedbackId: str, rank_update: FeedbackUpdate):
    if not ObjectId.is_valid(feedbackId):
        raise HTTPException(status_code=400, detail="Invalid feedbackId")

    feedback = await Feedback.get(ObjectId(feedbackId))
    if feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")

    feedback.rank = rank_update.rank
    await feedback.save()

    return FeedbackResponse(**feedback.dict())