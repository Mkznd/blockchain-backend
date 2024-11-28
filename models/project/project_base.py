from sqlmodel import SQLModel


class ProjectBase(SQLModel):
    name: str
    description: str
