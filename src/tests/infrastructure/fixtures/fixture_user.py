import pytest
from faker import Faker

from src.infrastructure.db.models.users import User
from src.infrastructure.db.repositories.user import UserRepository


@pytest.fixture()
def get_user_data(
        faker: Faker,
):
    return {
        "email": faker.email(),
        "username": f"username:{faker.word()}",
        "about_me": faker.paragraph(),
        "hash_password": faker.password(),
    }


@pytest.fixture()
async def get_user(
        get_user_data: dict,
):
    user = User(**get_user_data)
    await user.insert()
    return user


@pytest.fixture()
def get_repository_user():
    return UserRepository()
