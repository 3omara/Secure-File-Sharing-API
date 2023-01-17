from dataclasses import replace
from ciphers.RSACipher import RSACipher
from database.Database import Database
from models.User import User
from models.FileReference import FileReference
from models.FileRequest import FileRequest, FileRequestStatus
from shared.ObserverPattern import Subject, Observer
from repositories.FileRequestsRepository import FileRequestsRepository


class FileRequestsService(Subject, Observer):
    def __init__(self,

                 file_requests_repository: FileRequestsRepository,
                 user: User,
                 database: Database,
                 rsa_cipher: RSACipher):
        super().__init__()
        self.user = user
        self.database = database
        self.rsa_cipher = rsa_cipher
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

    def request(self, file_reference: FileReference):
        self.file_requests_repository.insert(
            FileRequest(
                file_id=file_reference.id,
                file_name=file_reference.name,
                sender_id=self.user.id,
                sender_name=self.user.name,
                receiver_id=file_reference.owner_id,
                receiver_name=file_reference.owner_name,
                status=FileRequestStatus.PENDING,
                public_key=b"",
                enc_master_key=b"",
                sent_at="",
            )
        )

    def accept(self, file_request: FileRequest):
        master_key = self.database.get_master_key(file_request.file_id)
        enc_master_key = self.rsa_cipher.encrypt(
            file_request.public_key, master_key)
        self.file_requests_repository.accept(replace(file_request,
                                                     enc_master_key=enc_master_key))

    def decline(self, file_request: FileRequest):
        self.file_requests_repository.decline(file_request)

    def cancel(self, file_request: FileRequest):
        self.file_requests_repository.delete(file_request)
