from typing import Annotated

from pydantic import BaseModel, Field


class UpdatePasswordRequestModel(BaseModel):
    """
    Тело запроса на обновление пароля
    """
    password: Annotated[str, Field(min_length=8)]
