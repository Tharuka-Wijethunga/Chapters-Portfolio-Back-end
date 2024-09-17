from fastapi import APIRouter, HTTPException, Query, Body, Depends
from typing import List, Optional
from models.project import Project, ProjectUpdate
from schemas.project import ProjectSchema, ProjectCreateSchema, ProjectUpdateSchema, ProjectListSchema
from database.database import get_projects, get_project, create_project, update_project, delete_project, search_projects, set_featured_status
from auth.jwt_bearer import JWTBearer

router = APIRouter()

admin_jwt_bearer = JWTBearer(allowed_roles=["admin"])
user_jwt_bearer = JWTBearer(allowed_roles=["user", "admin"])



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

@router.get("/{id}", response_model=ProjectSchema)
async def get_project_by_id(id: str):
    project = await get_project(id)
    if project:
        return ProjectSchema.from_orm(project)
    raise HTTPException(status_code=404, detail="Project not found")

@router.post("/create", response_model=ProjectSchema, dependencies=[Depends(user_jwt_bearer)])
async def create_new_project(project: ProjectCreateSchema):
    new_project = Project(**project.dict())
    created_project = await create_project(new_project)
    return ProjectSchema.from_orm(created_project)

@router.put("/{id}", response_model=ProjectSchema, dependencies=[Depends(user_jwt_bearer)])
async def update_existing_project(id: str, project_update: ProjectUpdateSchema):
    updated_project = await update_project(id, ProjectUpdate(**project_update.dict(exclude_unset=True)))
    if updated_project:
        return ProjectSchema.from_orm(updated_project)
    raise HTTPException(status_code=404, detail="Project not found")

@router.delete("/{id}", status_code=204, dependencies=[Depends(user_jwt_bearer)])
async def delete_existing_project(id: str):
    deleted = await delete_project(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")

@router.get("/search", response_model=List[ProjectSchema])
async def search_projects_by_query(query: str):
    projects = await search_projects(query)
    return [ProjectSchema.from_orm(project) for project in projects]

@router.put("/{id}/featured", response_model=ProjectSchema, dependencies=[Depends(admin_jwt_bearer)])
async def set_project_featured_status(id: str, featured: bool = Body(...)):
    updated_project = await set_featured_status(id, featured)
    if updated_project:
        return ProjectSchema.from_orm(updated_project)
    raise HTTPException(status_code=404, detail="Project not found")