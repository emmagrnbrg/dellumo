from enum import StrEnum


class OperationTypeEnum(StrEnum):
    """
    Типы операций, подтверждаемых одноразовым кодом
    """
    REGISTRATION = "REGISTRATION"  # регистрация
    PASSWORD_RECOVERY = "PASSWORD_RECOVERY"  # восстановление пароля
    TWO_FACTOR = "TWO_FACTOR"  # двухфакторная аутентификация
