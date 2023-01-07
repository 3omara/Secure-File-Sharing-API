from __future__ import annotations
from dataclasses import dataclass
from json import dumps, loads
from typing import List, Union
from enum import Enum


class FileRequestStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


@dataclass
class FileRequest:
    file_id: id
    file_name: str
    sender_id: id
    sender_name: str
    receiver_id: id
    receiver_name: str
    status: FileRequestStatus
    sent_at: str

    def to_json(obj: Union[List[FileRequest], FileRequest]):
        if isinstance(obj, list):
            return dumps([o.__dict__ for o in obj])
        return dumps(obj.__dict__)

    def from_json(json: str):
        if isinstance(json, list):
            return [FileRequest.from_json(o) for o in json]
        if isinstance(json, dict):
            return FileRequest(
                json["file_id"],
                json["file_name"],
                json["sender_id"],
                json["sender_name"],
                json["receiver_id"],
                json["receiver_name"],
                json["status"],
                json["sent_at"]
            )
        return FileRequest.from_json(loads(json))
