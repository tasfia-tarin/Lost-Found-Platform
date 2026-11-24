
from fastapi import HTTPException

from schemas import ItemCreate
from crud import item_crud


def create_item_service(item: ItemCreate, user_id: int):
    try:
        return item_crud.create_item(item, user_id)

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to create item"
        )


def get_items_service(user_id: int, is_admin: bool):
    try:
        return item_crud.get_items(user_id, is_admin)

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve items"
        )


def get_item_service(
    item_id: int,
    user_id: int,
    is_admin: bool
):
    try:
        item = item_crud.get_item(
            item_id,
            user_id,
            is_admin
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return item

    except HTTPException:
        raise

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve item"
        )


def update_item_service(
    item_id: int,
    item: ItemCreate,
    user_id: int,
    is_admin: bool
):
    try:
        updated_item = item_crud.update_item(
            item_id,
            item,
            user_id,
            is_admin
        )

        if updated_item is None:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return updated_item

    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error)
        )

    except HTTPException:
        raise

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to update item"
        )


def delete_item_service(
    item_id: int,
    user_id: int,
    is_admin: bool
):
    try:
        deleted_id = item_crud.delete_item(
            item_id,
            user_id,
            is_admin
        )

        if deleted_id is None:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return deleted_id

    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error)
        )

    except HTTPException:
        raise

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete item"
        )
