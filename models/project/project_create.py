from models.project.project_base import ProjectBase


class ProjectCreate(ProjectBase):
    owner_id: int
