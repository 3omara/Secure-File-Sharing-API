from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    pending = 0
    accepted = 1
    declined = 2

@dataclass
class File:
    file_id: int
    user_id: int
    file_name:str
    upload_time:str
    file_type:int