from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str
    password_hash: str
    role: str = "user"
    is_banned: bool = False
    created_at: datetime | None = None