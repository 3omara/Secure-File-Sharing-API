from dataclasses import dataclass
from flask_login import UserMixin


@dataclass
class User(UserMixin):
    id: int
    user_name: str
    password: str
    public_key: bytes
    sid: str

    def get_id(self):
        return str(self.id)
