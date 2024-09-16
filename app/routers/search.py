# app/routers/search.py

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.models.project import ProjectInDB
from app.services.search_service import search_projects
from app.dependencies.db_authentication import get_db

router = APIRouter()

@router.get("/projects/search", response_model=List[ProjectInDB])
async def search_projects_endpoint(
    query: Optional[str] = None,
    filter_name: Optional[str] = Query(None, alias="filter[name]"),
    filter_visibility: Optional[bool] = Query(None, alias="filter[visibility]"),
    sort_field: Optional[str] = Query(None, alias="sort[field]"),
    sort_direction: Optional[str] = Query("ascending", alias="sort[direction]"),
    page_number: int = Query(1, alias="page[number]", ge=1),
    page_size: int = Query(10, alias="page[size]", ge=1, le=100),
    db=Depends(get_db)
):
    try:
        results = await search_projects(
            query, 
            filter_name, 
            filter_visibility, 
            sort_field, 
            sort_direction, 
            page_number, 
            page_size, 
            db
        )
        return results
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))