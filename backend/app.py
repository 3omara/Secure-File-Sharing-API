import os
import psycopg2
import ftplib
from dotenv import load_dotenv
from flask import Flask, request
import requests
# from flask_restful import Api, Resource


# Each user has both a public and a private key for RSA encryption purposes.
CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (id VARCHAR(255), PRIMARY KEY (id));"
)

# This table holds two types of files: 
# - Bundle files containing both the encrypted data and associated keys. 
# - Files holding encrypted master keys. 
CREATE_FILES_TABLE = (
    "CREATE TABLE IF NOT EXISTS files (id SERIAL, user_id VARCHAR(255), name VARCHAR(255), PRIMARY KEY (id), FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);"
)

CREATE_REQUESTS_TABLE = """ CREATE TABLE IF NOT EXISTS requests (file_id INT, sender_id VARCHAR(255), receiver_id VARCHAR(255), 
                            FOREIGN KEY(sender_id) REFERENCES users(id),
                            FOREIGN KEY(receiver_id) REFERENCES users(id)),
                            FOREIGN KEY(file_id) REFERENCES files(id)); """

INSERT_USER = (
    "INSERT INTO users (id) VALUES (%s);"
)

INSERT_FILE = (
    "INSERT INTO files (user_id, name) VALUES (%s, %s);"
)

INSERT_REQUEST = (
    "INSERT INTO requests (file_id, sender_id, reciever_id) VALUES (%s, %s, %s);"
)

# GET_USER_BY_ID = (
#     "SELECT * FROM users WHERE id LIKE %s;"
# )

GET_FILE_BY_ID = (
    "SELECT * FROM files WHERE id = %s;"
)
    
# GET_USER_FILES = (
#   "SELECT * FROM files WHERE user_id LIKE %s;"
# )

# GET_SENT_REQUESTS = ("SELECT * FROM requests WHERE sender_id LIKE %s;")

# GET_RECEIVED_REQUESTS = ("SELECT * FROM requests WHERE receiver_id LIKE %s;")

load_dotenv()

# FTP server credentials
FTP_HOST = "127.0.0.1"
FTP_PORT = 6060
FTP_USER = "youssef"
FTP_PASS = "1234"

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

@app.route("/")
def home():
    return "Secure File Sharing"

######################### create user #########################
@app.route("/api/user", methods = ['POST'])
def create_user():
    data = request.get_json()
    user_id = data["id"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(INSERT_USER, (user_id,))
    
    return {"id": user_id}, 201

######################### upload data #########################
@app.route("/api/upload", methods = ['POST'])
def upload_data():
    data = request.get_json()
    user_id = data["user_id"]
    file_name = data["file_name"]

    # connect to the FTP server
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST,FTP_PORT)
    ftp.login(FTP_USER,FTP_PASS)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_FILES_TABLE)
            cursor.execute(INSERT_FILE, (user_id, file_name))

    # force UTF-8 encoding
    ftp.mkd(user_id)
    ftp.encoding = "utf-8"
    file_path = user_id + "/" + file_name
    with open(file_name, "rb") as file:
    # use FTP's STOR command to upload the file
        ftp.storbinary(f"STOR {file_path}", file)
        ftp.quit()
    
    return {"file_name": file_name, "file_path": file_path}, 201

######################### download data #########################
@app.route("/api/download", methods = ['GET'])
def download_data():
    args = request.args
    file_id = int(args.to_dict().get("file_id"))

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_FILE_BY_ID, (file_id,))
            result = cursor.fetchone()
            user_id = result[1]
            file_name = result[2]

    file_path = user_id + "/" + file_name
    
    # connect to the FTP server
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST,FTP_PORT)
    ftp.login(FTP_USER,FTP_PASS)

    # force UTF-8 encoding
    ftp.encoding = "utf-8"

    with open(file_name, "wb") as file:
    # use FTP's RETR command to download the file
        ftp.retrbinary(f"RETR {file_path}", file.write)
        ftp.quit()

    return {"message": f"File {file_name} downloaded."}, 201

# def create_request():
#     pass

# def encrypt_masterKey():
#     pass

# def decrypt_masterKey():
#     pass

# def encrypt_data():
#     pass

# def decrypt_data():
#     pass