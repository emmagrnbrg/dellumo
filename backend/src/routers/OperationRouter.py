from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.src.Database import getDbSession
from backend.src.services.OperationService import OperationService

router = APIRouter(prefix="/operation")


@router.get("/{uuid}/resent")
async def resent(uuid: str,
                 session: Session = Depends(getDbSession)) -> None:
    """
    Повторная отправка одноразового кода

    :param uuid: uuid операции
    :param session: сессия БД
    """
    OperationService(session).resent(uuid)
