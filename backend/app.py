import ftplib
from dotenv import load_dotenv
from flask import Flask, request
from flask_socketio import SocketIO
from Database import Database
from Repository import Repository
from Models.File import File
from Models.FileRequest import FileRequest
import datetime


# FTP server credentials
FTP_HOST = "127.0.0.1"
FTP_PORT = 6060
FTP_USER = "youssef"
FTP_PASS = "1234"

app = Flask(__name__)
socketio = SocketIO(app)

database = Database()
repository = Repository(database)

@app.route("/")
def home():
    return "Secure File Sharing"

######################### create user #########################
@app.route("/api/user", methods = ['POST'])
def create_user():
    data = request.get_json()
    user_id = data["id"]
    user_name = data["name"]

    repository.insert_user(user_id, user_name)
    
    return {"id": user_id}, 201

######################### upload data #########################
@socketio.on("upload_file")
def upload_data(data):

    user_id = data["user_id"]
    file_name = data["file_name"]
    file_type = data["file_type"]

    current_time = str(datetime.datetime.now())

    file_id = repository.insert_file(user_id, file_name, current_time, file_type)
    user = repository.get_user(user_id)

    message = {"file_id": file_id,"file_name":file_name, "user_id":user_id, "user_name":user.name, "upload_time":current_time}

    if(file_type==2):
        socketio.emit("new_file", message)

    return message, 201

######################### create request #########################
def create_request():
    pass

######################### accept request #########################
def accept_request():
    pass

######################### refuse request #########################
def refuse_request():
    pass

######################### login #########################
@socketio.on("connect")
def login(user_id):
    socketio.emit("init_requests")
    socketio.emit("init_files")
    