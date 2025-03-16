from datetime import datetime, timedelta
from random import choice
from hashlib import sha512 as _sha512

from backend.src.Constants import DIGITS, EXPIRATION_MINUTES


def sha512(text: str) -> str:
    """
    Open text -> hash sha512

    :param text: open text
    :return: hash
    """
    return _sha512(text.encode()).hexdigest()


def generateCode(length: int = 6) -> str:
    """
    Генерация случайного одноразового кода

    :param length: длина генерируемого кода
    :return: сгенерированный код
    """
    return "".join([choice(DIGITS) for _ in range(length)])


def getExpirationTime(minutes: int = EXPIRATION_MINUTES) -> datetime:
    """
    Рассчитать время окончания жизни операции

    :param minutes: время в минутах, в течение которого действителен запрос
    :return: время окончания жизни операции
    """
    return datetime.now() + timedelta(minutes=minutes)
