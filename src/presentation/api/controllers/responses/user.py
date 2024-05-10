from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    about_me: Optional[str]
