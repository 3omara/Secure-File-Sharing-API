from typing import List
import socketio as sio
from shared.ObserverPattern import Subject
from models.FileReference import FileReference


class FileReferencesRepository(Subject):
    def __init__(self, client: sio.Client):
        super().__init__()
        self.client = client
        self.__file_references = [
            FileReference(
                id=1,
                name="file1.txt",
                owner_id=1,
                owner_name="user1",
                master_key=None,
                uploaded_at="2020-01-01 00:00:00"
            ),
        ]

    @property
    def file_references(self):
        return [*self.__file_references]

    @file_references.setter
    def file_references(self, file_references: List[FileReference]):
        self.__file_references = file_references
        self.notify_observers()

    def insert(self, file: FileReference):
        def on_uploaded(response):
            self.file_references = [*self.__file_references,
                                    FileReference.from_json(response["data"])]

        self.client.emit("upload_file",
                         file.to_json(),
                         callback=on_uploaded)
