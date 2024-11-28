from fastapi import APIRouter

from db.config import SessionDep
from models.user.user_create import UserCreate
from services.user_service import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/")
async def get_all_users(session: SessionDep):
    return await UserService.get_all(session)


@router.post("/")
async def create_user(user_create: UserCreate, session: SessionDep):
    return await UserService.create(user_create, session)
