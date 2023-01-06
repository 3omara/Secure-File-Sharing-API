from dataclasses import dataclass


@dataclass
class FileReference:
    TABLE_NAME = "file_references"

    id: int
    name: str
    owner_id: int
    owner_name: str
    master_key: bytes
    uploaded_at: str
