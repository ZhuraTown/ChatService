from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchemaRequest(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    password_check: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")


class UserReadSchemaResponse(BaseModel):
    email: str
    name: str
    id: int | str

    class Config:
        from_attributes = True


class UserAuthSchemaRequest(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class AccessTokenSchemaResponse(BaseModel):
    access_token: str
    user: UserReadSchemaResponse


class UsersFilters(BaseModel):
    email__in: list[str] | None = None
    name__in: list[str] | None = None
    search: str | None = None
    id__in: list[int] | None = None
