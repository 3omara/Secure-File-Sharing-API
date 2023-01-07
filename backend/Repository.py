from shared.Singleton import Singleton
from Database import Database
from models.File import File
from models.FileRequest import FileRequest
from models.User import User
import json


INSERT_USER = (
    "INSERT INTO users (user_id, user_name, public_key) VALUES (%s, %s, %s);"
)

INSERT_FILE = (
    "INSERT INTO files (user_id, file_name, upload_time) VALUES (%s, %s, %s) RETURNING Inserted.id;"
)

INSERT_REQUEST = (
    "INSERT INTO requests (file_id, sender_id, status) VALUES (%s, %s, %s);"
)

GET_USER_BY_ID = (
    "SELECT * FROM users WHERE user_id = %s;"
)

GET_FILE_BY_ID = (
    "SELECT * FROM users LEFT JOIN files ON users.user_id = files.user_id WHERE users.user_id = files.user_id AND files.file_id = %s;"
)

GET_ALL_FILES = (
    "SELECT * FROM files;"
)

GET_USER_REQUESTS = (
    "SELECT * FROM files LEFT JOIN requests ON files.file_id = requests.file_id WHERE files.file_id = requests.file_id AND (requests.sender_id = %s OR files.user_id = %s) ;"
)

class Repository(metaclass = Singleton):

    def __init__(self, database: Database) -> None:
        self.database = Database

    def insert_user(self, user_id: int, user_name: str, public_key:bytes):
        c = self.database.connection.cursor()
        c.execute(INSERT_USER, (user_id, user_name, public_key))
        self.database.connection.commit()

    def insert_file(self, user_id: int, file_name:str, upload_time:str, file_type:int) -> int:
        c = self.database.connection.cursor()
        c.execute(INSERT_FILE, (user_id, file_name, upload_time, file_type))
        file_id = c.fetchone()
        self.database.connection.commit()
        return file_id

    def insert_request(self, file_id, sender_id, status):
        c = self.database.connection.cursor()
        c.execute(INSERT_REQUEST, (file_id, sender_id, status))
        self.database.connection.commit()

    def get_file_with_user(self, file_id):
        c = self.database.connection.cursor()
        c.execute(GET_FILE_BY_ID, (file_id,))
        res = c.fetchone()
        self.database.connection.commit()
        return res

    def get_user(self, user_id) -> User:
        c = self.database.connection.cursor()
        c.execute(GET_USER_BY_ID, (user_id,))
        res = c.fetchone()
        self.database.connection.commit()
        return User(res[0], res[1])

    def get_all_files(self):
        c = self.database.connection.cursor()
        c.execute(GET_ALL_FILES)
        res = c.fetchall()
        self.database.connection.commit()
        keys = ("file_id", "user_id", "file_name", "upload_time")
        allFiles = []
        for r in res:
            r = {keys[i] : r[i] for i, _ in enumerate(r)}
            allFiles.append(r)
        return json.dumps(allFiles)


    def get_user_requests(self, user_id: int):
        c = self.database.connection.cursor()
        c.execute(GET_USER_REQUESTS, (user_id,user_id))
        res = c.fetchall()
        self.database.connection.commit()
        keys = ("file_id", "sender_id", "status", "enc_master_key")
        allRequests = []
        for r in res:
            r = {keys[i] : r[i] for i, _ in enumerate(r)}
            allRequests.append(r)
        return json.dumps(allRequests)



    