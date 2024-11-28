from sqlmodel import SQLModel, Field


class ProjectBackerLink(SQLModel, table=True):
    project_id: int = Field(foreign_key="project.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)
