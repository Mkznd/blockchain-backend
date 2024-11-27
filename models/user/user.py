from fastapi import HTTPException
from sqlmodel import Field, Session, select

from models.user.user_base import UserBase
from models.user.user_create import UserCreate


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str

    @staticmethod
    async def create(user_create: UserCreate, session: Session):
        db_user = User.model_validate(user_create)
        session.add(db_user)
        try:
            session.commit()
        except:
            session.rollback()
            raise HTTPException(status_code=400, detail="Username already exists")
        session.refresh(db_user)
        return db_user

    @staticmethod
    async def get_all(session: Session):
        return session.exec(select(User)).all()
