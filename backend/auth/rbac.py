from fastapi import Depends, HTTPException, status

from auth.dependencies import get_current_user


# Permission Constants
class Permissions:
    CREATE_ITEM = "create_item"
    READ_OWN_ITEM = "read_own_item"
    UPDATE_OWN_ITEM = "update_own_item"
    DELETE_OWN_ITEM = "delete_own_item"

    READ_ALL_ITEMS = "read_all_items"
    MANAGE_USERS = "manage_users"
    MANAGE_GROUPS = "manage_groups"
    VIEW_AUDIT_LOGS = "view_audit_logs"


# Role-based permissions
ROLE_PERMISSIONS = {
    "user": {
        Permissions.CREATE_ITEM,
        Permissions.READ_OWN_ITEM,
        Permissions.UPDATE_OWN_ITEM,
        Permissions.DELETE_OWN_ITEM,
    },

    "admin": {
        Permissions.CREATE_ITEM,
        Permissions.READ_OWN_ITEM,
        Permissions.UPDATE_OWN_ITEM,
        Permissions.DELETE_OWN_ITEM,
        Permissions.READ_ALL_ITEMS,
        Permissions.MANAGE_USERS,
        Permissions.MANAGE_GROUPS,
        Permissions.VIEW_AUDIT_LOGS,
    },
}


# Check whether a user has a permission
def has_permission(user: dict, permission: str) -> bool:
    role = user.get("role")

    allowed_permissions = ROLE_PERMISSIONS.get(role, set())

    return permission in allowed_permissions


# Reusable permission dependency
def require_permission(permission: str):

    def permission_checker(
        current_user: dict = Depends(get_current_user)
    ):
        if not has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return permission_checker