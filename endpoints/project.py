from fastapi import APIRouter
from sqlmodel import select

from db.config import SessionDep
from models.project.project import Project
from models.project.project_create import ProjectCreate
from models.project.project_public import ProjectPublic
from models.user.user import User
from services.project_service import ProjectService
from services.user_service import UserService

router = APIRouter(prefix="/project", tags=["Project"])


@router.get("/", response_model=list[ProjectPublic])
async def get_all_projects(session: SessionDep):
    return ProjectService.get_all(session)


@router.post("/")
async def create_project(project_create: ProjectCreate, session: SessionDep):
    return await ProjectService.create(project_create, session)
