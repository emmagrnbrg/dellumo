from datetime import datetime, timedelta

from jose import jwt
from sqlalchemy.orm import Session

from ..Constants import REFRESH_TOKEN_LIFETIME, ACCESS_TOKEN_LIFETIME
from ..Utils import sha512
from ..entities.UserEntity import UserEntity
from ..errors.AuthorizationError import InvalidCredential, SessionExpired
from ..models.AuthorizationModel import TokenResponseModel
from ..services.SettingsService import SettingsService
from ..services.UserService import UserService


class AuthorizationService:
    """
    Сервис авторизации пользователей
    """

    def __init__(self, session: Session):
        self.__session = session
        self.__settingService = SettingsService(session)
        self.__userService = UserService(session)

    def login(self, email: str, password: str) -> TokenResponseModel:
        """
        Авторизация пользователя

        :param email: адрес электронной почты
        :param password: пароль
        :return: токены доступа
        """
        user = self.__userService.findByEmail(email)
        if not user or sha512(password) != user.password:
            raise InvalidCredential
        return TokenResponseModel(refresh_token=self.__generateToken(user.id, REFRESH_TOKEN_LIFETIME),
                                  access_token=self.__generateToken(user.id, ACCESS_TOKEN_LIFETIME),
                                  expire_at=(datetime.now() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)).timestamp())

    def getCurrentUser(self, token: str) -> UserEntity:
        """
        Получить данные текущего авторизованного пользователя

        :param token: токен пользователя
        :return: текущий пользователь
        """
        return self.__decodeUser(token)

    def refreshToken(self, refreshToken: str) -> TokenResponseModel:
        """
        Обновить refresh-токен

        :param refreshToken: текущий refresh-токен
        :return: обновлённые токены
        """
        user = self.__decodeUser(refreshToken)
        return TokenResponseModel(refresh_token=self.__generateToken(user.id, REFRESH_TOKEN_LIFETIME),
                                  access_token=self.__generateToken(user.id, ACCESS_TOKEN_LIFETIME),
                                  expire_at=(datetime.now() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)).timestamp())

    def __decodeUser(self, token: str) -> UserEntity | None:
        """
        Получение данных пользователя по токену

        :param token: токен
        :return: данные пользователя, если токен валидный
        """
        try:
            userData = jwt.decode(token,
                                  self.__settingService.getAccessTokenSecretKey(),
                                  algorithms=[self.__settingService.getAccessTokenAlgorithm()])
        except Exception:
            raise InvalidCredential

        userId, expireTime = userData.get("userId"), userData.get("expireTime")
        if not userId or not expireTime:
            raise InvalidCredential

        user: UserEntity | None = self.__userService.findById(userId)
        if not user:
            raise InvalidCredential

        if datetime.fromtimestamp(expireTime) <= datetime.now():
            raise SessionExpired

        return user

    def __generateToken(self, userId: int, expireIn: int) -> str:
        """
        Генерация токена

        :param userId: идентификатор пользователя
        :param expireIn: время жизни (в минутах)
        :return: сгенерированный токен
        """
        toEncode = {
            "userId": userId,
            "expireTime": round((datetime.now() + timedelta(minutes=expireIn)).timestamp(), 3)
        }
        return jwt.encode(toEncode,
                          self.__settingService.getAccessTokenSecretKey(),
                          algorithm=self.__settingService.getAccessTokenAlgorithm())
