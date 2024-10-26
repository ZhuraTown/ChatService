from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[UUID] = Field(primary_key=True, default=None)
    email: str | None = Field(None, min_length=2, max_length=100)
    username: str
    name: str | None = Field(None, min_length=2, max_length=100)
