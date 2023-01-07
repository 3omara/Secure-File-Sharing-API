import os
import psycopg2
from shared.Singleton import Singleton
from dotenv import load_dotenv

# Each user has both a public and a private key for RSA encryption purposes.
CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (user_id INT, user_name VARCHAR(255), public_key BYTEA, PRIMARY KEY (user_id));"
)

# This table holds two types of files:
# - Bundle files containing both the encrypted data and associated keys.
# - Files holding encrypted master keys.
# file_type values: 0 -> public key, 1 -> master key, 2 -> regular file
CREATE_FILES_TABLE = (
    "CREATE TABLE IF NOT EXISTS files (file_id SERIAL, user_id INT, file_name VARCHAR(255), upload_time VARCHAR(255), PRIMARY KEY (file_id), FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE);"
)

CREATE_REQUESTS_TABLE = """ CREATE TABLE IF NOT EXISTS requests (file_id INT, sender_id INT, status INT, enc_master_key BYTEA, 
                            FOREIGN KEY(sender_id) REFERENCES users(user_id),
                            FOREIGN KEY(file_id) REFERENCES files(file_id)); """


class Database(metaclass=Singleton):

    def __init__(self) -> None:
        load_dotenv()
        self.url = os.getenv("DATABASE_URL")
        self.connection = psycopg2.connect(self.url)
        c = self.connection.cursor()
        c.execute(CREATE_USERS_TABLE)
        c.execute(CREATE_FILES_TABLE)
        c.execute(CREATE_REQUESTS_TABLE)
        self.connection.commit()
