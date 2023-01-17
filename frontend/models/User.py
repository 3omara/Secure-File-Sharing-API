from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    private_key: bytes
