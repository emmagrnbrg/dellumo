from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from ..models.OperationModel import OperationVerifyRequestModel


class PasswordRecoveryRequestModel(BaseModel):
    """
    Тело запроса на восстановление пароля
    """
    email: EmailStr


class ResetPasswordRequestModel(BaseModel):
    operation: OperationVerifyRequestModel
    password: Annotated[str, Field(min_length=8)]
