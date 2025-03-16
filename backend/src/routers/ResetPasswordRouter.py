from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from backend.src.Database import getDbSession
from backend.src.models.OperationModel import OperationResponseModel
from backend.src.models.ResetPasswordModel import PasswordRecoveryRequestModel, ResetPasswordRequestModel
from backend.src.services.ResetPasswordService import ResetPasswordService

router = APIRouter(prefix="/reset-password")


@router.post("/start")
async def start(requestBody: Annotated[PasswordRecoveryRequestModel, Body()],
                session: Session = Depends(getDbSession)) -> OperationResponseModel:
    """
    Создание заявки на восстановление пароля пользователя

    :param requestBody: тело запроса
    :param session: сессия БД
    :return: uuid созданной заявки
    """
    return OperationResponseModel(uuid=ResetPasswordService(session).start(requestBody.email))


@router.post("/{uuid}/verify")
async def verify(uuid: str,
                 requestBody: Annotated[ResetPasswordRequestModel, Body()],
                 session: Session = Depends(getDbSession)) -> None:
    """
    Верификация одноразового кода для подтверждения восстановления пароля

    :param uuid: uuid операции
    :param requestBody: тело запроса
    :param session: сессия БД
    """
    ResetPasswordService(session).verify(uuid, requestBody.operation.code, requestBody.password)
