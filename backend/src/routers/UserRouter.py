from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from backend.src.Database import getDbSession
from backend.src.entities.UserEntity import UserEntity
from backend.src.models.UserModel import UpdatePasswordRequestModel
from backend.src.routers.AuthorizationRouter import getCurrentActiveUser
from backend.src.services.UserService import UserService

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
