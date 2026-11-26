from fastapi import APIRouter, Depends, HTTPException, status

from auth.dependencies import get_current_user
from crud import group_crud


router = APIRouter(
    prefix="/api/groups",
    tags=["Groups"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_group(
    data: dict,
    current_user: dict = Depends(get_current_user)
):
    name = data.get("name", "").strip()
    description = data.get("description", "")

    if not name:
        raise HTTPException(status_code=400, detail="Group name is required")

    return group_crud.create_group(
        name=name,
        description=description,
        owner_id=current_user["id"]
    )


@router.get("/")
def get_my_groups(current_user: dict = Depends(get_current_user)):
    return group_crud.get_user_groups(current_user["id"])


@router.get("/{group_id}")
def get_group(
    group_id: int,
    current_user: dict = Depends(get_current_user)
):
    group = group_crud.get_group_details(group_id, current_user["id"])

    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    return group


@router.put("/{group_id}")
def update_existing_group(
    group_id: int,
    data: dict,
    current_user: dict = Depends(get_current_user)
):
    name = data.get("name", "").strip()
    description = data.get("description", "")

    if not name:
        raise HTTPException(status_code=400, detail="Group name is required")

    group = group_crud.update_group(
        group_id=group_id,
        owner_id=current_user["id"],
        name=name,
        description=description
    )

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found or you are not the owner"
        )

    return group


@router.delete("/{group_id}")
def delete_existing_group(
    group_id: int,
    current_user: dict = Depends(get_current_user)
):
    deleted = group_crud.delete_group(group_id, current_user["id"])

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Group not found or you are not the owner"
        )

    return {"message": "Group deleted successfully"}


@router.post("/{group_id}/members")
def add_member(
    group_id: int,
    data: dict,
    current_user: dict = Depends(get_current_user)
):
    email = data.get("email", "").strip()

    if not email:
        raise HTTPException(status_code=400, detail="Member email is required")

    result = group_crud.add_group_member(
        group_id=group_id,
        owner_id=current_user["id"],
        member_email=email
    )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@router.get("/{group_id}/members")
def get_members(
    group_id: int,
    current_user: dict = Depends(get_current_user)
):
    members = group_crud.get_group_members(group_id, current_user["id"])

    if members is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found or you are not a member"
        )

    return members


@router.put("/{group_id}/members/{member_id}/permissions")
def update_permissions(
    group_id: int,
    member_id: int,
    data: dict,
    current_user: dict = Depends(get_current_user)
):
    result = group_crud.update_member_permissions(
        group_id=group_id,
        owner_id=current_user["id"],
        member_id=member_id,
        can_read_items=data.get("can_read_items", False),
        can_create_items=data.get("can_create_items", False),
        can_update_items=data.get("can_update_items", False),
        can_delete_items=data.get("can_delete_items", False)
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Group or member not found, or permission denied"
        )

    return result


@router.delete("/{group_id}/members/{member_id}")
def remove_member(
    group_id: int,
    member_id: int,
    current_user: dict = Depends(get_current_user)
):
    removed = group_crud.remove_group_member(
        group_id=group_id,
        owner_id=current_user["id"],
        member_id=member_id
    )

    if not removed:
        raise HTTPException(
            status_code=404,
            detail="Group or member not found, or permission denied"
        )

    return {"message": "Member removed successfully"}


@router.post("/{group_id}/items", status_code=status.HTTP_201_CREATED)
def share_item(
    group_id: int,
    data: dict,
    current_user: dict = Depends(get_current_user)
):
    item_id = data.get("item_id")

    if not isinstance(item_id, int) or isinstance(item_id, bool) or item_id <= 0:
        raise HTTPException(status_code=400, detail="A valid item_id is required")

    result = group_crud.share_item_with_group(
        group_id=group_id,
        item_id=item_id,
        user_id=current_user["id"]
    )

    if "error" in result:
        raise HTTPException(status_code=403, detail=result["error"])

    return result


@router.get("/{group_id}/items")
def get_shared_items(
    group_id: int,
    current_user: dict = Depends(get_current_user)
):
    result = group_crud.get_group_items(group_id, current_user["id"])

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found or you are not a member"
        )

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=403, detail=result["error"])

    return result


@router.put("/{group_id}/items/{item_id}")
def update_shared_item(
    group_id: int,
    item_id: int,
    data: dict,
    current_user: dict = Depends(get_current_user)
):
    result = group_crud.update_shared_item(
        group_id=group_id,
        item_id=item_id,
        user_id=current_user["id"],
        data=data
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Shared item not found or you are not a group member"
        )

    if "error" in result:
        raise HTTPException(status_code=403, detail=result["error"])

    return result


@router.delete("/{group_id}/items/{item_id}")
def remove_shared_item(
    group_id: int,
    item_id: int,
    current_user: dict = Depends(get_current_user)
):
    result = group_crud.remove_shared_item(
        group_id=group_id,
        item_id=item_id,
        user_id=current_user["id"]
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Shared item not found or you are not a group member"
        )

    if "error" in result:
        raise HTTPException(status_code=403, detail=result["error"])

    return result