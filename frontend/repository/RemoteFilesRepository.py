from database.Database import Database
from shared.Singleton import Singleton
from models.FileReference import FileReference


class RemoteFilesRepository(metaclass=Singleton):
    def __init__(self, database: Database):
        self.database = database

    def insert(self, file: FileReference):
        c = self.database.connection.cursor()
        c.execute(
            f"INSERT INTO {FileReference.TABLE_NAME} (id, name, owner_id, owner_name, master_key, uploaded_at) VALUES (?, ?, ?, ?, ?, ?)",
            (file.id, file.name, file.owner_id,
             file.owner_name, file.master_key, file.uploaded_at)
        )
        self.database.connection.commit()

    def get(self, id: int) -> FileReference:
        c = self.database.connection.cursor()
        c.execute(
            f"SELECT * FROM {FileReference.TABLE_NAME} WHERE id = ?", (id,))
        row = c.fetchone()
        return FileReference(row[0], row[1], row[2], row[3], row[4], row[5])
