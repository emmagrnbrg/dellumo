from sqlalchemy.orm import Session

from backend.src.entities.UserEntity import UserEntity


class UserService:
    """
    Сервис пользователей
    """

    def __init__(self, session: Session):
        self.__session = session

    def findByEmail(self, email: str) -> UserEntity | None:
        """
        Найти пользователя по адресу электронной почты

        :param email: адрес электронной почты
        :return: данные пользователя (если найден)
        """
        return self.__session.query(UserEntity).filter(UserEntity.email == email).first()

    def save(self, user: UserEntity) -> UserEntity:
        """
        Сохранить пользователя в системе

        :param user: данные пользователя
        :return: данные сохранённого пользователя
        """
        self.__session.add(user)
        self.__session.commit()
        self.__session.refresh(user)
        return user
