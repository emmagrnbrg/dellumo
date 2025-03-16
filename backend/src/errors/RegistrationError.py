from fastapi import HTTPException, status


class UserExists(HTTPException):
    """
    Исключение, выбрасываемое в случае, если с указанным адресом электронной почты пользователь уже существует
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с указанным адресом электронной почты уже существует"
        )
