from flask import Flask, request, session
from flask_socketio import SocketIO
from Database import Database
from Repository import Repository
from models.File import File, Status
from models.User import User
import datetime
from flask_login import login_user, LoginManager, logout_user
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = "SECRETKEY"
bcrypt = Bcrypt(app)

database = Database()
repository = Repository(database)

login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# login_manager.login_view = "login"


@login_manager.user_loader
def load_user(id):
    try:
        print("LOADING USER")
        return repository.get_user(int(id))
    except:
        print("LOADING USER EXCEPTION")
        return None

# @login_manager.request_loader
# def request_loader(request):
#     print("request: ",request)
#     user_id = request.form.get('email')
#     if user_id == None:
#         return
#     return repository.get_user(int(user_id))


@app.route("/")
def home():
    return "Secure File Sharing"

######################### create user #########################


@app.route("/login", methods=['POST'])
def login():
    session.pop('id', None)
    user_name = request.form["user_name"]
    password = request.form["password"]
    public_key = request.form["public_key"]
    print("Entered Password: ",  password)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf8')
    print("ARRIVED")
    user = repository.get_user_by_name(user_name)
    if (user != None):
        print(user.password, password)
        if bcrypt.check_password_hash(user.password, password):
            if (public_key != "None"):
                print("public key: ", public_key)
                repository.update_user_pkey(public_key, user.id)
            session['id'] = user.id
            print("user already registered: ", user)
            login_user(user)

            return {"id": user.id, "user_name": user.user_name}, 201
        else:
            return "Failed to login", 404
    else:
        print(public_key)
        user_id = repository.insert_user(
            user_name, hashed_password, public_key)
        user = repository.get_user(user_id)
        print("first time: ", user)
        session['id'] = user.id
        login_user(user)
        print(user_id)
        return {"id": user_id, "user_name": user_name}, 201


@app.route('/logout')
def logout():
    logout_user()
    session.pop('id', None)
    return 'Logged out'


@app.before_first_request
def init_app():
    print("before first request")
    logout_user()


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401

######################### upload data #########################


@socketio.on("new_file_reference", namespace="/file_references")
def new_file_reference(data):
    user_id = data["owner_id"]
    file_name = data["name"]

    current_time = str(datetime.datetime.now())

    file_id = repository.insert_file(
        user_id, file_name, current_time)
    user = repository.get_user(user_id)
    message = {"id": file_id, "name": file_name,
               "owner_id": user_id, "owner_name": user.user_name, "uploaded_at": current_time}
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
    sender_id = data['sender_id']
    file_id = data['file_id']
    sent_at = str(datetime.datetime.now())

    repository.insert_request(
        file_id, sender_id, 0, sent_at
    )
    public_key = repository.get_request(file_id, sender_id)["public_key"]

    message = {"file_id": file_id, "file_name": data['file_name'],
               "sender_id": data['sender_id'],  "sender_name": data['sender_name'],
               "receiver_id": data['receiver_id'], "receiver_name": data['receiver_name'],
               "status": Status(0).name, "sent_at": sent_at, "public_key": public_key}
    response = {"status": True, "data": message}

    receiver = repository.get_user(data['receiver_id'])
    print(receiver)
    receiver_sid = receiver.sid

    if (receiver_sid != None):
        socketio.emit("new_file_request",
                      response,
                      namespace="/file_requests",
                      to=receiver_sid)

    return response

######################### accept request #########################


@socketio.on("accept_file_request", namespace="/file_requests")
def accept_file_request(data):
    sender_id = data['sender_id']
    file_id = data['file_id']
    master_key = data['enc_master_key']

    repository.update_request(1, master_key, file_id, sender_id)
    data = {
        "file_id": file_id, "enc_master_key": master_key
    }
    response = {"status": True, "data": data}

    sender = repository.get_user(sender_id)
    sender_sid = sender.sid

    if (sender_sid != None):
        socketio.emit("accept_file_request",
                      response,
                      namespace="/file_requests",
                      to=sender_sid)
    return response


######################### decline request #########################


@socketio.on("decline_file_request", namespace="/file_requests")
def decline_file_request(data):
    sender_id = data['sender_id']
    file_id = data['file_id']

    repository.update_request(2, None, file_id, sender_id)
    data = {
        "file_id": file_id
    }
    response = {"status": True, "data": data}

    sender = repository.get_user(sender_id)
    sender_sid = sender.sid

    if (sender_sid != None):
        socketio.emit("decline_file_request",
                      response,
                      namespace="/file_requests",
                      to=sender_sid)
    return response

######################### delete request #########################


@socketio.on("delete_file_request", namespace="/file_requests")
def delete_file_request(data):
    sender_id = data['sender_id']
    file_id = data['file_id']
    receiver_id = data['receiver_id']

    repository.delete_request(file_id, sender_id)
    data = {
        "file_id": file_id
    }
    response = {
        "status": True, "data": data
    }

    receiver = repository.get_user(receiver_id)
    receiver_sid = receiver.sid

    if (receiver_sid != None):
        socketio.emit("delete_file_request",
                      response,
                      namespace="/file_requests",
                      to=receiver_sid)
    return response


######################### Initial Connection #########################


@socketio.on("connect", namespace="/file_references")
def connect_file_references():
    session_id = request.sid
    all_files = repository.get_all_files()
    socketio.emit("init_file_references",
                  {"status": True, "data": all_files},
                  namespace="/file_references",
                  to=session_id)


@socketio.on("connect", namespace="/file_requests")
def connect_file_requests(auth):
    print(auth)
    user_id = auth["user_id"]
    print("requests - user id:  ", user_id)
    session_id = request.sid
    repository.update_user_sid(session_id, user_id)
    user_reqs = repository.get_user_requests(user_id)
    socketio.emit("init_file_requests",
                  {"status": True, "data": user_reqs},
                  namespace="/file_requests",
                  to=session_id)
