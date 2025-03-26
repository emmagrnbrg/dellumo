from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from ..Database import getDbSession
from ..entities.UserEntity import UserEntity
from ..models.UserModel import UpdatePasswordRequestModel
from ..routers.AuthorizationRouter import getCurrentActiveUser
from ..services.UserService import UserService

router = APIRouter(prefix="/user")


@router.post("/change-password")
async def changePassword(requestBody: Annotated[UpdatePasswordRequestModel, Body()],
                         user: Annotated[UserEntity, Depends(getCurrentActiveUser)],
                         session: Session = Depends(getDbSession)) -> None:
    """
    Заменить пароль у авторизованного пользователя

    :param requestBody: тело запроса
    :param user: данные пользователя
    :param session: сессия БД
    """
    UserService(session).changePassword(user, requestBody.password)
