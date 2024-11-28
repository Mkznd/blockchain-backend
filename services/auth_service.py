from fastapi import HTTPException
from passlib.handlers.bcrypt import bcrypt
from sqlmodel import Session, select
from starlette import status

from models.user.user import User
from models.user.user_create import UserCreate
from models.user.user_login import UserLogin
from services.user_service import UserService


class AuthService:
    @staticmethod
    async def register(user_create: UserCreate, session: Session):
        existing_user = session.exec(
            select(User).where(User.username == user_create.username)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        return await UserService.create(user_create, session)

    @staticmethod
    async def login(user_login: UserLogin, session: Session):
        user = session.exec(
            select(User).where(User.username == user_login.username)
        ).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid username or password",
            )

        if not bcrypt.verify(user_login.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        return user
