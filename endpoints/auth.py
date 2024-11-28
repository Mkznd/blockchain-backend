from fastapi import APIRouter
from db.config import SessionDep
from models.user.user_create import UserCreate
from models.user.user_login import UserLogin
from models.user.user_public import UserPublic
from services.auth_service import AuthService
from services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserPublic)
async def register(user_create: UserCreate, session: SessionDep):
    return await AuthService.register(user_create, session)


@router.post("/login", response_model=UserPublic)
async def login(user_login: UserLogin, session: SessionDep):
    return await AuthService.login(user_login, session)
