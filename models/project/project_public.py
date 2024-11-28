from sqlmodel import Field

from models.project.project_base import ProjectBase
from models.project.project_status import ProjectStatus


class ProjectPublic(ProjectBase):
    id: int
    status: ProjectStatus
    owner_id: int
