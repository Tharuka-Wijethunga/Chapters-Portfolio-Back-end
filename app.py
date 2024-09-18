from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from config.config import initiate_database
from routes.admin import router as AdminRouter
from routes.user import router as UserRouter
from routes.project import router as ProjectRouter
from routes.utils import router as UtilsRouter
from auth.jwt_bearer import JWTBearer

app = FastAPI()


app.add_event_handler("startup", initiate_database)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to 'Chapters' Portfolio backend API !"}

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(AdminRouter, tags=["Admins"], prefix="/admin")
app.include_router(UserRouter, tags=["Users"], prefix="/user")
app.include_router(ProjectRouter, tags=["Projects"], prefix="/projects")
app.include_router(UtilsRouter, tags=["Utilities"], prefix="/utils")
# app.include_router(FeedbackRouter, tags=["Feedbacks"], prefix="/feedback", dependencies=[Depends(JWTBearer(allowed_roles=["user", "admin"]))])
