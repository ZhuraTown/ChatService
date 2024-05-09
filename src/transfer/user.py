from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserDTO(BaseModel):
    id: UUID
    email: str
    username: str
    about_me: Optional[str]


class ToCreateUserDTO(BaseModel):
    email: str
    username: str
    about_me: Optional[str]
    password: str


class UpdateUserDTO(BaseModel):
    username: str
    about_me: Optional[str]
    password: str


class FilterUserDTO(BaseModel):
    search: Optional[str] = None
    limit: int = 10
    offset: int = 0

