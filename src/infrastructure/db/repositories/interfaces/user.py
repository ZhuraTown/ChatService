from src.infrastructure.db.models.users import User
from src.infrastructure.db.repositories.interfaces.base import (
    CreateRepositoryInterfaceMixin,
    UpdateRepositoryInterfaceMixin,
    GetRepositoryInterfaceMixin,
    ListRepositoryInterfaceMixin,
    DeleteRepositoryInterfaceMixin,
)
from src.transfer.user import (UserDTO, UpdateUserDTO, FilterUserDTO)


class UserRepositoryI(
    CreateRepositoryInterfaceMixin[User, UserDTO],
    UpdateRepositoryInterfaceMixin[UpdateUserDTO, UserDTO],
    GetRepositoryInterfaceMixin[UserDTO],
    ListRepositoryInterfaceMixin[FilterUserDTO, UserDTO],
    DeleteRepositoryInterfaceMixin,
):
    ...
