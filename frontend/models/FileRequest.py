from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Union


class FileRequestStatus:
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


@dataclass
class FileRequest:
    file_id: int
    file_name: str
    sender_id: int
    sender_name: str
    receiver_id: int
    receiver_name: str
    public_key: bytes
    enc_master_key: bytes
    status: str
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
                res.get("public_key", None),
                res.get("enc_master_key", None),
                res.get("status", None),
                res.get("sent_at", None),
            )
        return FileRequest.from_response(res)
