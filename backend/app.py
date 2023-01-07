import ftplib
import json
from dotenv import load_dotenv
from flask import Flask, request
from flask_socketio import SocketIO
from Database import Database
from Repository import Repository
from models.File import File, Status
from models.User import User
from models.FileRequest import FileRequest
import datetime


# FTP server credentials
FTP_HOST = "127.0.0.1"
FTP_PORT = 6060
FTP_USER = "youssef"
FTP_PASS = "1234"

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

database = Database()
repository = Repository(database)


@app.route("/")
def home():
    return "Secure File Sharing"

######################### create user #########################


@app.route("/api/user", methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = data["id"]
    user_name = data["name"]
    public_key = data["public_key"]

    repository.insert_user(user_id, user_name, public_key)

    return {"id": user_id}, 201

######################### upload data #########################


@socketio.on("new_file_reference", namespace="/file_references")
def new_file_reference(data):
    data = json.loads(data)
    user_id = data["owner_id"]
    file_name = data["name"]

    current_time = str(datetime.datetime.now())

    file_id = repository.insert_file(
        user_id, file_name, current_time)
    user = repository.get_user(user_id)

    message = {"id": file_id, "name": file_name,
               "owner_id": user_id, "owner_name": user.name, "uploaded_at": current_time}
    response = {"status": True, "data": message}
    socketio.emit("new_file_reference",
                  response,
                  namespace="/file_references",
                  broadcast=True,
                  include_self=False)
    return response


######################### send request #########################


@socketio.on("new_file_request", namespace="/file_requests")
def new_file_request(data):
    sender_sid = request.sid
    data = json.loads(data)
    sender_id = data['sender_id']
    file_id = data['file_id']
    sent_at = str(datetime.datetime.now())

    repository.insert_request(
        file_id, sender_id, 0, sent_at
    )

    message = {"file_id": file_id, "file_name": data['file_name'],
               "sender_id": data['sender_id'],  "sender_name": data['sender_name'],
               "receiver_id": data['receiver_id'], "receiver_name": data['receiver_name'],
               "status": Status(0).name, "sent_at": sent_at}
    response = {"status": True, "data": message}

    receiver = User()
    receiver = repository.get_user(data['receiver_id'])
    receiver_sid = receiver[3]

    socketio.emit("new_file_request",
                  json.dumps(response),
                  namespace="/file_requests",
                  to=sender_sid)

    socketio.emit("new_file_request",
                  json.dumps(response),
                  namespace="/file_requests",
                  to=receiver_sid)

    return response

######################### accept request #########################


@socketio.on("accept_file_request", namespace="/file_requests")
def accept_file_request():
    pass

######################### decline request #########################


@socketio.on("decline_file_request", namespace="/file_requests")
def decline_file_request():
    pass

######################### delete request #########################


@socketio.on("delete_file_request", namespace="/file_requests")
def delete_file_request():
    pass

######################### Initial Connection #########################


@socketio.on("connect", namespace="/file_references")
def connect_file_references():
    session_id = request.sid
    all_files = repository.get_all_files()
    socketio.emit("init_file_references",
                  json.dumps({"status": True, "data": all_files}),
                  namespace="/file_references",
                  to=session_id)


@socketio.on("connect", namespace="/file_requests")
def connect_file_requests():
    user_id = 1
    session_id = request.sid
    user_reqs = repository.get_user_requests(user_id)
    socketio.emit("init_file_requests",
                  json.dumps({"status": True, "data": user_reqs}),
                  namespace="/file_requests",
                  to=session_id)
