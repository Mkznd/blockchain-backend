import logging

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette import status

from models.project.project import Project
from models.project.project_create import ProjectCreate
from models.user.user import User


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
