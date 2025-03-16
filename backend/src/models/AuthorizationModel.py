from pydantic import BaseModel


class TokenResponseModel(BaseModel):
    """
    Модель, содержащая токены для авторизации
    """
    refresh_token: str
    access_token: str
    expire_at: int


class RefreshTokenRequestModel(BaseModel):
    """
    Модель запроса для обновления access-токена по refresh-токену
    """
    token: str
