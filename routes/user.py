from fastapi import APIRouter, Body, HTTPException, Depends
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt
from auth.jwt_bearer import JWTBearer
from auth.security import get_current_user_id
from models.user import User
from schemas.user import UserSignUp, UserSignIn
from database.user import *

from services.keycloak import get_all_users, get_user_by_id
from schemas.keycloak import KeycloakUser as keycloak_user
from typing import List


router = APIRouter()
hash_helper = CryptContext(schemes=["bcrypt"])

user_jwt_bearer = JWTBearer(allowed_roles=["user", "admin"])

@router.get("/keycloak-users", response_model=List[keycloak_user], tags=["Keycloak User"])
async def keycloak_users():
    return get_all_users()

@router.get("/keycloak-user/{user_id}", response_model=keycloak_user, tags=["Keycloak User"])
async def keycloak_user(user_id: str):
    return get_user_by_id(user_id)

@router.post("/signup")
async def user_signup(user: UserSignUp = Body(...)):
    user_exists = await get_user(user.email)
    if user_exists:
        raise HTTPException(
            status_code=409, detail="User with this email already exists"
        )
    hashed_password = hash_helper.encrypt(user.password)
    user = User(fullname=user.fullname, email=user.email, password=hashed_password)
    new_user = await add_user(user)
    return {"message": "User created successfully"}

@router.post("/login")
async def user_login(user_credentials: UserSignIn = Body(...)):
    user = await get_user(user_credentials.email)
    if user:
        password = hash_helper.verify(
            user_credentials.password, user.password
        )
        if password:
            return sign_jwt(user.email, role="user")
        raise HTTPException(
            status_code=403, detail="Incorrect email or password"
        )
    raise HTTPException(
        status_code=403, detail="Incorrect email or password"
    )

@router.get("/dashboard", dependencies=[Depends(user_jwt_bearer)])
async def user_dashboard():
    return {"message": "Welcome to the user dashboard!"}