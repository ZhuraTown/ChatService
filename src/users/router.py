from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse

from db.orm import User
from users.auth import create_access_token
from users.dependency import get_user_service, get_current_user
from users.schemas import (
    UserRegisterSchemaRequest, UserReadSchemaResponse,
    UserAuthSchemaRequest, AccessTokenSchemaResponse, UsersFilters,
)
from users.service import UserService

users_api_router = APIRouter(prefix='/api/users', tags=['users'])
templates = Jinja2Templates(directory='templates')

users_router = APIRouter(prefix='/auth', tags=['auth-page'])


@users_router.get("", response_class=HTMLResponse, summary="Страница авторизации")
async def auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@users_api_router.post(
    '/register',
    status_code=HTTPStatus.CREATED,
    response_model=UserReadSchemaResponse
)
async def register_user(
        data: UserRegisterSchemaRequest,
        service: Annotated[UserService, Depends(get_user_service)],
):
    new_user = await service.register(data.model_dump(mode='json'))
    return UserReadSchemaResponse.model_validate(new_user)


@users_api_router.post(
    "/login",
    status_code=HTTPStatus.CREATED,
    response_model=AccessTokenSchemaResponse,
)
async def login(
        auth_data: UserAuthSchemaRequest,
        service: Annotated[UserService, Depends(get_user_service)],
):
    auth_user = await service.authenticate(auth_data.email, auth_data.password)
    access_token = create_access_token({"sub": str(auth_user.id)})
    return AccessTokenSchemaResponse(
        access_token=access_token,
        user=UserReadSchemaResponse.model_validate(auth_user)
    )


@users_api_router.get(
    "/me",
    status_code=HTTPStatus.OK,
    response_model=UserReadSchemaResponse,
)
async def me(
        auth_user: Annotated[User, Depends(get_current_user)]
):
    return UserReadSchemaResponse.model_validate(auth_user)


@users_api_router.post(
    "",
    response_model=list[UserReadSchemaResponse],
    dependencies=[
        Depends(get_current_user),
    ]
)
async def get_users(
        service: Annotated[UserService, Depends(get_user_service)],
        filters: UsersFilters
):
    users = await service.list_users(filters.model_dump(mode='json', exclude_none=True))
    return [UserReadSchemaResponse.model_validate(u) for u in users]