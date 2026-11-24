from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from auth.dependencies import require_admin

from crud.user_crud import (
    get_all_users,
    count_users,
    get_user_statistics,
    ban_user,
    unban_user,
    update_user_role,
    get_user_by_id,
)

from crud.session_crud import revoke_all_user_sessions

from crud.audit_crud import (
    create_audit_log,
    get_audit_logs,
)

from crud.security_crud import get_security_logs


router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],
)


class BanUserRequest(BaseModel):
    reason: str = Field(
        min_length=3,
        max_length=500,
        description="Reason for banning the user"
    )


class UpdateRoleRequest(BaseModel):
    role: str = Field(
        pattern="^(admin|user)$",
        description="New role: admin or user"
    )




@router.get("/users")
def list_users(
    search: str = Query(default="", max_length=100),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    users = get_all_users(
        search=search,
        limit=limit,
        offset=offset,
    )

    total = count_users(search=search)

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "users": users,
    }




@router.get("/stats")
def admin_statistics():
    return get_user_statistics()





@router.post("/users/{user_id}/ban")
def ban_user_account(
    user_id: int,
    request: BanUserRequest,
    current_admin: dict = Depends(require_admin),
):
    result = ban_user(user_id, request.reason)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found or cannot be banned",
        )

    create_audit_log(
        actor_user_id=current_admin["id"],
        action="USER_BANNED",
        target_user_id=user_id,
        details={
            "reason": request.reason,
        },
    )

    return {
        "message": "User banned successfully",
        "user": result,
    }



@router.post("/users/{user_id}/unban")
def unban_user_account(
    user_id: int,
    current_admin: dict = Depends(require_admin),
):
    result = unban_user(user_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found or cannot be unbanned",
        )

    create_audit_log(
        actor_user_id=current_admin["id"],
        action="USER_UNBANNED",
        target_user_id=user_id,
        details={},
    )

    return {
        "message": "User unbanned successfully",
        "user": result,
    }




@router.patch("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    request: UpdateRoleRequest,
    current_admin: dict = Depends(require_admin),
):
    if current_admin["id"] == user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot change your own role",
        )

    result = update_user_role(user_id, request.role)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found or target is already an admin",
        )

    create_audit_log(
        actor_user_id=current_admin["id"],
        action="USER_ROLE_CHANGED",
        target_user_id=user_id,
        details={
            "new_role": result["role"],
        },
    )

    return {
        "message": "User role updated successfully",
        "user": result,
    }




@router.post("/users/{user_id}/revoke-sessions")
def admin_revoke_user_sessions(
    user_id: int,
    current_admin: dict = Depends(require_admin),
):
    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    revoked_count = revoke_all_user_sessions(user_id)

    create_audit_log(
        actor_user_id=current_admin["id"],
        action="USER_SESSIONS_REVOKED",
        target_user_id=user_id,
        details={
            "revoked_sessions": revoked_count,
        },
    )

    return {
        "message": "User sessions revoked successfully",
        "user_id": user_id,
        "revoked_sessions": revoked_count,
    }




@router.get("/audit-logs")
def list_audit_logs(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    logs = get_audit_logs(
        limit=limit,
        offset=offset,
    )

    return {
        "total_returned": len(logs),
        "logs": logs,
    }

@router.get("/security-logs")
def list_security_logs(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    logs = get_security_logs(
        limit=limit,
        offset=offset,
    )

    return {
        "total_returned": len(logs),
        "logs": logs,
    }