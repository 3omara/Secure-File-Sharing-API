from ftplib import FTP
from typing import List
from ciphers.FileCipher import FileCipher
from ciphers.RSACipher import RSACipher
from models.User import User
from models.FileReference import FileReference
from models.FileRequest import FileRequest, FileRequestStatus
from repositories.FileReferencesRepository import FileReferencesRepository
from repositories.FileRequestsRepository import FileRequestsRepository
from shared import PathUtil


class SecureFTPService:
    def __init__(self,
                 ftp: FTP,
                 cipher: FileCipher,
                 master_cipher: FileCipher,
                 master_key_cipher: RSACipher,
                 file_references_repository: FileReferencesRepository,
                 file_requests_repository: FileRequestsRepository,
                 user: User
                 ):
        self.ftp = ftp
        self.ftp.encoding = "utf-8"
        self.cipher = cipher
        self.master_cipher = master_cipher
        self.master_key_cipher = master_key_cipher
        self.file_references_repository = file_references_repository
        self.file_requests_repository = file_requests_repository
        self.user = user
        PathUtil.setup_secure_ftp_cache()

    def connect(self, host, port=0, timeout=-999):
        return self.ftp.connect(host, port, timeout)

    def login(self, user='', passwd='', acct=''):
        return self.ftp.login(user, passwd, acct)

    def upload(self, filepath: str):
        # Encrypt file
        filename = PathUtil.get_name(filepath)
        encrypted_filepath = PathUtil.encrypted_filepath(filename)
        keys = self.cipher.generate_keys()
        with open(filepath, 'rb') as file:
            with open(encrypted_filepath, 'wb') as encrypted_file:
                self.cipher.encrypt(
                    file.read, encrypted_file.write, keys)

        # Encrypt keys
        keys_filepath = PathUtil.keys_filepath(filename)
        encrypted_keys_filepath = PathUtil.encrypted_filepath(keys_filepath)
        master_keys = self.master_cipher.generate_keys()
        with open(keys_filepath, 'wb') as keys_file:
            keys_file.writelines(keys)
        with open(keys_filepath, 'rb') as keys_file:
            with open(encrypted_keys_filepath, 'wb') as encrypted_keys_file:
                self.master_cipher.encrypt(
                    keys_file.read, encrypted_keys_file.write, master_keys)

        # Upload file, and keys
        keys_filename = PathUtil.get_name(keys_filepath)
        dir = str(self.user.id)
        if not self.directory_exists(dir):
            self.ftp.mkd(dir)
        with open(encrypted_filepath, 'rb') as encrypted_file:
            self.ftp.storbinary(f"STOR {dir + '/' + filename}", encrypted_file)
        with open(encrypted_keys_filepath, 'rb') as encrypted_keys_file:
            self.ftp.storbinary(
                f"STOR {dir + '/' + keys_filename}", encrypted_keys_file)

        # Create file reference, and master key
        file_reference = FileReference(
            id=0,
            name=PathUtil.get_name(filepath),
            owner_id=self.user.id,
            owner_name=self.user.name,
            uploaded_at=''
        )
        self.file_references_repository.insert(file_reference, master_keys[0])

    def download(self, file_reference: FileReference, output_filepath: str):
        # Get file request
        file_request = self.file_requests_repository.get(file_reference.id)
        if file_request is None:
            raise Exception("You didn't request this file")
        if file_request.status != FileRequestStatus.ACCEPTED:
            raise Exception("File request not approved")

        filename = file_reference.name
        dir = str(file_reference.owner_id)

        # Check if file exists
        if not self.directory_exists(dir):
            raise Exception("File not found")

        # Download file
        encrypted_filepath = PathUtil.encrypted_filepath(filename)
        with open(encrypted_filepath, 'wb') as encrypted_file:
            self.ftp.retrbinary(
                f"RETR {dir + '/' + filename}", encrypted_file.write)

        # Download keys
        keys_filename = PathUtil.keys_filename(filename)
        encrypted_keys_filepath = PathUtil.encrypted_filepath(keys_filename)
        with open(encrypted_keys_filepath, 'wb') as encrypted_keys_file:
            self.ftp.retrbinary(
                f"RETR {dir + '/' + keys_filename}", encrypted_keys_file.write)

        # Decrypt master key
        master_key = self.master_key_cipher.decrypt(
            self.user.private_key,
            file_request.enc_master_key)

        # Decrypt keys
        keys_filepath = PathUtil.keys_filepath(filename)
        with open(encrypted_keys_filepath, 'rb') as encrypted_keys_file:
            with open(keys_filepath, 'wb') as keys_file:
                self.master_cipher.decrypt(
                    encrypted_keys_file.read, keys_file.write, [master_key])

        # Read keys
        with open(keys_filepath, 'rb') as keys_file:
            keys = [keys_file.read(c.KEY_SIZE) for c in self.cipher.ciphers]

        # Decrypt file
        with open(encrypted_filepath, 'rb') as encrypted_file:
            with open(output_filepath, 'wb') as output_file:
                self.cipher.decrypt(
                    encrypted_file.read, output_file.write, keys)

    def directory_exists(self, dir: str):
        ls: List[str] = []
        self.ftp.retrlines('LIST', ls.append)
        for f in ls:
            if f.split()[-1] == dir and f.upper().startswith('D'):
                return True
        return False
