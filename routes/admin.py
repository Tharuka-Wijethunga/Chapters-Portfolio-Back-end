from fastapi import APIRouter, Depends
from auth.jwt_bearer import JWTBearer

router = APIRouter()

@router.get("/dashboard", dependencies=[Depends(JWTBearer(allowed_roles=["manage-account"]))])
async def admin_dashboard():
    """
    Admin dashboard endpoint. Access is restricted to users with the 'admin' role.
    The JWTBearer dependency handles token validation and role checking.
    """
    return {"message": "Welcome to the admin dashboard!"}