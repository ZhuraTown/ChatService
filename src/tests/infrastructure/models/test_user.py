from faker import Faker

from src.infrastructure.db.models.users import User


class TestUserModel:

    async def test_create_user(
            self,
            faker: Faker
    ):
        data = {"email": faker.email(), "username": f'username:{faker.word()}',
                "about_me": faker.paragraph(), "password": faker.password()}
        user = User(**data)

        await user.insert()

        assert user
        assert user.id
        assert user.email == data['email']
        assert user.username == data['username']
        assert user.about_me == data['about_me']
        assert user.password == data['password']
        assert user.created_at

