from dataclasses import replace
from models.FileReference import FileAccess, FileReference
from models.FileRequest import FileRequestStatus
from shared.ObserverPattern import Subject, Observer
from repositories.FileRequestsRepository import FileRequestsRepository
from repositories.FileReferencesRepository import FileReferencesRepository


class FileReferencesService(Subject, Observer):
    USER_ID = 1

    def __init__(self,
                 file_references_repository: FileReferencesRepository,
                 file_requests_repository: FileRequestsRepository,):
        super().__init__()
        self.__file_references = []
        self.__file_id_to_user_file_request = {}
        self.file_references_repository = file_references_repository
        self.file_requests_repository = file_requests_repository
        self.file_references_repository.register_observer(self)
        self.file_requests_repository.register_observer(self)

    @property
    def file_references(self):
        return [*self.__file_references]

    def user_file_request(self, file_id):
        return self.__file_id_to_user_file_request[file_id]

    @file_references.setter
    def file_references(self, file_references):
        def map_ref(ref: FileReference) -> FileReference:
            if ref.id in self.__file_id_to_user_file_request:
                req = self.__file_id_to_user_file_request[ref.id]
                if req.status == FileRequestStatus.PENDING:
                    return replace(ref, access=FileAccess.REQUESTED)
                elif req.status == FileRequestStatus.ACCEPTED:
                    return replace(ref, access=FileAccess.PERMITTED)
                elif req.status == FileRequestStatus.DECLINED:
                    return replace(ref, access=FileAccess.DENIED)
            elif ref.owner_id == self.USER_ID:
                return replace(ref, access=FileAccess.PERMITTED)
            else:
                return replace(ref, access=FileAccess.NOT_REQUESTED)

        self.__file_references = list(map(map_ref, file_references))
        self.notify_observers()

    def update(self, subject):
        if isinstance(subject, FileReferencesRepository):
            self.file_references = subject.file_references
        elif isinstance(subject, FileRequestsRepository):
            self.__file_id_to_user_file_request = {
                request.file_id: request
                for request in subject.file_requests
                if request.sender_id == self.USER_ID
            }
            self.file_references = self.file_references
