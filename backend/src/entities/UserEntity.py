from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime

from backend.src.Database import BaseEntity
from backend.src.Utils import sha512


class UserEntity(BaseEntity):
    """
    Пользователи
    """
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True, unique=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
    createdAt = Column("created_at", DateTime, default=datetime.now())

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = sha512(password)

    def updatePwd(self, pwd: str):
        self.password = sha512(pwd)
