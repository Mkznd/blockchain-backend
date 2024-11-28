from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from models.association_tables.project_backer_link import ProjectBackerLink
from models.project.project_base import ProjectBase
from models.project.project_status import ProjectStatus
from models.user.user import User

if TYPE_CHECKING:
    from models.user.user import User


class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    status: ProjectStatus = Field(default=ProjectStatus.active)

    owner_id: int = Field(foreign_key="user.id", nullable=False)
    owner: User = Relationship(
        back_populates="projects",
    )

    backers: list["User"] = Relationship(
        back_populates="backed_projects",
        link_model=ProjectBackerLink,
    )
