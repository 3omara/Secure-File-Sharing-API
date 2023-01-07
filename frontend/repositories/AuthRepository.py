from shared.Subject import Subject
from models.User import User


class AuthRepository(Subject):
    def __init__(self):
        self.__user = None

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user: User):
        self.__user = user
        self.notify_observers()
