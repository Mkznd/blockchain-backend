from sqlmodel import Field, Relationship

from models.association_tables.project_backer_link import ProjectBackerLink
from models.user.user_base import UserBase

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.project.project import Project


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str

    projects: list["Project"] = Relationship(
        back_populates="owner", cascade_delete=True
    )

    backed_projects: list["Project"] = Relationship(
        back_populates="backers", link_model=ProjectBackerLink
    )
