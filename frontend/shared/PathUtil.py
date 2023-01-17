import os
import pathlib

SECURE_FTP_CACHE = 'secure_ftp_cache'


def setup_secure_ftp_cache():
    if not os.path.exists(SECURE_FTP_CACHE):
        os.mkdir(SECURE_FTP_CACHE)


def get_name(filepath: str) -> str:
    return os.path.basename(filepath)


def extension(filepath: str) -> str:
    return pathlib.Path(filepath).suffix


def encrypted_filepath(filepath: str) -> str:
    return f"{SECURE_FTP_CACHE}/" + get_name(filepath) + ".enc"


def decrypted_filepath(filepath: str) -> str:
    return f"{SECURE_FTP_CACHE}/" + get_name(filepath) + ".dec"


def keys_filepath(filepath: str) -> str:
    return f"{SECURE_FTP_CACHE}/" + keys_filename(filepath)


def keys_filename(filepath: str) -> str:
    return get_name(filepath) + ".keys"
