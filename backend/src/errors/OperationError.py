from fastapi import HTTPException, status

from backend.src.Constants import CODE_LIFE_TIME


class OperationNotFound(HTTPException):
    """
    Исключение, выбрасываемое в случае, если операция не найдена или истекла
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Операция не найдена или истекла"
        )


class TooManyAttempts(HTTPException):
    """
    Исключение, выбрасываемое в случае, если количество попыток ввода кода превышено
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Количество попыток ввода кода превышено. "
                   "Инициируйте операцию заново или сгенерируйте новый код"
        )


class IncorrectOTP(HTTPException):
    """
    Исключение, выбрасываемое в случае, если одноразовый пароль введён неверно
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный код"
        )


class OTPTimeout(HTTPException):
    """
    Исключение, выбрасываемое в случае, если запрос на повторную отправку кода отправлен до истечения таймера
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Для данного адреса электронной почты в течение последних {} минут "
                   "уже была запрошена процедура отправки кода. Попробуйте позднее".format(CODE_LIFE_TIME)
        )
