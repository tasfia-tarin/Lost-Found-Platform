import os
import sys
from pathlib import Path

# Add backend folder to Python path
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

# Test environment variables
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-rbac")
os.environ.setdefault("PASSWORD_PEPPER", "test-password-pepper")

from auth.rbac import has_permission, Permissions


def test_user_can_create_item():
    user = {"id": 1, "role": "user"}

    assert has_permission(user, Permissions.CREATE_ITEM) is True


def test_user_cannot_manage_users():
    user = {"id": 1, "role": "user"}

    assert has_permission(user, Permissions.MANAGE_USERS) is False


def test_admin_can_read_all_items():
    admin = {"id": 2, "role": "admin"}

    assert has_permission(admin, Permissions.READ_ALL_ITEMS) is True