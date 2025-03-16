from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class RegistrationRequestModel(BaseModel):
    """
    Тело запроса на создание запроса на регистрацию
    """
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]
