from fastapi import HTTPException, status

# тексты ошибок
_ERRORS = {
    "email": "Некорректный адрес электронной почты",
    "username": "Для имени пользователя допускается использование латиницы (A-z), цифр (0-9), "
                "символов нижнего подчеркивания (_). В качестве первого символа "
                "допускается использование <b>только</b> латиницы",
    "password": "Допускается пароль длиной <b>не менее</b> 8 символов",
    "uuid": "Запрос не найден",
    "code": "Неверный формат кода"
}


class ValidationError(HTTPException):
    """
    Исключение, выбрасываемое в случае ошибок валидации
    """
    def __init__(self, field: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=_ERRORS[field])
