from common.exceptions import UserWithEmailExists, IncorrectEmailOrPasswordException
from common.uow import SQLAlchemyUoW
from db.orm import User
from users.auth import get_password_hash, verify_password
from users.repo import UserRepository


class UserService:

    async def _email_exists(self, email: str):
        found_user = await self.user_repo.find_by({"email": email})
        if found_user:
            raise UserWithEmailExists(email)

    def __init__(
            self,
            user_repo,
            uow: SQLAlchemyUoW
    ):
        self.user_repo: UserRepository = user_repo
        self.uow = uow

    async def register(
            self,
            data: dict
    ) -> User:
        await self._email_exists(data['email'])
        new_user = {
            "email": data['email'],
            "name": data['name'],
            'hashed_password': get_password_hash(data['password'])
        }
        user = await self.user_repo.create(new_user)
        await self.uow.commit()
        return user

    async def authenticate(
            self,
            email: str,
            password: str
    ) -> User:
        user = await self.user_repo.find_by({"email": email})
        if not user:
            raise IncorrectEmailOrPasswordException()
        if not verify_password(password, user.hashed_password):
            raise IncorrectEmailOrPasswordException()
        return user

    async def list_users(self, filter_by: dict) -> list[User]:
        users = await self.user_repo.list(filter_by)
        return users
