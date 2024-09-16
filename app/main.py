from fastapi import FastAPI
from app.routers.project import router as project

app = FastAPI(title="AI Portal Backend")

app.include_router(project, prefix="/api/portfolio", tags=["projects"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI Portal Backend"}
