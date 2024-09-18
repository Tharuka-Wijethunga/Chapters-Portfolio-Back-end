from typing import List, Optional
from bson import ObjectId

from models.project import Project, ProjectUpdate


async def get_projects(
    name: Optional[str] = None,
    visibility: Optional[bool] = None,
    sort_field: Optional[str] = None,
    sort_direction: str = "ascending",
    page: int = 1,
    page_size: int = 10
) -> List[Project]:
    filter_params = {}
    if name:
        filter_params["name"] = {"$regex": name, "$options": "i"}
    if visibility is not None:
        filter_params["visibility"] = visibility

    sort_params = {}
    if sort_field:
        sort_params[sort_field] = 1 if sort_direction == "ascending" else -1

    skip = (page - 1) * page_size

    projects = await Project.find(filter_params).sort(sort_params).skip(skip).limit(page_size).to_list()
    return projects

async def get_project(id: ObjectId) -> Optional[Project]:
    return await Project.get(id)

async def create_project(project: Project) -> Project:
    return await project.insert()

async def update_project(id: ObjectId, project_update: ProjectUpdate) -> Optional[Project]:
    project = await Project.get(id)
    if project:
        await project.update({"$set": project_update.dict(exclude_unset=True)})
        return project
    return None

async def delete_project(id: ObjectId) -> bool:
    project = await Project.get(id)
    if project:
        await project.delete()
        return True
    return False

async def search_projects(query: str) -> List[Project]:
    projects = await Project.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ],
        "visibility": True
    }).to_list()
    return projects

async def set_featured_status(id: str, featured: bool) -> Optional[Project]:
    project = await Project.get(ObjectId(id))
    if project:
        project.featured = featured
        await project.save()
        return project
    return None