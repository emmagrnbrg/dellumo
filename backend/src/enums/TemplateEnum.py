import pathlib
from enum import StrEnum

_BASE_TEMPLATE_PATH = f"{str(pathlib.Path(__file__).parents[1])}\\static\\email-templates\\"


class TemplateEnum(StrEnum):
    """
    Список шаблонов электронных писем
    """
    OTP = _BASE_TEMPLATE_PATH + "OTP.html"
    PASSWORD_CHANGED = _BASE_TEMPLATE_PATH + "PasswordChanged.html"
