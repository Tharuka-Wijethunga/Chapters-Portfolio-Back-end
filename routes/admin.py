from fastapi import APIRouter, Body, HTTPException, Depends
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt
from auth.jwt_bearer import JWTBearer
from database.admin import *
from schemas.admin import AdminSignIn

router = APIRouter()
hash_helper = CryptContext(schemes=["bcrypt"])

admin_jwt_bearer = JWTBearer(allowed_roles=["admin"])


@router.post("/login")
async def admin_login(admin_credentials: AdminSignIn = Body(...)):
    admin = await get_admin(admin_credentials.username)
    if admin:
        password = hash_helper.verify(
            admin_credentials.password, admin.password
        )
        if password:
            return sign_jwt(admin.username, role="admin")
        raise HTTPException(
            status_code=403, detail="Incorrect username or password"
        )
    raise HTTPException(
        status_code=403, detail="Incorrect username or password"
    )


@router.get("/dashboard", dependencies=[Depends(admin_jwt_bearer)])
async def admin_dashboard():
    return {"message": "Welcome to the admin dashboard!"}
