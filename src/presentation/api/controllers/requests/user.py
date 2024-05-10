from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from transfer.user import ToCreateUserDTO


class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=6, max_length=64)
    about_me: Optional[str]
    password: str = Field(..., min_length=8, max_length=64)

    def convert_to_dto(self) -> ToCreateUserDTO:
        return ToCreateUserDTO(
            email=self.email,
            username=self.username,
            about_me=self.about_me,
            password=self.password,
        )
