from ftplib import FTP
from ciphers.FileCipher import FileCipher
from models.FileReference import FileReference
from repositories.FileReferencesRepository import FileReferencesRepository
from shared import PathUtil


class SecureFTPService:
    def __init__(self,
                 ftp: FTP,
                 cipher: FileCipher,
                 master_cipher: FileCipher,
                 file_references_repository: FileReferencesRepository,
                 ):
        self.ftp = ftp
        self.ftp.encoding = "utf-8"
        self.cipher = cipher
        self.master_cipher = master_cipher
        self.file_references_repository = file_references_repository
        PathUtil.setup_secure_ftp_cache()

    def connect(self, host, port=0, timeout=-999):
        return self.ftp.connect(host, port, timeout)

    def login(self, user='', passwd='', acct=''):
        return self.ftp.login(user, passwd, acct)

    def upload(self, filepath: str):
        filename = PathUtil.get_name(filepath)
        encrypted_filepath = PathUtil.encrypted_filepath(filename)
        keys = self.cipher.generate_keys()
        with open(filepath, 'rb') as file:
            with open(encrypted_filepath, 'wb') as encrypted_file:
                self.cipher.encrypt(
                    file.read, encrypted_file.write, keys)

        keys_filepath = PathUtil.keys_filepath(filename)
        encrypted_keys_filepath = PathUtil.encrypted_filepath(keys_filepath)
        master_keys = self.master_cipher.generate_keys()
        with open(keys_filepath, 'wb') as keys_file:
            keys_file.writelines(keys)
        with open(keys_filepath, 'rb') as keys_file:
            with open(encrypted_keys_filepath, 'wb') as encrypted_keys_file:
                self.master_cipher.encrypt(
                    keys_file.read, encrypted_keys_file.write, master_keys)

        keys_filename = PathUtil.get_name(keys_filepath)
        dir = "1"
        if not self.directory_exists(dir):
            self.ftp.mkd(dir)
        with open(encrypted_filepath, 'rb') as encrypted_file:
            self.ftp.storbinary(f"STOR {dir + '/' + filename}", encrypted_file)
        with open(keys_filepath, 'rb') as encrypted_keys_file:
            self.ftp.storbinary(
                f"STOR {dir + '/' + keys_filename}", encrypted_keys_file)

        # file_reference = FileReference(
        #     id=0,
        #     name=PathUtil.get_name(filepath),
        #     owner_id=1,
        #     owner_name='Admin',
        #     master_key=master_keys[0],
        #     uploaded_at=''
        # )
        # self.file_references_repository.insert(file_reference)

    def directory_exists(self, dir):
        filelist = []
        self.ftp.retrlines('LIST', filelist.append)
        for f in filelist:
            if f.split()[-1] == dir and f.upper().startswith('D'):
                return True
        return False
