from typing import Protocol
from uuid import UUID

from src.application.services.interfaces.base import (
    CreateServiceInterfaceMixin,
    UpdateServiceInterfaceMixin,
    GetServiceInterfaceMixin,
    ListServiceInterfaceMixin,
    SoftDeleteServiceInterfaceMixin,
)
from src.transfer.user import (
    ToCreateUserDTO,
    UserDTO,
    UpdateUserDTO,
    FilterUserDTO, UpdateUserPasswordDTO,
)


class UserServiceI(
    CreateServiceInterfaceMixin[ToCreateUserDTO, UserDTO],
    UpdateServiceInterfaceMixin[UpdateUserDTO, UserDTO],
    GetServiceInterfaceMixin[UserDTO],
    ListServiceInterfaceMixin[FilterUserDTO, UserDTO],
    SoftDeleteServiceInterfaceMixin,
):
    async def change_password(
            self,
            user_id: UUID,
            update_data: UpdateUserPasswordDTO
    ) -> UserDTO:
        raise NotImplementedError
