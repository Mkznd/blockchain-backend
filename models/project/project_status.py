from enum import Enum


class ProjectStatus(str, Enum):
    active = "active"
    paused = "paused"
    completed = "completed"
    deleted = "deleted"
