from dataclasses import dataclass


@dataclass
class File:
    file_id: int
    user_id: int
    file_name:str
    upload_time:str
    file_type:int