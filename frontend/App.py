import os
from ftplib import FTP
from typing import List
import socketio as sio

from ciphers.AESCipher import AESCipher
from ciphers.DESCipher import DESCipher
from ciphers.BlowfishCipher import BlowfishCipher
from ciphers.FileCipher import FileCipher
from database.Database import Database
from repositories.FileReferencesRepository import FileReferencesRepository
from repositories.FileRequestsRepository import FileRequestsRepository
from services.FileReferencesService import FileReferencesService
from services.FileRequestsService import FileRequestsService
from services.SecureFTPService import SecureFTPService


class App:
    def __init__(self):
        self.sio_clients: List[sio.Client] = []
        self.__file_references_repository = None
        self.__file_requests_repository = None
        self.file_references_service = None
        self.file_requests_service = None
        self.ftp_service = None
        self.user_id = None

    def initialize_services(self):
        self.sio_clients.append(sio.Client(logger=True))
        self.__file_references_repository = FileReferencesRepository(
            self.sio_clients[-1],
            Database()
        )
        self.sio_clients.append(sio.Client(logger=True))
        self.__file_requests_repository = FileRequestsRepository(
            self.sio_clients[-1],
        )
        self.file_references_service = FileReferencesService(
            self.__file_references_repository,
            self.__file_requests_repository
        )
        self.file_requests_service = FileRequestsService(
            self.__file_requests_repository
        )
        self.ftp_service = SecureFTPService(
            ftp=FTP(),
            cipher=FileCipher(
                [AESCipher(), DESCipher(), BlowfishCipher()]
            ),
            master_cipher=FileCipher(
                [AESCipher()]
            ),
            file_references_repository=self.__file_references_repository
        )
        self.ftp_service.connect(
            host=os.getenv("FTP_HOST"),
            port=int(os.getenv("FTP_PORT")),
        )
        self.ftp_service.login(
            user=os.getenv("FTP_USER"),
            passwd=os.getenv("FTP_PASSWD")
        )

    def run(self):
        from views.LoginView import LoginView
        LoginView(None).build(self)

        if self.user_id is not None:
            self.initialize_services()
            from views.MainView import MainView
            MainView(None).build(self)

    def on_closing(self):
        Database().close()
        for sio_client in self.sio_clients:
            sio_client.disconnect()
