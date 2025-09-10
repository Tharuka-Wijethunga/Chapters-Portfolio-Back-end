from fastapi import APIRouter, Depends
from typing import List

from auth.jwt_bearer import JWTBearer
from services.keycloak import get_all_users, get_user_by_id
from schemas.keycloak import KeycloakUser as keycloak_user

router = APIRouter()

@router.get("/keycloak-users", response_model=List[keycloak_user], dependencies=[Depends(JWTBearer(allowed_roles=[]))])
async def keycloak_users():
    return get_all_users()

@router.get("/keycloak-user/{user_id}", response_model=keycloak_user, dependencies=[Depends(JWTBearer(allowed_roles=[]))])
async def keycloak_user(user_id: str):
    return get_user_by_id(user_id)

@router.get("/dashboard", dependencies=[Depends(JWTBearer(allowed_roles=["view-profile"]))])
async def user_dashboard():
    return {"message": "Welcome to the user dashboard!"}