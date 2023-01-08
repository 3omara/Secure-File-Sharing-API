from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Union
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
    master_key: bytes
    status: FileRequestStatus
    sent_at: str

    def to_response(obj: Union[List[FileRequest], FileRequest]):
        if isinstance(obj, list):
            return [o.__dict__ for o in obj]
        return obj.__dict__

    def from_response(res: Union[List, Dict]):
        if isinstance(res, list):
            return [FileRequest.from_response(o) for o in res]
        if isinstance(res, dict):
            return FileRequest(
                res.get("file_id", None),
                res.get("file_name", None),
                res.get("sender_id", None),
                res.get("sender_name", None),
                res.get("receiver_id", None),
                res.get("receiver_name", None),
                res.get("master_key", None),
                res.get("status", None),
                res.get("sent_at", None),
            )
        return FileRequest.from_response(res)
