from sqlalchemy import Column, Integer, String, Enum

from ..Database import BaseEntity
from ..enums.SettingEnum import SettingEnum


class SettingEntity(BaseEntity):
    """
    Модель данных настройки системы
    """
    __tablename__ = "settings"

    id = Column(Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    name = Column(Enum(SettingEnum), unique=True, nullable=False)
    value = Column(String, nullable=False)
    description = Column(String, nullable=False)
