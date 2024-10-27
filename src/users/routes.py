from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from src.users.dependencies import get_user_service
from src.users.models import UserCreate
from src.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post(
    "/registration",
    status_code=HTTPStatus.CREATED
)
async def register_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    user_data: UserCreate
):
    return await user_service.create(user_data)
