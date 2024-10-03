from typing import List

from pydantic import BaseModel

from crypto.database.models import Favorite

class UserCreateSchema(BaseModel):
    name: str

class UserCreatePublic(UserCreateSchema):
    id: int


class UserListSchema(BaseModel):
    id: int
    name: str
    favorites: List['UserFavoritePublic']


class UserFavoriteSchema(BaseModel):
    user_id: int
    symbol: str

class UserFavoritePublic(UserFavoriteSchema):
    id: int

class MessageSchema(BaseModel):
    message: str


class DaySummarySchema(BaseModel):
    highest: float
    lowest: float
    symbol: str