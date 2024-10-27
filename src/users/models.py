from uuid import UUID

from sqlmodel import SQLModel, Field


__all__ = [
    "User",
    "UserRead",
    "UserCreate",
]

from src.db.mixin import TimestampMixin, OIDMixin


class UserBase(SQLModel):
    email: str | None = Field(None, min_length=2, max_length=100)
    username: str = Field(unique=True)
    name: str | None = Field(None, min_length=2, max_length=100)


class HashPassword(SQLModel):
    hash_password: str


class CreatePassword(SQLModel):
    password: str = Field(min_length=6, max_length=128)


class User(
    OIDMixin,
    TimestampMixin,
    UserBase,
    HashPassword,
    table=True
):
    pass


class UserCreate(UserBase, CreatePassword):
    email: str | None = Field(None, min_length=2, max_length=100)
    username: str = Field(unique=True)
    name: str | None = Field(None, min_length=2, max_length=100)


class UserRead(UserBase):
    id: UUID
