import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.orm import Session

from backend.src.entities.OperationEntity import OperationEntity
from backend.src.entities.UserEntity import UserEntity
from backend.src.enums.OperationTypeEnum import OperationTypeEnum
from backend.src.enums.TemplateEnum import TemplateEnum
from backend.src.services.SettingsService import SettingsService


class EmailService:
    """
    Сервис отправки электронных писем
    """
    def __init__(self, session: Session):
        self.__settingService = SettingsService(session)

        self.__from = self.__settingService.getEmailLogin()
        self.__server = smtplib.SMTP_SSL(self.__settingService.getEmailHost(),
                                         self.__settingService.getEmailPort())
        self.__server.login(self.__from, self.__settingService.getEmailPassword())

    def sendOTPEmail(self, operation: OperationEntity) -> None:
        """
        Отправить письмо для верификации операции

        :param operation: данные операции
        """
        username = operation.user.email.split("@")[0]
        self.__send(operation.user.email,
                    EmailService.__getEmailSubjectByOperation(operation),
                    EmailService.__readEmailTemplate(TemplateEnum.OTP).format(
                        username=username,
                        code=operation.code,
                        operationType=EmailService.__getEmailOperationTypeByOperation(operation)
                    ))

    def sendPasswordChangedNotification(self, user: UserEntity) -> None:
        """
        Отправить уведомление о смене пароля пользователю

        :param user: адресат письма
        :return: пустое тело ответа в случае отсутствия ошибок
        """
        username = user.email.split("@")[0]
        self.__send(user.email,
                    "Пароль был изменён",
                    EmailService.__readEmailTemplate(TemplateEnum.PASSWORD_CHANGED).format(
                        username=username,
                        host=self.__settingService.getHost()
                    ))

    def __send(self, to: str, topic: str, body: str) -> None:
        """
        Отправка электронного письма

        :param to: адресат письма
        :param topic: тема письма
        :param body: тело письма
        """
        msg = MIMEMultipart()
        msg["From"] = self.__from
        msg["To"] = to
        msg["Subject"] = topic

        msg.attach(MIMEText(body, "html"))

        self.__server.sendmail(self.__from, to, msg.as_string())
        self.__server.close()

    @staticmethod
    def __readEmailTemplate(template: TemplateEnum) -> str:
        """
        Чтение шаблона электронного письма из репозитория

        :param template: наименование шаблона
        :return: данные шаблона
        """
        with open(str(template.value), "r", encoding="utf-8") as rf:
            return rf.read()

    @staticmethod
    def __getEmailSubjectByOperation(operation: OperationEntity) -> str:
        """
        Определить тему письма по типу операции

        :param operation: данные операции
        :return: тема письма
        """
        __SUBJECTS = {
            OperationTypeEnum.REGISTRATION: "Верификация регистрации",
            OperationTypeEnum.PASSWORD_RECOVERY: "Восстановление пароля",
            OperationTypeEnum.TWO_FACTOR: "Подтверждение входа в систему",
        }

        return __SUBJECTS[operation.type]

    @staticmethod
    def __getEmailOperationTypeByOperation(operation: OperationEntity) -> str:
        """
        Определить тип операции для вставки в письмо по операции

        :param operation: данные операции
        :return: тип операции для письма
        """
        __TYPES = {
            OperationTypeEnum.REGISTRATION: "верификации регистрации",
            OperationTypeEnum.PASSWORD_RECOVERY: "восстановления пароля",
            OperationTypeEnum.TWO_FACTOR: "подтверждения входа в систему",
        }

        return __TYPES[operation.type]


