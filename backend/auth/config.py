import os
from datetime import timedelta

from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
PASSWORD_PEPPER = os.getenv("PASSWORD_PEPPER")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not configured")

if not PASSWORD_PEPPER:
    raise RuntimeError("PASSWORD_PEPPER is not configured")

ACCESS_TOKEN_EXPIRE = timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
)
REFRESH_TOKEN_EXPIRE_DAYS = 7

REFRESH_TOKEN_EXPIRE = timedelta(
    days=REFRESH_TOKEN_EXPIRE_DAYS
)