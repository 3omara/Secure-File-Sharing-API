import sqlite3
from shared.Singleton import Singleton
from models.FileReference import FileReference


class Database(metaclass=Singleton):
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.connection.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {FileReference.TABLE_NAME} (
                id              INT PRIMARY KEY     NOT NULL,
                name            TEXT                NOT NULL,
                owner_id        INT                 NOT NULL,
                owner_name      TEXT                NOT NULL,
                master_key      BLOB                NOT NULL,
                uploaded_at     TEXT                NOT NULL
            );
            ''')
