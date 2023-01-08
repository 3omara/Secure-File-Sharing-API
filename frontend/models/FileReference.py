from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Union


@dataclass
class FileReference:
    TABLE_NAME = "file_references"

    id: int
    name: str
    owner_id: int
    owner_name: str
    uploaded_at: str

    def to_response(obj: Union[List[FileReference], FileReference]):
        if isinstance(obj, list):
            return [o.__dict__ for o in obj]
        return obj.__dict__

    def from_response(res: Union[List, Dict]):
        if isinstance(res, list):
            return [FileReference.from_response(o) for o in res]
        if isinstance(res, dict):
            return FileReference(
                res.get("id", None),
                res.get("name", None),
                res.get("owner_id", None),
                res.get("owner_name", None),
                res.get("uploaded_at", None),
            )
        return FileReference.from_response(res)
