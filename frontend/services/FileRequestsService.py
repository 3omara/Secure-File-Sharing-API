from shared.ObserverPattern import Subject, Observer
from repositories.FileRequestsRepository import FileRequestsRepository


class FileRequestsService(Subject, Observer):
    def __init__(self, file_requests_repository: FileRequestsRepository):
        super().__init__()
        self.file_requests_repository = file_requests_repository
        self.file_requests_repository.register_observer(self)
        self.__file_requests = self.file_requests_repository.file_requests

    @property
    def file_requests(self):
        return [*self.__file_requests]

    @file_requests.setter
    def file_requests(self, file_requests):
        self.__file_requests = file_requests
        self.notify_observers()

    def update(self, subject):
        if isinstance(subject, FileRequestsRepository):
            self.file_requests = subject.file_requests

    def accept(self, file_request):
        self.file_requests_repository.accept(file_request)

    def decline(self, file_request):
        self.file_requests_repository.decline(file_request)

    def cancel(self, file_request):
        self.file_requests_repository.delete(file_request)
