from datetime import datetime, timezone

import psycopg
from fastapi import APIRouter, HTTPException, status

from auth.schemas import SignupRequest, LoginRequest
from auth.passwords import hash_password, verify_password
from auth.tokens import create_access_token
from crud.user_crud import (
    create_user,
    get_user_by_email,
    reset_failed_login_attempts,
    increment_failed_login_attempts,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest):

    existing_user = get_user_by_email(data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    password_hash = hash_password(data.password)

    try:
        user = create_user(data.email, password_hash)
    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    token = create_access_token(
        user_id=user["id"],
        role=user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "is_banned": user["is_banned"]
        }
    }


@router.post("/login")
def login(data: LoginRequest):

    user = get_user_by_email(data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if user["is_banned"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been banned"
        )

    locked_until = user["locked_until"]

    if locked_until and locked_until > datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Account temporarily locked"
        )

    if not verify_password(
        data.password,
        user["password_hash"]
    ):
        increment_failed_login_attempts(user["id"])

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    reset_failed_login_attempts(user["id"])

    token = create_access_token(
        user_id=user["id"],
        role=user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "is_banned": user["is_banned"]
        }
    }