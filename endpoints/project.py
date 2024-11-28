from fastapi import APIRouter
from sqlmodel import select

from db.config import SessionDep
from models.project.project import Project
from models.project.project_create import ProjectCreate
from models.project.project_public import ProjectPublic
from models.user.user import User
from models.user.user_public import UserPublic
from services.project_service import ProjectService
from services.user_service import UserService

router = APIRouter(prefix="/project", tags=["Project"])


@router.get("/", response_model=list[ProjectPublic])
async def get_all_projects(session: SessionDep):
    return ProjectService.get_all(session)


@router.post("/")
async def create_project(project_create: ProjectCreate, session: SessionDep):
    return await ProjectService.create(project_create, session)


@router.get("/{project_id}", response_model=ProjectPublic)
async def get_project_by_id(project_id: int, session: SessionDep):
    return await ProjectService.get_by_id(project_id, session)


@router.get("/{project_id}/backers", response_model=list[UserPublic])
async def get_project_backers(project_id: int, session: SessionDep):
    return await ProjectService.get_backers(project_id, session)


@router.post("/{project_id}/backer/{user_id}")
async def add_project_backer(project_id: int, user_id: int, session: SessionDep):
    return await ProjectService.add_backer(project_id, user_id, session)
