from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from ..Database import getDbSession
from ..models.OperationModel import OperationResponseModel, OperationVerifyRequestModel
from ..models.RegistrationModel import RegistrationRequestModel
from ..services.RegistrationService import RegistrationService

router = APIRouter(prefix="/registration")


@router.post("/start")
async def start(requestBody: Annotated[RegistrationRequestModel, Body()],
                session: Session = Depends(getDbSession)) -> OperationResponseModel:
    """
    Создание заявки на регистрацию пользователя

    :param requestBody: тело запроса
    :param session: сессия БД
    :return: uuid созданной заявки
    """
    return OperationResponseModel(uuid=RegistrationService(session).start(requestBody))


@router.post("/{uuid}/verify")
async def verify(uuid: str,
                 requestBody: Annotated[OperationVerifyRequestModel, Body()],
                 session: Session = Depends(getDbSession)) -> None:
    """
    Верификация одноразового кода для подтверждения верификации

    :param uuid: uuid операции
    :param requestBody: тело запроса
    :param session: сессия БД
    """
    RegistrationService(session).verify(uuid, requestBody.code)
