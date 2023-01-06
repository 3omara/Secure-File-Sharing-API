from dataclasses import dataclass


@dataclass
class FileRequest:
    file_id: int
    sender_id: str 
    status: int
    enc_master_key: bytes