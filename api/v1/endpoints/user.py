from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from core.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    allow_authenticated,
    Token
)
from models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate
from core.database import get_db

router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    # Check if user exists
    existing_user = await User.find_one(User.email == user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        email=user_in.email,
        fullname=user_in.fullname,
        password=get_password_hash(user_in.password)
    )
    await user.create()
    
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await User.find_one(User.email == form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": create_access_token(user.email, "user"),
        "refresh_token": create_refresh_token(user.email, "user"),
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(allow_authenticated)) -> Any:
    """
    Get current user information.
    """
    user = await User.find_one(User.email == current_user["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/me", response_model=UserResponse)
async def update_user(
    user_update: UserUpdate,
    current_user: dict = Depends(allow_authenticated)
) -> Any:
    """
    Update current user information.
    """
    user = await User.find_one(User.email == current_user["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    
    await user.update({"$set": update_data})
    return user
