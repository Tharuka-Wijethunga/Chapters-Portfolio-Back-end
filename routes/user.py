from fastapi import APIRouter, Body, HTTPException, Depends, status
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt
from auth.jwt_bearer import JWTBearer
from models.user import User
from schemas.user import UserSignUp, UserSignIn, UserData, TokenResponse
from database.user import get_user, add_user

router = APIRouter()
hash_helper = CryptContext(schemes=["bcrypt"])

user_jwt_bearer = JWTBearer(allowed_roles=["user", "admin"])


@router.post("/signup", response_model=UserData, status_code=status.HTTP_201_CREATED)
async def user_signup(user: UserSignUp = Body(...)):
    """
    Create new user account.
    """
    user_exists = await get_user(user.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    hashed_password = hash_helper.hash(user.password)
    new_user = User(
        fullname=user.fullname,
        email=user.email,
        password=hashed_password
    )
    
    created_user = await add_user(new_user)
    return UserData(**created_user.to_user_data())


@router.post("/login", response_model=TokenResponse)
async def user_login(user_credentials: UserSignIn = Body(...)):
    """
    Login for existing users.
    """
    user = await get_user(user_credentials.email)
    if user and hash_helper.verify(user_credentials.password, user.password):
        token_data = sign_jwt(user.email, role="user")
        return TokenResponse(**token_data)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/me", response_model=UserData, dependencies=[Depends(user_jwt_bearer)])
async def get_current_user_info(current_user: dict = Depends(user_jwt_bearer)):
    """
    Get current authenticated user's information.
    """
    user = await get_user(current_user["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserData(**user.to_user_data())


@router.get("/dashboard", dependencies=[Depends(user_jwt_bearer)])
async def user_dashboard():
    """
    User dashboard endpoint.
    """
    return {"message": "Welcome to the user dashboard!"}
