import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()


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
    return await User.get_all(session)


@app.post("/user/", response_model=UserPublic)
async def create_user(user_create: UserCreate, session: SessionDep):
    return await User.create(user_create, session)
