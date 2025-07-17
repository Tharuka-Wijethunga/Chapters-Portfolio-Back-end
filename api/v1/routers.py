from fastapi import APIRouter
from routes import admin, user, project, utils

api_router = APIRouter()

api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
api_router.include_router(project.router, prefix="/projects", tags=["Project"])
api_router.include_router(utils.router, prefix="/utils", tags=["Utils"])
