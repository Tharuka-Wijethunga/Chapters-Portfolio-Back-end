# app/services/search_service.py

from app.models.project import ProjectInDB
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional, List

async def search_projects(
    query: Optional[str],
    filter_name: Optional[str],
    filter_visibility: Optional[bool],
    sort_field: Optional[str],
    sort_direction: str,
    page_number: int,
    page_size: int,
    db: AsyncIOMotorDatabase
) -> List[ProjectInDB]:
    # Build the filter
    filter_query = {}
    if query:
        filter_query["$text"] = {"$search": query}
    if filter_name:
        filter_query["name"] = {"$regex": filter_name, "$options": "i"}
    if filter_visibility is not None:
        filter_query["visibility"] = filter_visibility

    # Build the sort
    sort_params = []
    if sort_field:
        if sort_field not in ["date", "name"]:
            raise ValueError("Invalid sort field. Must be 'date' or 'name'.")
        sort_direction = 1 if sort_direction.lower() == "ascending" else -1
        sort_params.append((sort_field, sort_direction))
    
    # If text search is used, sort by relevance first
    if query:
        sort_params.insert(0, ("score", {"$meta": "textScore"}))

    # Perform the query
    cursor = db.projects.find(
        filter_query,
        {"score": {"$meta": "textScore"}} if query else None
    )
    
    if sort_params:
        cursor = cursor.sort(sort_params)

    # Apply pagination
    total_count = await cursor.count()
    cursor = cursor.skip((page_number - 1) * page_size).limit(page_size)

    projects = []
    async for doc in cursor:
        projects.append(ProjectInDB(
            id=str(doc["_id"]),
            name=doc["name"],
            description=doc["description"],
            image=doc["image"],
            visibility=doc["visibility"]
        ))

    return projects  # This returns a list of ProjectInDB objects