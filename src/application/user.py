from uuid import UUID

from src.infrastructure.db.convertors.user import convert_created_user_to_dbmodel
from src.infrastructure.db.repositories.interfaces.user import UserRepositoryI
from src.application.services.exceptions.user import (
    EmailAlreadyExistError,
    UserNotExistError,
    UsernameAlreadyExistError,
)
from src.transfer.user import (
    UserDTO,
    ToCreateUserDTO,
    UpdateUserDataDTO,
    UpdateUserPasswordDTO,
    UserFullDTO, FilterUserDTO,
)


class ValidateUserDataMixin:
    _user_repository: UserRepositoryI

    async def validate_user_data(self, user_data: ToCreateUserDTO):

        if await self._user_repository.get_user_by_email(user_data.email):
            raise EmailAlreadyExistError(user_data.email)

        if await self._user_repository.get_user_by_username(user_data.username):
            raise UsernameAlreadyExistError(user_data.username)


class UserService(
    ValidateUserDataMixin
):

    def __init__(self, user_repository):
        self._user_repository: UserRepositoryI = user_repository

    async def count(
            self,
            filters: FilterUserDTO,
    ) -> int:
        count = await self._user_repository.count(filters)
        return count

    async def create(
            self,
            user_data: ToCreateUserDTO,
    ) -> UserDTO:

        await self.validate_user_data(user_data)
        # todo: add later hash password
        user = await self._user_repository.create(
            convert_created_user_to_dbmodel(user_data)
        )
        return user

    async def get(
            self,
            id: UUID,
    ) -> UserDTO | None:
        user = await self._user_repository.get(id)
        if not user:
            raise UserNotExistError(id)
        return user

    async def update(
            self,
            id: UUID,
            update_data: UpdateUserDataDTO
    ) -> UserDTO:
        user = await self._user_repository.get(id)
        if not user:
            raise UserNotExistError(id)
        await self._user_repository.update(id, update_data)
        return await self.get(id)

    async def list(
            self,
            filters: FilterUserDTO
    ) -> list[UserDTO]:
        users = await self._user_repository.list(filters)
        return users

    async def soft_delete(
            self,
            id: UUID,
    ):
        user = await self._user_repository.get(id)
        if not user:
            raise UserNotExistError(id)
        await self._user_repository.delete(id)

    async def change_password(
            self,
            user_id: UUID,
            update_data: UpdateUserPasswordDTO,
    ) -> UserDTO:
        user = await self._user_repository.get(user_id)
        if not user:
            raise UserNotExistError(user_id)
        await self._user_repository.update(user_id, update_data)
        return await self.get(user_id)

    async def check_password(
            self,
            email: str | None,
            username: str | None,
            password: str
    ) -> bool:

        if email:
            user = await self._user_repository.get_user_by_email(email)
        elif username:
            user = await self._user_repository.get_user_by_username(username)

        return user.password == password



