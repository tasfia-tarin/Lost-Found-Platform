from crud.user_crud import get_database_connection


def create_group(name: str, description: str, owner_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO public.groups
                    (name, description, owner_id)
                VALUES (%s, %s, %s)
                RETURNING id, name, description, owner_id, created_at
                """,
                (name.strip(), description, owner_id)
            )

            group = cursor.fetchone()

            cursor.execute(
                """
                INSERT INTO public.group_members
                    (
                        group_id,
                        user_id,
                        member_role,
                        can_read_items,
                        can_create_items,
                        can_update_items,
                        can_delete_items
                    )
                VALUES (%s, %s, 'owner', TRUE, TRUE, TRUE, TRUE)
                """,
                (group[0], owner_id)
            )

    return {
        "id": group[0],
        "name": group[1],
        "description": group[2],
        "owner_id": group[3],
        "created_at": group[4]
    }


def get_user_groups(user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    g.id,
                    g.name,
                    g.description,
                    g.owner_id,
                    g.created_at,
                    gm.member_role
                FROM public.group_members gm
                JOIN public.groups g ON g.id = gm.group_id
                WHERE gm.user_id = %s
                ORDER BY g.created_at DESC
                """,
                (user_id,)
            )

            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "owner_id": row[3],
            "created_at": row[4],
            "member_role": row[5]
        }
        for row in rows
    ]


def get_group_details(group_id: int, user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    g.id,
                    g.name,
                    g.description,
                    g.owner_id,
                    g.created_at,
                    gm.member_role
                FROM public.groups g
                JOIN public.group_members gm ON g.id = gm.group_id
                WHERE g.id = %s AND gm.user_id = %s
                """,
                (group_id, user_id)
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "owner_id": row[3],
        "created_at": row[4],
        "member_role": row[5]
    }


def update_group(
    group_id: int,
    owner_id: int,
    name: str,
    description: str
):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.groups
                SET name = %s,
                    description = %s,
                    updated_at = NOW()
                WHERE id = %s AND owner_id = %s
                RETURNING id, name, description, owner_id, updated_at
                """,
                (name.strip(), description, group_id, owner_id)
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
        "owner_id": row[3],
        "updated_at": row[4]
    }


def delete_group(group_id: int, owner_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM public.groups
                WHERE id = %s AND owner_id = %s
                """,
                (group_id, owner_id)
            )

            return cursor.rowcount > 0


def add_group_member(
    group_id: int,
    owner_id: int,
    member_email: str
):
    from crud.user_crud import get_user_by_email

    member = get_user_by_email(member_email)

    if member is None:
        return {"error": "User not found"}

    if member["id"] == owner_id:
        return {"error": "You are already the group owner"}

    with get_database_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id
                FROM public.groups
                WHERE id = %s AND owner_id = %s
                """,
                (group_id, owner_id)
            )

            if cursor.fetchone() is None:
                return {
                    "error": "Group not found or you are not the owner"
                }

            cursor.execute(
                """
                INSERT INTO public.group_members
                    (group_id, user_id, member_role)
                VALUES (%s, %s, 'member')
                ON CONFLICT (group_id, user_id) DO NOTHING
                RETURNING id
                """,
                (group_id, member["id"])
            )

            if cursor.fetchone() is None:
                return {"error": "User is already a group member"}

    return {
        "message": "Member added successfully",
        "user_id": member["id"],
        "email": member["email"]
    }


def get_group_members(group_id: int, user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT 1
                FROM public.group_members
                WHERE group_id = %s AND user_id = %s
                """,
                (group_id, user_id)
            )

            if cursor.fetchone() is None:
                return None

            cursor.execute(
                """
                SELECT
                    u.id,
                    u.email,
                    gm.member_role,
                    gm.can_read_items,
                    gm.can_create_items,
                    gm.can_update_items,
                    gm.can_delete_items,
                    gm.added_at
                FROM public.group_members gm
                JOIN public.users u ON u.id = gm.user_id
                WHERE gm.group_id = %s
                ORDER BY gm.added_at
                """,
                (group_id,)
            )

            rows = cursor.fetchall()

    return [
        {
            "user_id": row[0],
            "email": row[1],
            "member_role": row[2],
            "can_read_items": row[3],
            "can_create_items": row[4],
            "can_update_items": row[5],
            "can_delete_items": row[6],
            "added_at": row[7]
        }
        for row in rows
    ]


def update_member_permissions(
    group_id: int,
    owner_id: int,
    member_id: int,
    can_read_items: bool,
    can_create_items: bool,
    can_update_items: bool,
    can_delete_items: bool
):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.group_members gm
                SET
                    can_read_items = %s,
                    can_create_items = %s,
                    can_update_items = %s,
                    can_delete_items = %s
                FROM public.groups g
                WHERE gm.group_id = g.id
                  AND gm.group_id = %s
                  AND gm.user_id = %s
                  AND g.owner_id = %s
                  AND gm.member_role = 'member'
                RETURNING
                    gm.user_id,
                    gm.can_read_items,
                    gm.can_create_items,
                    gm.can_update_items,
                    gm.can_delete_items
                """,
                (
                    can_read_items,
                    can_create_items,
                    can_update_items,
                    can_delete_items,
                    group_id,
                    member_id,
                    owner_id
                )
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "user_id": row[0],
        "can_read_items": row[1],
        "can_create_items": row[2],
        "can_update_items": row[3],
        "can_delete_items": row[4]
    }


def remove_group_member(
    group_id: int,
    owner_id: int,
    member_id: int
):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM public.group_members gm
                USING public.groups g
                WHERE gm.group_id = g.id
                  AND gm.group_id = %s
                  AND gm.user_id = %s
                  AND g.owner_id = %s
                  AND gm.member_role = 'member'
                """,
                (group_id, member_id, owner_id)
            )

            return cursor.rowcount > 0


def get_group_member_permissions(group_id: int, user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    can_read_items,
                    can_create_items,
                    can_update_items,
                    can_delete_items
                FROM public.group_members
                WHERE group_id = %s AND user_id = %s
                """,
                (group_id, user_id)
            )

            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "can_read_items": row[0],
        "can_create_items": row[1],
        "can_update_items": row[2],
        "can_delete_items": row[3]
    }


def share_item_with_group(
    group_id: int,
    item_id: int,
    user_id: int
):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:

            # Check group membership and permission
            cursor.execute(
                """
                SELECT can_create_items
                FROM public.group_members
                WHERE group_id = %s AND user_id = %s
                """,
                (group_id, user_id)
            )

            permission = cursor.fetchone()

            if permission is None:
                return {"error": "You are not a member of this group"}

            if not permission[0]:
                return {
                    "error": "You do not have permission to share items"
                }

            # Check item ownership
            cursor.execute(
                """
                SELECT id, title
                FROM public.items
                WHERE id = %s AND user_id = %s
                """,
                (item_id, user_id)
            )

            item = cursor.fetchone()

            if item is None:
                return {
                    "error": "Item not found or you are not the owner"
                }

            # Share item with group
            cursor.execute(
                """
                INSERT INTO public.group_items
                    (group_id, item_id, added_by)
                VALUES (%s, %s, %s)
                ON CONFLICT (group_id, item_id) DO NOTHING
                RETURNING id
                """,
                (group_id, item_id, user_id)
            )

            result = cursor.fetchone()

    if result is None:
        return {"error": "This item is already shared with the group"}

    return {
        "message": "Item shared with group successfully",
        "group_id": group_id,
        "item_id": item_id,
        "title": item[1]
    }


def get_group_items(group_id: int, user_id: int):
    permissions = get_group_member_permissions(group_id, user_id)

    if permissions is None:
        return None

    if not permissions["can_read_items"]:
        return {
            "error": "You do not have permission to view group items"
        }

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    i.id,
                    i.title,
                    i.description,
                    i.category,
                    i.status,
                    i.location,
                    i.contact_info,
                    i.created_at,
                    i.user_id,
                    gi.added_by,
                    gi.added_at
                FROM public.group_items gi
                JOIN public.items i ON i.id = gi.item_id
                WHERE gi.group_id = %s
                ORDER BY gi.added_at DESC
                """,
                (group_id,)
            )

            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "category": row[3],
            "status": row[4],
            "location": row[5],
            "contact_info": row[6],
            "created_at": row[7],
            "owner_id": row[8],
            "shared_by": row[9],
            "shared_at": row[10]
        }
        for row in rows
    ]


def update_shared_item(
    group_id: int,
    item_id: int,
    user_id: int,
    data: dict
):
    permissions = get_group_member_permissions(group_id, user_id)

    if permissions is None:
        return None

    if not permissions["can_update_items"]:
        return {"error": "You do not have permission to update items"}

    allowed_fields = {
        "title",
        "description",
        "category",
        "status",
        "location",
        "contact_info"
    }

    updates = {
        key: value
        for key, value in data.items()
        if key in allowed_fields
    }

    if not updates:
        return {"error": "No valid fields provided"}

    with get_database_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT i.id
                FROM public.group_items gi
                JOIN public.items i ON i.id = gi.item_id
                WHERE gi.group_id = %s AND i.id = %s
                """,
                (group_id, item_id)
            )

            if cursor.fetchone() is None:
                return None

            set_clause = ", ".join(
                f"{field} = %s" for field in updates
            )

            values = list(updates.values())
            values.extend([item_id])

            cursor.execute(
                f"""
                UPDATE public.items
                SET {set_clause}
                WHERE id = %s
                RETURNING id, title, description, category,
                          status, location, contact_info
                """,
                values
            )

            row = cursor.fetchone()

    return {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "category": row[3],
        "status": row[4],
        "location": row[5],
        "contact_info": row[6],
        "message": "Shared item updated successfully"
    }


def remove_shared_item(
    group_id: int,
    item_id: int,
    user_id: int
):
    permissions = get_group_member_permissions(group_id, user_id)

    if permissions is None:
        return None

    if not permissions["can_delete_items"]:
        return {"error": "You do not have permission to remove items"}

    with get_database_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM public.group_items
                WHERE group_id = %s AND item_id = %s
                RETURNING id
                """,
                (group_id, item_id)
            )

            result = cursor.fetchone()

    if result is None:
        return None

    return {
        "message": "Item removed from group successfully",
        "group_id": group_id,
        "item_id": item_id
    }