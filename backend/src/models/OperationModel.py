from pydantic import BaseModel


class OperationResponseModel(BaseModel):
    """
    Тело ответа на запрос получения кода
    """
    uuid: str


class OperationVerifyRequestModel(BaseModel):
    """
    Модель запроса, содержащая одноразовый код
    """
    code: str
