from contextlib import asynccontextmanager
from sqlite3 import IntegrityError

from fastapi import FastAPI, HTTPException

from db.config import create_db_and_tables, SessionDep
from models.user.user import User
from models.user.user_create import UserCreate
from models.user.user_public import UserPublic


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get_all_users(session: SessionDep):
    return session.query(User).all()


@app.post("/user/", response_model=UserPublic)
async def create_user(user_create: UserCreate, session: SessionDep):
    db_user = User.model_validate(user_create)
    session.add(db_user)
    try:
        session.commit()
    except:
        session.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")
    session.refresh(db_user)
    return db_user
