# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.dependencies.db_authentication import connect_to_mongo, close_mongo_connection
from app.routers import handle_utils
from app.routers.project import router as project

app = FastAPI(title="AI Portal Backend")

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Routers
app.include_router(handle_utils.router, prefix="/utils", tags=["Utils"])
app.include_router(project, prefix="/api/portfolio", tags=["projects"])


# Events
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)