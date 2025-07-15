from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db, close_db_connection
from core.config import settings
from routes.admin import router as AdminRouter
from routes.user import router as UserRouter
from routes.project import router as ProjectRouter
from routes.utils import router as UtilsRouter

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Chapters Portfolio",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Database event handlers
@app.on_event("startup")
async def startup_db_client():
    await init_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db_connection()

# Include routers
app.include_router(AdminRouter, prefix="/admin", tags=["Admin"])
app.include_router(UserRouter, prefix="/user", tags=["User"])
app.include_router(ProjectRouter, prefix="/projects", tags=["Projects"])
app.include_router(UtilsRouter, prefix="/utils", tags=["Utils"])

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs",
        "version": "1.0.0"
    }
