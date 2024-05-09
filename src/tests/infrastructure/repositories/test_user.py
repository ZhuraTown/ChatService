from src.infrastructure.db.models.users import User
from src.infrastructure.db.repositories.interfaces.user import UserRepositoryI
from src.transfer.user import UserDTO


class TestUserRepository:

    async def test_create_user(
            self,
            get_user_data: dict,
            get_repository_user: UserRepositoryI

    ):
        user = User(**get_user_data)
        created_user = await get_repository_user.create(user)

        assert created_user
        assert created_user.id
        assert created_user.email == user.email
        assert created_user.username == user.username
        assert created_user.about_me == user.about_me
        assert isinstance(created_user, UserDTO)

    async def test_get_user(
            self,
            get_user: User,
            get_repository_user: UserRepositoryI
    ):
        founded_user = await get_repository_user.get(get_user.id)

        assert founded_user
        assert founded_user.id
        assert founded_user.email == get_user.email
        assert founded_user.username == get_user.username
        assert founded_user.about_me == get_user.about_me
        assert isinstance(founded_user, UserDTO)
