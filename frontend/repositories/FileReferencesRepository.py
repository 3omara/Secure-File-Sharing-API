import socketio as sio
from database.Database import Database
from shared.Singleton import Singleton
from models.FileReference import FileReference


class FileReferencesRepository(metaclass=Singleton):
    def __init__(self, database: Database, sio_client: sio.Client):
        self.database = database
        self.sio_client = sio_client

    def insert(self, file: FileReference):
        def on_uploaded(response):
            file = FileReference.from_json(response)
            c = self.database.connection.cursor()
            c.execute(
                f"INSERT INTO {FileReference.TABLE_NAME} (id, name, owner_id, owner_name, master_key, uploaded_at) VALUES (?, ?, ?, ?, ?, ?)",
                (file.id, file.name, file.owner_id,
                 file.owner_name, file.master_key, file.uploaded_at)
            )
            self.database.connection.commit()

        self.sio_client.emit("upload_file",
                             file.to_json(),
                             callback=on_uploaded)

    def get(self, id: int) -> FileReference:
        c = self.database.connection.cursor()
        c.execute(
            f"SELECT * FROM {FileReference.TABLE_NAME} WHERE id = ?", (id,))
        row = c.fetchone()
        return FileReference(row[0], row[1], row[2], row[3], row[4], row[5])
