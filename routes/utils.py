from fastapi import APIRouter, Body

from schemas.thumbnail import thumbnail
from services.thumbnail_service import generate_thumbnail

router = APIRouter()


@router.post("/generate_thumbnail")
async def user_generate_thumbnail(thumbnail: thumbnail = Body(...)):
    try:
        return generate_thumbnail(thumbnail)
    except Exception as e:
        return {"error": str(e)}
