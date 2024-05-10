from src.infrastructure.db.models.users import User
from src.transfer.user import UserDTO, ToCreateUserDTO, UserFullDTO


def convert_user_dbmodel_to_dto(user: User) -> UserDTO | None:
    if not user:
        return

    return UserDTO(
        id=user.id,
        email=user.email,
        username=user.username,
        about_me=user.about_me
    )


def convert_user_dbmodel_to_full_dto(user: User) -> UserDTO | None:
    if not user:
        return

    return UserFullDTO(
        id=user.id,
        email=user.email,
        username=user.username,
        about_me=user.about_me,
        password=user.password
    )


def convert_user_dto_to_dbmodel(user: UserDTO) -> User:
    return User(
        id=user.id,
        email=user.email,
        username=user.username,
        about_me=user.about_me
    )


def convert_created_user_to_dbmodel(user: ToCreateUserDTO) -> User:

    return User(
        email=user.email,
        username=user.username,
        about_me=user.about_me,
        password=user.password
    )
