import hashlib
import hmac

from pwdlib import PasswordHash
from auth.config import PASSWORD_PEPPER


password_hasher = PasswordHash.recommended()


def _pepper_password(password: str) -> str:
    return hmac.new(
        PASSWORD_PEPPER.encode("utf-8"),
        password.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def hash_password(password: str) -> str:
    peppered_password = _pepper_password(password)
    return password_hasher.hash(peppered_password)


def verify_password(password: str, hashed_password: str) -> bool:
    peppered_password = _pepper_password(password)
    return password_hasher.verify(
        peppered_password,
        hashed_password
    )