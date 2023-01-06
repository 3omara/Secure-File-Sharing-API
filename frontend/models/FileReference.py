from dataclasses import dataclass
from json import dumps, loads
from typing import List, Union


@dataclass
class FileReference:
    TABLE_NAME = "file_references"

    id: int
    name: str
    owner_id: int
    owner_name: str
    master_key: bytes
    uploaded_at: str

    def to_json(obj: Union[List["FileReference"], "FileReference"]):
        if isinstance(obj, list):
            return dumps([o.__dict__ for o in obj])
        return dumps(obj.__dict__)

    def from_json(json: str):
        if isinstance(json, list):
            return [FileReference.from_json(o) for o in json]
        if isinstance(json, dict):
            return FileReference(
                json["id"],
                json["name"],
                json["owner_id"],
                json["owner_name"],
                json["master_key"],
                json["uploaded_at"]
            )
        return FileReference.from_json(loads(json))
