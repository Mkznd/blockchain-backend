from models.user.UserBase import UserBase


class UserPublic(UserBase, table=False):
    id: int
