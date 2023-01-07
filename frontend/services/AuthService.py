from shared.ObserverPattern import Observer
from repositories.AuthRepository import AuthRepository


class AuthService(Observer):
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository
        self.auth_repository.register_observer(self)
        self.__user = self.auth_repository.user

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user):
        self.__user = user

    def update(self, subject):
        if isinstance(subject, AuthRepository):
            self.user = subject.user
