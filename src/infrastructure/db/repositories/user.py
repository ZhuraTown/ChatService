from uuid import UUID
from datetime import datetime, UTC

from beanie.odm.operators.update.general import Set

from src.infrastructure.db.convertors.user import convert_user_dbmodel_to_dto, convert_user_dbmodel_to_full_dto
from src.infrastructure.db.models.users import User
from src.transfer.user import UserDTO, UpdateUserDTO, FilterUserDTO


class UserRepository:
    async def create(
            self,
            user: User
    ) -> UserDTO:
        await user.insert()
        return await self.get(user.id)

    async def get(
            self,
            id: UUID,
    ) -> UserDTO | None:
        user = await User.find(User.id == id, User.deleted_at == None).first_or_none()
        return convert_user_dbmodel_to_dto(user)

    async def update(
            self,
            id: UUID,
            update_data: UpdateUserDTO
    ) -> UserDTO:
        # todo: fix me later deleted_at
        user = await User.find(User.id == id, User.deleted_at == None).first_or_none()
        await user.set(update_data.get_data())
        return await self.get(id)

    async def list(
            self,
            filters: FilterUserDTO
    ) -> list[UserDTO]:
        users = await (User.find(User.deleted_at == None,
                                 limit=filters.limit,
                                 skip=filters.offset)
                       .to_list())
        return [convert_user_dbmodel_to_dto(user) for user in users]

    async def delete(
            self,
            id: UUID
    ):
        user = await User.find(User.id == id, User.deleted_at == None).first_or_none()
        await user.update(Set({User.deleted_at: datetime.now(tz=UTC)}))

    async def get_user_by_email(
            self,
            email: str
    ) -> UserDTO | None:
        user = await User.find(User.email == email).first_or_none()
        return convert_user_dbmodel_to_full_dto(user)

    async def get_user_by_username(
            self,
            username: str
    ) -> UserDTO | None:
        user = await User.find(User.username == username).first_or_none()
        return convert_user_dbmodel_to_full_dto(user)

    async def count(
            self,
            filters: FilterUserDTO
    ) -> int:
        count = await (User.find(User.deleted_at == None,
                                 limit=filters.limit,
                                 skip=filters.offset)
                       .count())
        return count
