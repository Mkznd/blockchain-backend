import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from passlib.hash import bcrypt

from db.config import SessionDep
from models.user.user import User
from models.user.user_create import UserCreate
from models.user.user_login import UserLogin
from sqlmodel import select

from models.user.user_public import UserPublic
from services.auth_service import AuthService
from services.jwt_service import create_access_token, decode_access_token
from security.jwt_check import check_jwt

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(
    user_create: UserCreate,
    auth_service: Annotated[AuthService, Depends()],
    session: SessionDep,
) -> str:
    """
    Register a new user. Hashes the password before saving.
    """
    user = await auth_service.register(user_create, session)
    access_token = create_access_token({"sub": str(user.id)})

    return access_token


@router.post("/login")
async def login(
    user_data: UserLogin,
    auth_service: Annotated[AuthService, Depends()],
    session: SessionDep,
) -> str:
    """
    Validate username/password, return a JWT if valid.
    """
    user = await auth_service.login(user_data, session)

    # If OK, generate token. Typically, store user id in "sub" (subject)
    access_token = create_access_token({"sub": str(user.id)})

    return access_token


@router.post("/logout")
async def logout() -> dict:
    """
    In JWT-based auth, "logout" is mostly handled client-side
    by discarding the token. This endpoint is optional or
    could store blacklisted tokens if needed.
    """
    return {"message": "Logout successful (client must discard token)"}


@router.get("/me")
async def get_me(session: SessionDep, user_id: int = Depends(check_jwt)) -> UserPublic:
    """
    Returns user info if the Authorization header has a valid JWT.
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing subject (sub)")

    # 4) Fetch user from DB
    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
