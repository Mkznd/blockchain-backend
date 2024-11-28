from sqlmodel import Field

from models.user.user_base import UserBase


class UserCreate(UserBase):
    password: str = Field(min_length=8)
