from typing import List, Optional
from bson import ObjectId

from models.project import Project, ProjectUpdate
from core.database import get_database


async def get_projects() -> List[Project]:
    try:
        projects = await Project.find_all().to_list()
        return projects
    except Exception as e:
        print(f"Error getting projects: {e}")
        raise


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
    projects = await Project.find(
        {
            "$and": [
                {
                    "$or": [
                        {"topic": {"$regex": query, "$options": "i"}},
                        {"description": {"$regex": query, "$options": "i"}}
                    ]
                },
                {"visibility": True}
            ]
        }
    ).to_list()
    return projects


async def set_featured_status(id: str, featured: bool) -> Optional[Project]:
    project = await Project.get(ObjectId(id))
    if project:
        project.featured = featured
        await project.save()
        return project
    return None
