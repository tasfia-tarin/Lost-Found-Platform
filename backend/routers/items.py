from fastapi import APIRouter

from schemas import ItemCreate
from services import item_service

router = APIRouter(prefix="/api/items", tags=["Items"])


@router.post("")
def create_item(item: ItemCreate):
    created_item = item_service.create_item_service(item)
    return {
        "message": "Item created successfully",
        "item": created_item
    }


@router.get("")
def get_items():
    return {"items": item_service.get_items_service()}


@router.get("/{item_id}")
def get_item(item_id: int):
    return {"item": item_service.get_item_service(item_id)}


@router.put("/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    updated_item = item_service.update_item_service(item_id, item)
    return {
        "message": "Item updated successfully",
        "item": updated_item
    }


@router.delete("/{item_id}")
def delete_item(item_id: int):
    deleted_id = item_service.delete_item_service(item_id)
    return {
        "message": "Item deleted successfully",
        "deleted_item_id": deleted_id
    }
