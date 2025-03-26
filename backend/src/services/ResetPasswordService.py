from sqlalchemy.orm import Session

from ..entities.OperationEntity import OperationEntity
from ..enums.OperationTypeEnum import OperationTypeEnum
from ..errors.ResetPasswordError import UserNotFound
from ..services.EmailService import EmailService
from ..services.OperationService import OperationService
from ..services.UserService import UserService


class ResetPasswordService:
    def __init__(self, session: Session):
        self.__session = session
        self.__operationService = OperationService(session)
        self.__userService = UserService(session)
        self.__emailService = EmailService(session)

    def start(self, email: str) -> str:
        """
        Создание заявки на восстановление пароля пользователя

        :param email: адрес электронной почты пользователя
        :return: uuid созданной заявки
        """
        user = self.__userService.findByEmail(email)
        if not user or not user.verified:
            raise UserNotFound

        operation = self.__operationService.findByUserAndType(user, OperationTypeEnum.PASSWORD_RECOVERY)
        if not operation:
            operation = OperationEntity(user, OperationTypeEnum.PASSWORD_RECOVERY)
        else:
            operation = self.__operationService.reset(operation)

        return self.__operationService.save(operation)

    def verify(self, uuid: str, code: str, password: str):
        """
        Верификация одноразового кода

        :param uuid: uuid операции
        :param code: одноразовый код
        :param password: пароль пользователя
        """
        operation = self.__operationService.verify(uuid, code)
        operation.user.updatePwd(password)
        self.__session.add(operation.user)
        self.__emailService.sendPasswordChangedNotification(operation.user)
        self.__session.delete(operation)
        self.__session.commit()
