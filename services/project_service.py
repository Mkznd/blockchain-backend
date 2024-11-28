import logging

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette import status

from models.project.project import Project
from models.project.project_create import ProjectCreate
from models.user.user import User

PROJECT_NOT_FOUND = "Project not found"


class ProjectService:
    @staticmethod
    async def create(project_create: ProjectCreate, session: Session):
        project = Project.model_validate(project_create)
        try:
            owner = session.exec(
                select(User).where(User.id == project.owner_id)
            ).first()
            if not owner:
                raise HTTPException(status_code=400, detail="Owner does not exist.")
            session.add(project)
            session.commit()
            session.refresh(project)
        except Exception as e:
            session.rollback()
            logging.error(f"Create failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Create failed: {str(e)}",
            )
        return project

    @staticmethod
    def get_all(session: Session):
        try:
            return session.exec(select(Project)).all()
        except Exception as e:
            logging.error(f"Could not retrieve projects: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not retrieve projects: {str(e)}",
            )

    @staticmethod
    async def get_by_id(project_id: int, session: Session):
        project = session.exec(select(Project).where(Project.id == project_id)).first()
        if not project:
            logging.error(f"Project with id {project_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND
            )
        return project

    @staticmethod
    async def get_backers(project_id: int, session: Session):
        project = session.exec(select(Project).where(Project.id == project_id)).first()
        if not project:
            logging.error(f"Project with id {project_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND
            )
        return project.backers

    @staticmethod
    async def add_backer(project_id: int, user_id: int, session: Session):
        project = session.exec(select(Project).where(Project.id == project_id)).first()
        if not project:
            logging.error(f"Project with id {project_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND
            )
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            logging.error(f"User with id {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        project.backers.append(user)
        session.add(project)
        session.commit()
        session.refresh(project)
        return project
