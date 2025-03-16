from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.src.Database import getDbSession
from backend.src.entities.UserEntity import UserEntity
from backend.src.models.AuthorizationModel import TokenResponseModel, RefreshTokenRequestModel
from backend.src.services.AuthorizationService import AuthorizationService

router = APIRouter()


# аутентификация
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="JWT", auto_error=False)


async def getCurrentActiveUser(token: str | None = Depends(oauth2Scheme),
                               session: Session = Depends(getDbSession)) -> UserEntity:
    """
    Получить данные текущего авторизованного пользователя

    :param token: токен пользователя
    :param session: сессия соединения с БД
    :return: данные пользователя
    """
    return AuthorizationService(session).getCurrentUser(token)


@router.post("/login")
def login(payload: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(getDbSession)) -> TokenResponseModel:
    """
    Аутентификация пользователя в систему

    :param payload: данные формы для аутентификации
    :param session: сессия соединения с БД
    :return: refresh & access-токены
    """
    return AuthorizationService(session).login(payload.username, payload.password)


@router.post("/token/refresh")
async def refreshToken(request: Annotated[RefreshTokenRequestModel, Body()],
                       session: Session = Depends(getDbSession)) -> TokenResponseModel:
    """
    Запрос на обновление access-токена пользователя

    :param request: тело запроса
    :param session: сессия соединения с БД
    :return: access & refresh токены доступа
    """
    return AuthorizationService(session).refreshToken(request.token)
