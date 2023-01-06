from frontend.shared.Singleton import Singleton
from Database import Database
from Models.File import File
from Models.FileRequest import FileRequest
from Models.User import User


INSERT_USER = (
    "INSERT INTO users (id, name) VALUES (%s, %s);"
)

INSERT_FILE = (
    "INSERT INTO files (user_id, name, upload_time, file_type) VALUES (%s, %s, %s, %s) RETURNING Inserted.id;"
)

INSERT_REQUEST = (
    "INSERT INTO requests (file_id, sender_id, status) VALUES (%s, %s, %s);"
)

GET_USER_BY_ID = (
    "SELECT * FROM users WHERE id = %s;"
)

GET_FILE_BY_ID = (
    "SELECT * FROM users LEFT JOIN files ON users.id = files.user_id AND files.id = %s;"
)

GET_ALL_FILES = (
    "SELECT * FROM users LEFT JOIN files ON users.id = files.user_id;"
)
    
# GET_USER_FILES = (
#   "SELECT * FROM files WHERE user_id LIKE %s;"
# )

# GET_SENT_REQUESTS = ("SELECT * FROM requests WHERE sender_id LIKE %s;")

# GET_RECEIVED_REQUESTS = ("SELECT * FROM requests WHERE receiver_id LIKE %s;")

class Repository(metaclass = Singleton):
    def __init__(self, database: Database) -> None:
        self.database = Database

    def insert_user(self, user_id: int, user_name: str):
        c = self.database.connection.cursor()
        c.execute(INSERT_USER, (user_id, user_name))
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

    def get_all_files(self) -> dict:
        c = self.database.connection.cursor()
        c.execute(GET_ALL_FILES)
        res = c.fetchall()
        self.database.connection.commit()


    