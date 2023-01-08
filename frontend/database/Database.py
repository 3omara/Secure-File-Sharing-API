import sqlite3
from shared.Singleton import Singleton
from models.FileReference import FileReference


MASTER_KEY_TABLE_NAME = "master_keys"


class Database(metaclass=Singleton):
    def __init__(self):
        self.connection = sqlite3.connect(
            "database.db", check_same_thread=False)
        self.connection.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {MASTER_KEY_TABLE_NAME} (
                id              INT PRIMARY KEY     AUTOINCREMENT,
                file_id         INT                 NOT NULL,
                master_key      BLOB                NOT NULL
            );
            ''')

    def insert_master_key(self, file_id: int, master_key: bytes):
        self.connection.execute(
            f'''
            INSERT INTO {MASTER_KEY_TABLE_NAME} (file_id, master_key)
            VALUES (?, ?);
            ''',
            (file_id, master_key)
        )
        self.connection.commit()

    def get_master_key(self, file_id: int) -> bytes or None:
        cursor = self.connection.execute(
            f'''
            SELECT master_key FROM {MASTER_KEY_TABLE_NAME}
            WHERE file_id = ?;
            ''',
            (file_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return row
