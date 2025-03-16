from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from backend.src.Database import BaseEntity
from backend.src.Utils import generateCode, getExpirationTime
from backend.src.entities.UserEntity import UserEntity
from backend.src.enums.OperationTypeEnum import OperationTypeEnum


class OperationEntity(BaseEntity):
    """
    Одноразовые коды
    """
    __tablename__ = "operations"

    id = Column(String, nullable=False, primary_key=True, unique=True, default=str(uuid4()))
    userId = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(OperationTypeEnum), nullable=False)
    code = Column(String, nullable=False, default=generateCode())
    expireAt = Column("expire_at", DateTime,  nullable=False, default=getExpirationTime())
    resentAt = Column("resent_at", DateTime, nullable=False, default=datetime.now())
    attemptsCount = Column("attempts_count", Integer, nullable=False, default=0)

    user = relationship("UserEntity", backref="operations")

    def __init__(self, user: UserEntity, operationType: OperationTypeEnum):
        self.user = user
        self.userId = user.id
        self.type = operationType

    def reset(self):
        self.code = generateCode()
        self.expireAt = getExpirationTime()
        self.resentAt = datetime.now()
        self.attemptsCount = 0
