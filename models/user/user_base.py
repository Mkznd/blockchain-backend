from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
