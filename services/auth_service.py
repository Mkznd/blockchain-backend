import logging

from fastapi import HTTPException
from passlib.handlers.bcrypt import bcrypt
from sqlmodel import Session, select
from starlette import status

from models.user.user import User
from models.user.user_create import UserCreate
from models.user.user_login import UserLogin
from services.user_service import UserService

INVALID_USERNAME_PASSWORD = "Invalid username or password"
USERNAME_ALREADY_EXISTS = "Username already exists"


class AuthService:
    @staticmethod
    async def register(user_create: UserCreate, session: Session):
        existing_user = session.exec(
            select(User).where(User.username == user_create.username)
        ).first()
        if existing_user:
            logging.error(USERNAME_ALREADY_EXISTS)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=USERNAME_ALREADY_EXISTS,
            )
        return await UserService.create(user_create, session)

    @staticmethod
    async def login(user_login: UserLogin, session: Session):

        user = session.exec(
            select(User).where(User.username == user_login.username)
        ).first()
        if not user:
            logging.error(INVALID_USERNAME_PASSWORD)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=INVALID_USERNAME_PASSWORD,
            )

        if not bcrypt.verify(user_login.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_USERNAME_PASSWORD,
            )

        return user
