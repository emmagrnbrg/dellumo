from fastapi import HTTPException, status


class InvalidCredential(HTTPException):
    """
    Исключение, выбрасываемое в случае, если пользователь ввёл неверные данные авторизации
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный адрес электронной почты или пароль"
        )


class SessionExpired(HTTPException):
    """
    Исключение, выбрасываемое в случае, если сессия пользователя истекла
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Сессия истекла. Пожалуйста, авторизуйтесь заново"
        )
