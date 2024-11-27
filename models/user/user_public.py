from models.user.user_base import UserBase


class UserPublic(UserBase, table=False):
    id: int
