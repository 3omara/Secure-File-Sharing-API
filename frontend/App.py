import os
from ftplib import FTP
from ttkthemes import ThemedTk
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
        self.__file_references_repository = FileReferencesRepository(
            sio.Client(
                logger=True
            ),
            Database()
        )
        self.__file_requests_repository = FileRequestsRepository(
            sio.Client(
                logger=True
            )
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
        self.setup_window()
        self.window.mainloop()

    def setup_window(self):
        self.width = 1000
        self.height = 600
        self.window = ThemedTk(theme="arc")
        self.window.title("Vault")
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False, False)
        from views.MainView import MainView
        MainView(self.window).build(self)
