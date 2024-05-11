from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from presentation.api.controllers import BaseResponse
from transfer.user import UserDTO


class UserResponse(BaseResponse):
    id: UUID
    email: EmailStr
    username: str
    about_me: Optional[str]

    @classmethod
    def convert_from_dto(cls, dto: UserDTO):
        return cls(
            id=dto.id,
            email=dto.email,
            username=dto.username,
            about_me=dto.about_me,
        )