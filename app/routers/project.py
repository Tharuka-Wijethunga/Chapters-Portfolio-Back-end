from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional
from app.models.project import ProjectModel, ProjectUpdate, ProjectSearch, get_projects_pipeline, search_projects_pipeline
from app.database.mongodb import db
from bson import ObjectId

router = APIRouter()

@router.get("/projects", response_model=List[ProjectModel])
async def get_projects(
    name: Optional[str] = Query(None),
    visibility: Optional[bool] = Query(None),
    sort_field: Optional[str] = Query(None),
    sort_direction: Optional[str] = Query("ascending"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    filter_params = {}
    if name:
        filter_params["name"] = name
    if visibility is not None:
        filter_params["visibility"] = visibility

    sort_params = None
    if sort_field:
        sort_params = {"field": sort_field, "direction": sort_direction}

    pipeline = get_projects_pipeline(filter_params, sort_params, page, page_size)
    projects = await db.projects.aggregate(pipeline).to_list(length=None)
    return [ProjectModel(**project) for project in projects]

@router.get("/projects/{id}", response_model=ProjectModel)
async def get_project(id: str):
    project = await db.projects.find_one({"_id": ObjectId(id)})
    if project:
        return ProjectModel(**project)
    raise HTTPException(status_code=404, detail="Project not found")

@router.post("/projects", response_model=ProjectModel)
async def create_project(project: ProjectModel):
    project_dict = project.model_dump(by_alias=True, exclude={"id"})
    new_project = await db.projects.insert_one(project_dict)
    created_project = await db.projects.find_one({"_id": new_project.inserted_id})
    return ProjectModel(**created_project)

@router.put("/projects/{id}", response_model=ProjectModel)
async def update_project(id: str, project_update: ProjectUpdate):
    update_data = project_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    updated_project = await db.projects.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True
    )
    
    if updated_project:
        return ProjectModel(**updated_project)
    raise HTTPException(status_code=404, detail="Project not found")

@router.delete("/projects/{id}", status_code=204)
async def delete_project(id: str):
    delete_result = await db.projects.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")

@router.get("/projects/search", response_model=List[ProjectModel])
async def search_projects(query: str):
    pipeline = search_projects_pipeline(query)
    projects = await db.projects.aggregate(pipeline).to_list(length=None)
    return [ProjectModel(**project) for project in projects]

@router.put("/projects/{id}/featured", response_model=ProjectModel)
async def set_featured_status(id: str, featured: bool = Body(...)):
    updated_project = await db.projects.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"featured": featured, "updated_at": datetime.utcnow()}},
        return_document=True
    )
    
    if updated_project:
        return ProjectModel(**updated_project)
    raise HTTPException(status_code=404, detail="Project not found")