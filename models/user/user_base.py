from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    name: str = Field(index=True, min_length=2, max_length=100)
    email: EmailStr = Field(index=True)
