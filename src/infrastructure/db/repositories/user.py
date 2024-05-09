from uuid import UUID

from src.infrastructure.db.convertors.user import convert_user_dbmodel_to_dto
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
        user = await User.get(id)
        return convert_user_dbmodel_to_dto(user)

    async def update(
            self,
            id: UUID,
            update_data: UpdateUserDTO
            ):
        ...

    async def list(
            self,
            filters: FilterUserDTO
    ):
        ...