from dataclasses import dataclass
from uuid import UUID

from src.application.common.exceptions import ToClientException


@dataclass(eq=False)
class UserNotExistError(ToClientException):
    id: UUID

    @property
    def message(self) -> str:
        return f"User with id:{self.id} not exist!"


@dataclass(eq=False)
class UsernameAlreadyExistError(ToClientException):
    username: str

    @property
    def message(self) -> str:
        return f"User with username:{self.username} already exist!"


@dataclass(eq=False)
class EmailAlreadyExistError(ToClientException):
    email: str

    @property
    def message(self) -> str:
        return f"User with email:{self.email} already exist!"
