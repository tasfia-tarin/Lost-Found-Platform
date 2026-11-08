from fastapi import HTTPException

from schemas import ItemCreate
from crud import item_crud


def create_item_service(item: ItemCreate):
    try:
        return item_crud.create_item(item)
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


def get_items_service():
    try:
        return item_crud.get_items()
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


def get_item_service(item_id: int):
    try:
        item = item_crud.get_item(item_id)

        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return item

    except HTTPException:
        raise
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


def update_item_service(item_id: int, item: ItemCreate):
    try:
        updated_item = item_crud.update_item(item_id, item)

        if updated_item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return updated_item

    except HTTPException:
        raise
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


def delete_item_service(item_id: int):
    try:
        deleted_id = item_crud.delete_item(item_id)

        if deleted_id is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return deleted_id

    except HTTPException:
        raise
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
