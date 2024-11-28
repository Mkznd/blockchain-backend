from fastapi import APIRouter, Depends, HTTPException
from db.config import SessionDep
from models.user.user_create import UserCreate
from models.user.user_public import UserPublic
from services.user_service import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=UserPublic)
async def get_all_users(session: SessionDep):
    return await UserService.get_all(session)


@router.get("/{user_id}", response_model=UserPublic)
async def get_user_by_id(user_id: int, session: SessionDep):
    return await UserService.get_by_id(user_id, session)


@router.post("/", response_model=UserPublic)
async def create_user(user_create: UserCreate, session: SessionDep):
    return await UserService.create(user_create, session)


@router.put("/{user_id}", response_model=UserPublic)
async def update_user(user_id: int, user_create: UserCreate, session: SessionDep):
    return await UserService.update(user_id, user_create, session)


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: SessionDep):
    return await UserService.delete(user_id, session)
