from fastapi import APIRouter, Depends

from schemas import ItemCreate
from services import item_service
from auth.rbac import Permissions, require_permission


router = APIRouter(prefix="/api/items", tags=["Items"])


# Create Item
@router.post("")
def create_item(
    item: ItemCreate,
    current_user: dict = Depends(
        require_permission(Permissions.CREATE_ITEM)
    )
):
    created_item = item_service.create_item_service(
        item,
        current_user["id"]
    )

    return {
        "message": "Item created successfully",
        "item": created_item
    }


# Get All Items
@router.get("")
def get_items(
    current_user: dict = Depends(
        require_permission(Permissions.READ_OWN_ITEM)
    )
):
    items = item_service.get_items_service(
        current_user["id"],
        current_user["role"] == "admin"
    )

    return {"items": items}


# Get Single Item
@router.get("/{item_id}")
def get_item(
    item_id: int,
    current_user: dict = Depends(
        require_permission(Permissions.READ_OWN_ITEM)
    )
):
    item = item_service.get_item_service(
        item_id,
        current_user["id"],
        current_user["role"] == "admin"
    )

    return {"item": item}


# Update Item
@router.put("/{item_id}")
def update_item(
    item_id: int,
    item: ItemCreate,
    current_user: dict = Depends(
        require_permission(Permissions.UPDATE_OWN_ITEM)
    )
):
    updated_item = item_service.update_item_service(
        item_id,
        item,
        current_user["id"],
        current_user["role"] == "admin"
    )

    return {
        "message": "Item updated successfully",
        "item": updated_item
    }


# Delete Item
@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    current_user: dict = Depends(
        require_permission(Permissions.DELETE_OWN_ITEM)
    )
):
    deleted_id = item_service.delete_item_service(
        item_id,
        current_user["id"],
        current_user["role"] == "admin"
    )

    return {
        "message": "Item deleted successfully",
        "deleted_item_id": deleted_id
    }