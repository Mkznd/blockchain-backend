import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

from logging_config import setup_logging

load_dotenv()


from db.config import create_db_and_tables
from endpoints.user import router as user_router
from endpoints.auth import router as auth_router
from endpoints.project import router as project_router

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    logging.info("Application startup")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(project_router)
