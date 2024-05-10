from abc import abstractmethod, ABC
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.infrastructure.db.models.users import User


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


class UpdateUserDTO(BaseModel, ABC):

    @abstractmethod
    def get_data(self):
        raise NotImplementedError


class UpdateUserDataDTO(UpdateUserDTO):
    about_me: Optional[str]

    def get_data(self):
        return {User.about_me: self.about_me}


class UpdateUserPasswordDTO(UpdateUserDTO):
    password: str

    def get_data(self):
        return {User.password: self.password}


class FilterUserDTO(BaseModel):
    search: Optional[str] = None
    limit: int = 10
    offset: int = 0

