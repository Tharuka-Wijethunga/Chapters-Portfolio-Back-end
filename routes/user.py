from typing import List

from fastapi import APIRouter, Depends

from auth.jwt_bearer import JWTBearer
from schemas.keycloak import KeycloakUser
from services.keycloak import get_all_users, get_user_by_id

router = APIRouter()


@router.get(
    "/keycloak-users",
    response_model=List[KeycloakUser],
    dependencies=[Depends(JWTBearer(allowed_roles=[]))],
)
async def keycloak_users():
    return get_all_users()


@router.get(
    "/keycloak-user/{user_id}",
    response_model=KeycloakUser,
    dependencies=[Depends(JWTBearer(allowed_roles=[]))],
)
async def keycloak_user(user_id: str):
    return get_user_by_id(user_id)


@router.get("/me", response_model=dict)
async def get_current_user_info(payload: dict = Depends(JWTBearer(allowed_roles=["view-profile", "manage-account"]))):
    """
    Get current authenticated user's information directly from the JWT payload.
    """
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "name": payload.get("name"),
        "preferred_username": payload.get("preferred_username"),
        "roles": payload.get("resource_access", {}).get("account", {}).get("roles", [])
    }


@router.get("/dashboard", dependencies=[Depends(JWTBearer(allowed_roles=["view-profile", "manage-account"]))])
async def user_dashboard():
    """
    User dashboard endpoint, accessible to users with 'user' or 'admin' roles.
    """
    return {"message": "Welcome to the user dashboard!"}