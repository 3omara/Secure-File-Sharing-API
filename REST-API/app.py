import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from Crypto.PublicKey import RSA
from flask_restful import Api, Resource


# Each user has both a public and a private key for RSA encryption purposes.
CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (id SPECIAL PRIMARY KEY, public_key INTEGER, private_key INTEGER);"
)

# This table holds two types of files: 
# - Bundle files containing both the encrypted data and associated keys. 
# - Files holding encrypted master keys. 
CREATE_FILES_TABLE = (
    "CREATE TABLE IF NOT EXISTS files (id SPECIAL PRIMARY KEY, user_id TEXT, file_path TEXT, FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);"
)

CREATE_REQUESTS_TABLE = """ CREATE TABLE IF NOT EXISTS requests (file_id INTEGER, sender_id TEXT, receiver_id TEXT, 
                            FOREIGN KEY(sender_id) REFERENCES users(id),
                            FOREIGN KEY(receiver_id) REFERENCES users(id)),
                            FOREIGN KEY(file_id) REFERENCES files(id)); """

INSERT_USER = (
    "INSERT INTO users (id, public_key, private_key) VALUES (%s, %s, %s);"
)

INSERT_FILE = (
    "INSERT INTO files (user_id, file_path) VALUES (%s, %s);"
)

INSERT_REQUEST = (
    "INSERT INTO requests (file_id, sender_id, reciever_id) VALUES (%s, %s, %s);"
)

GET_USER_BY_ID = (
    "SELECT * FROM users WHERE id LIKE (user_id) VALUES (%s);"
)

GET_FILE_BY_ID = {
    "SELECT * FROM files WHERE id = (file_id) VALUES (%s);"
}

GET_USER_FILES = {
    "SELECT * FROM files WHERE user_id LIKE (user_id) VALUES (%s);"
}

GET_SENT_REQUESTS = {
    "SELECT * FROM requests WHERE sender_id LIKE (user_id) VALUES (%s);"
}

GET_RECEIVED_REQUESTS = {
    "SELECT * FROM requests WHERE receiver_id LIKE (user_id) VALUES (%s);"
}

load_dotenv()

app = Flask(__name__)
# api = Api(app)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.post("/api/user")

def create_user():
    data = request.get_json()
    id = data["id"]
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USER, (id, public_key, private_key))
            

# if __name__ == "__main__":
#     app.run(debug=True)
