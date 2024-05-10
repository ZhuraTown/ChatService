from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from application.common.exceptions import ToClientException
from application.services.exceptions.user import EmailAlreadyExistError
from application.services.interfaces.user import UserServiceI
from presentation.api.controllers.requests.user import CreateUserRequest
from presentation.api.controllers.responses.user import UserResponse
from presentation.api.deps.services import get_user_service


router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_current_user)],
)


@router.post(
    "/",
    description="Регистрация",
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
)
async def register_user(
    new_user: CreateUserRequest,
    service: Annotated[UserServiceI, Depends(get_user_service)],
):
    user = await service.create(new_user.convert_to_dto())
    return user


@router.get(
    "/{user_id}",
    description="Получить пользователя",
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
)
async def get_user(
        user_id: UUID,
        service: Annotated[UserServiceI, Depends(get_user_service)],
):
    user = await service.get(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return user
