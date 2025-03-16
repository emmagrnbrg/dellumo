from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from backend.src.Constants import CODE_LIFE_TIME, MAX_ATTEMPTS_COUNT
from backend.src.Utils import generateCode
from backend.src.entities.OperationEntity import OperationEntity
from backend.src.entities.UserEntity import UserEntity
from backend.src.enums.OperationTypeEnum import OperationTypeEnum
from backend.src.errors.OperationError import OperationNotFound, TooManyAttempts, IncorrectOTP, OTPTimeout
from backend.src.services.EmailService import EmailService


class OperationService:
    """
    Сервис одноразовых кодов
    """
    def __init__(self, session: Session):
        self.__session = session
        self.__emailService = EmailService(session)

    def findByUserAndType(self, user: UserEntity, operationType: OperationTypeEnum) -> OperationEntity | None:
        """
        Найти операцию по пользователю и типу

        :param user: данные пользователя
        :param operationType: тип операции
        :return: данные операции
        """
        return self.__session.query(OperationEntity).filter(
            and_(
                OperationEntity.user == user,
                OperationEntity.type == operationType
            )
        ).first()

    def save(self, operation: OperationEntity) -> str:
        """
        Создание операции на верификацию процесса одноразовым кодом

        :param operation: данные операции
        :return: uuid операции
        """
        self.__session.add(operation)
        self.__session.commit()
        self.__session.refresh(operation)
        self.__emailService.sendOTPEmail(operation)
        return operation.id

    def verify(self, uuid: str, code: str) -> OperationEntity:
        """
        Верификация операции по одноразовому коду

        :param uuid: uuid операции
        :param code: одноразовый код
        :return: данные операции в случае успешной верификации
        """
        operation = self.__findById(uuid)
        now = datetime.now()

        if not operation:
            raise OperationNotFound

        if operation.expireAt <= now:
            self.__session.delete(operation)
            raise OperationNotFound

        if operation.attemptsCount >= MAX_ATTEMPTS_COUNT:
            raise TooManyAttempts

        if code != operation.code:
            operation.attemptsCount += 1
            self.__session.add(operation)
            self.__session.commit()
            self.__session.refresh(operation)
            raise IncorrectOTP

        return operation

    def resent(self, uuid: str) -> None:
        """
        Отправить одноразовый код заново

        :param uuid: uuid операции
        """
        operation = self.__findById(uuid)
        now = datetime.now()

        if not operation:
            raise OperationNotFound

        if operation.expireAt <= now:
            self.__session.delete(operation)
            raise OperationNotFound

        if operation.resentAt + timedelta(minutes=CODE_LIFE_TIME) > now:
            raise OTPTimeout

        operation.code = generateCode()
        operation.resentAt = now
        operation.attemptsCount = 0
        self.__session.add(operation)
        self.__session.commit()
        self.__session.refresh(operation)
        self.__emailService.sendOTPEmail(operation)

    @staticmethod
    def reset(operation: OperationEntity) -> OperationEntity:
        """
        Сбросить (обновить) операцию

        :param operation: данные операции
        :return: uuid операции
        """
        now = datetime.now()
        if operation.resentAt + timedelta(minutes=CODE_LIFE_TIME) > now:
            raise OTPTimeout

        operation.reset()
        return operation

    def __findById(self, uuid: str) -> OperationEntity | None:
        """
        Найти операцию по uuid

        :param uuid: uuid операции
        :return: данные операции (если найдена)
        """
        return self.__session.query(OperationEntity).filter(OperationEntity.id == uuid).first()
