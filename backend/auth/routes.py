
from datetime import datetime, timezone

import psycopg

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Request,
    Response,
    Depends,
)

from auth.schemas import (
    SignupRequest,
    LoginRequest,
    ProfileUpdateRequest,
    PasswordChangeRequest,
)

from auth.passwords import hash_password, verify_password

from auth.tokens import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
)

from auth.config import REFRESH_TOKEN_EXPIRE
from auth.dependencies import get_current_user

from crud.user_crud import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    update_user_email,
    update_user_password,
    reset_failed_login_attempts,
    increment_failed_login_attempts,
)

from crud.session_crud import (
    create_refresh_session,
    rotate_refresh_session,
    get_active_refresh_session,
    revoke_refresh_session,
    get_user_active_sessions,
    revoke_all_user_sessions,
)

from crud.security_crud import create_security_log


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# Create and save refresh token
def issue_refresh_token(user_id: int, request: Request):

    refresh_token = create_refresh_token()
    token_hash = hash_refresh_token(refresh_token)

    expires_at = datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRE

    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None

    create_refresh_session(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    return refresh_token


# Set refresh token cookie
def set_refresh_cookie(
    response: Response,
    request: Request,
    refresh_token: str
):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=request.url.scheme == "https",
        samesite="lax",
        max_age=int(REFRESH_TOKEN_EXPIRE.total_seconds()),
        path="/api/auth",
    )

# GET CURRENT USER
@router.get("/me")
def get_me(
    current_user: dict = Depends(get_current_user)
):
    return {
        "user": current_user
    }

# SIGNUP
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(
    data: SignupRequest,
    request: Request,
    response: Response
):
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

    access_token = create_access_token(
        user_id=user["id"],
        role=user["role"]
    )

    refresh_token = issue_refresh_token(user["id"], request)

    set_refresh_cookie(response, request, refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "is_banned": user["is_banned"]
        }
    }


# LOGIN
@router.post("/login")
def login(
    data: LoginRequest,
    request: Request,
    response: Response
):
    user = get_user_by_email(data.email)

    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    if not user:
        create_security_log(
            email=data.email,
            event_type="FAILED_LOGIN",
            ip_address=ip_address,
            user_agent=user_agent,
            details={"reason": "unknown_email"}
        )

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

    if not verify_password(data.password, user["password_hash"]):
        increment_failed_login_attempts(user["id"])

        create_security_log(
            email=data.email,
            event_type="FAILED_LOGIN",
            user_id=user["id"],
            ip_address=ip_address,
            user_agent=user_agent,
            details={"reason": "incorrect_password"}
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    reset_failed_login_attempts(user["id"])

    access_token = create_access_token(
        user_id=user["id"],
        role=user["role"]
    )

    refresh_token = issue_refresh_token(user["id"], request)

    set_refresh_cookie(response, request, refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "is_banned": user["is_banned"]
        }
    }


# REFRESH ACCESS TOKEN
@router.post("/refresh")
def refresh_access_token(
    request: Request,
    response: Response
):
    old_token = request.cookies.get("refresh_token")

    if not old_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )

    new_refresh_token = create_refresh_token()

    new_token_hash = hash_refresh_token(new_refresh_token)

    expires_at = datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRE

    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host if request.client else None

    user_id = rotate_refresh_session(
        old_token_hash=hash_refresh_token(old_token),
        new_token_hash=new_token_hash,
        expires_at=expires_at,
        user_agent=user_agent,
        ip_address=ip_address,
    )

    if not user_id:
        response.delete_cookie(
            key="refresh_token",
            path="/api/auth"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    user = get_user_by_id(user_id)

    if not user or user["is_banned"]:
        revoke_all_user_sessions(user_id)

        response.delete_cookie(
            key="refresh_token",
            path="/api/auth"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is unavailable"
        )

    access_token = create_access_token(
        user_id=user["id"],
        role=user["role"]
    )

    set_refresh_cookie(response, request, new_refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# LOGOUT
@router.post("/logout")
def logout(
    request: Request,
    response: Response
):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        session = get_active_refresh_session(
            hash_refresh_token(refresh_token)
        )

        if session:
            revoke_refresh_session(session[0])

    response.delete_cookie(
        key="refresh_token",
        path="/api/auth"
    )

    return {
        "message": "Logged out successfully"
    }


# VIEW ACTIVE SESSIONS
@router.get("/sessions")
def list_sessions(
    current_user: dict = Depends(get_current_user)
):
    sessions = get_user_active_sessions(current_user["id"])

    return [
        {
            "id": session[0],
            "created_at": session[1],
            "expires_at": session[2],
            "user_agent": session[3],
            "ip_address": str(session[4]) if session[4] else None
        }
        for session in sessions
    ]


# REVOKE A SESSION
@router.delete("/sessions/{session_id}/revoke")
def revoke_session(
    session_id: int,
    current_user: dict = Depends(get_current_user)
):
    sessions = get_user_active_sessions(current_user["id"])

    owned_session_ids = [session[0] for session in sessions]

    if session_id not in owned_session_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    revoke_refresh_session(session_id)

    return {
        "message": "Session revoked successfully"
    }


# UPDATE PROFILE EMAIL
@router.patch("/profile")
def update_profile(
    data: ProfileUpdateRequest,
    current_user: dict = Depends(get_current_user),
):
    if data.email is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No profile information provided",
        )

    try:
        user = update_user_email(
            current_user["id"],
            str(data.email),
        )

    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    return {
        "message": "Profile updated successfully",
        "user": user,
    }


# CHANGE PASSWORD
@router.post("/change-password")
def change_password(
    data: PasswordChangeRequest,
    response: Response,
    current_user: dict = Depends(get_current_user),
):
    user = get_user_by_id(current_user["id"])

    if not verify_password(
        data.current_password,
        user["password_hash"],
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    if verify_password(
        data.new_password,
        user["password_hash"],
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different",
        )

    new_password_hash = hash_password(data.new_password)

    update_user_password(
        current_user["id"],
        new_password_hash,
    )

    revoke_all_user_sessions(current_user["id"])

    response.delete_cookie(
        key="refresh_token",
        path="/api/auth",
    )

    return {
        "message": "Password changed successfully. Please log in again."
    }
