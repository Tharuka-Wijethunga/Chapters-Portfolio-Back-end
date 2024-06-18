# app/routers/utils.py

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pymongo.mongo_client import MongoClient
from fastapi.encoders import jsonable_encoder
import json

from app.dependencies.db_authentication import get_database
from app.services.thumbnail_service import generate_thumbnail


router = APIRouter()


@router.get("/test_database")
async def test_database_connection(
    db: MongoClient = Depends(get_database)
):
    try:
        db.server_info()
        return {"status": "Connection successful"}
    except Exception as e:
        return {"error": str(e)}
    

@router.get("/execute_mongodb_query")
async def execute_mongodb_query(
    query: str = Query(..., title="MongoDB Query"),
    db: MongoClient = Depends(get_database),
):
    try:
        query_dict = json.loads(query)
        result = db.command(query_dict)
        return result
    except Exception as e:
        return {"error": str(e)}

# http://127.0.0.1:8000/execute_mongodb_query?query={"insert":"SocialMedia","documents":[{"sm_id":"SM01","name":"Facebook"},{"sm_id":"SM02","name":"Instagram"}]}


@router.get("/generate_thumbnail")
async def generate_thumbnail(
    width: int = Query(..., title="Width of the thumbnail"),
    height: int = Query(..., title="Height of the thumbnail"),
):
    try:
        thumbnail = await generate_thumbnail(width, height)
        return thumbnail
    except Exception as e:
        return {"error": str(e)}