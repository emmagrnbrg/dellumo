from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    """
    Исключение, выбрасываемое в случае, если с указанным адресом электронной почты пользователь не найден
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с указанным адресом электронной почты не найден"
        )
