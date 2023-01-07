from shared.ObserverPattern import Subject, Observer
from repositories.FileReferencesRepository import FileReferencesRepository


class FileReferencesService(Subject, Observer):
    def __init__(self, file_references_repository: FileReferencesRepository):
        super().__init__()
        self.file_references_repository = file_references_repository
        self.file_references_repository.register_observer(self)
        self.__file_references = self.file_references_repository.file_references

    @property
    def file_references(self):
        return [*self.__file_references]

    @file_references.setter
    def file_references(self, file_references):
        self.__file_references = file_references
        self.notify_observers()

    def update(self, subject):
        if isinstance(subject, FileReferencesRepository):
            self.file_references = subject.file_references
