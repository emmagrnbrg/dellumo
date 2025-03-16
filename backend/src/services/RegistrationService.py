from sqlalchemy.orm import Session

from backend.src.entities.OperationEntity import OperationEntity
from backend.src.entities.UserEntity import UserEntity
from backend.src.enums.OperationTypeEnum import OperationTypeEnum
from backend.src.errors.RegistrationError import UserExists
from backend.src.models.RegistrationModel import RegistrationRequestModel
from backend.src.services.EmailService import EmailService
from backend.src.services.OperationService import OperationService
from backend.src.services.UserService import UserService


class RegistrationService:
    """
    Сервис регистрации пользователей
    """

    def __init__(self, session: Session):
        self.__session = session
        self.__userService = UserService(session)
        self.__operationService = OperationService(session)
        self.__emailService = EmailService(session)

    def start(self, request: RegistrationRequestModel) -> str:
        """
        Создание заявки на регистрацию пользователя

        :param request: тело запроса
        :return: uuid заявки
        """
        user = self.__userService.findByEmail(request.email)
        if not user:
            user = UserEntity(request.email, request.password)
        else:
            if user.verified:
                raise UserExists
            user.updatePwd(request.password)
        user = self.__userService.save(user)

        operation = self.__operationService.findByUserAndType(user, OperationTypeEnum.REGISTRATION)
        if not operation:
            operation = OperationEntity(user, OperationTypeEnum.REGISTRATION)
        else:
            operation = self.__operationService.reset(operation)

        return self.__operationService.save(operation)

    def verify(self, operationUuid: str, code: str) -> None:
        """
        Верификация одноразового кода для подтверждения регистрации

        :param operationUuid: uuid операции
        :param code: одноразовый код
        """
        operation = self.__operationService.verify(operationUuid, code)
        operation.user.verified = True
        self.__session.add(operation.user)
        self.__session.delete(operation)
        self.__session.commit()
