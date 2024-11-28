import logging

from fastapi import HTTPException, status
from sqlmodel import Session, select
from passlib.hash import bcrypt

from models.user.user import User
from models.user.user_create import UserCreate

USER_NOT_FOUND = "User not found"


class UserService:

    @staticmethod
    async def create(user_create: UserCreate, session: Session):
        # Hash the password before saving
        hashed_password = bcrypt.hash(user_create.password)
        db_user = User(
            username=user_create.username,
            name=user_create.name,
            email=user_create.email,
            password=hashed_password,
        )
        session.add(db_user)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"User creation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User creation failed: {str(e)}",
            )
        session.refresh(db_user)
        return db_user

    @staticmethod
    async def get_all(session: Session):
        try:
            users = session.exec(select(User)).all()
            return users
        except Exception as e:
            logging.error(f"Could not retrieve users: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not retrieve users: {str(e)}",
            )

    @staticmethod
    async def get_by_id(user_id: int, session: Session):
        user = session.get(User, user_id)
        if not user:
            logging.error(f"User with id {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
            )
        return user

    @staticmethod
    async def update(user_id: int, user_data: UserCreate, session: Session):
        user = session.get(User, user_id)
        if not user:
            logging.error(f"User with id {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
            )

        for key, value in user_data.dict(exclude_unset=True).items():
            if key == "password":  # Hash the new password if updated
                value = bcrypt.hash(value)
            setattr(user, key, value)

        try:
            session.add(user)
            session.commit()
            session.refresh(user)
        except Exception as e:
            session.rollback()
            logging.error(f"Update failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Update failed: {str(e)}",
            )
        return user

    @staticmethod
    async def delete(user_id: int, session: Session):
        user = session.get(User, user_id)
        if not user:
            logging.error(f"User with id {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
            )
        try:
            session.delete(user)
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Delete failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Delete failed: {str(e)}",
            )
        return user

    @staticmethod
    async def get_projects(user_id: int, session: Session):
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            logging.error(f"User with id {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
            )
        return user.projects
