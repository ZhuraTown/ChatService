from dataclasses import dataclass
from fastapi.exceptions import ValidationException


class ToClientException(ValidationException):
    errors: str = "Validation errors"

    @property
    def message(self):
        return self.errors


@dataclass
class UserWithEmailExists(ToClientException):
    email: str

    @property
    def message(self):
        return f"Почта {self.email} уже занята другим пользователем"


@dataclass
class UsersNotFound(ToClientException):
    errors = "Переданы несуществующие пользователи"


@dataclass
class UserNotBelongChat(ToClientException):
    errors = "У пользователя нет доступа к чату"


@dataclass
class IncorrectEmailOrPasswordException(ToClientException):
    errors: str = "Неверная почта или пароль"


@dataclass
class TokenNotValid(ToClientException):
    errors = 'Токен не валидный!'
