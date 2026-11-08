import os

import psycopg

from schemas import ItemCreate


def get_database_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("Database URL not found")

    return psycopg.connect(
        database_url,
        sslmode="require"
    )


def row_to_item(row):
    if row is None:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "category": row[3],
        "status": row[4],
        "location": row[5],
        "contact_info": row[6],
        "created_at": row[7]
    }


def create_item(item: ItemCreate):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.items
                (title, description, category, status, location, contact_info)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, title, description, category, status,
                          location, contact_info, created_at
                """,
                (
                    item.title,
                    item.description,
                    item.category,
                    item.status,
                    item.location,
                    item.contact_info
                )
            )

            row = cursor.fetchone()

    return row_to_item(row)


def get_items():
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, description, category, status,
                       location, contact_info, created_at
                FROM public.items
                ORDER BY created_at DESC
                """
            )

            rows = cursor.fetchall()

    return [row_to_item(row) for row in rows]


def get_item(item_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, description, category, status,
                       location, contact_info, created_at
                FROM public.items
                WHERE id = %s
                """,
                (item_id,)
            )

            row = cursor.fetchone()

    return row_to_item(row)


def update_item(item_id: int, item: ItemCreate):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.items
                SET title = %s,
                    description = %s,
                    category = %s,
                    status = %s,
                    location = %s,
                    contact_info = %s
                WHERE id = %s
                RETURNING id, title, description, category, status,
                          location, contact_info, created_at
                """,
                (
                    item.title,
                    item.description,
                    item.category,
                    item.status,
                    item.location,
                    item.contact_info,
                    item_id
                )
            )

            row = cursor.fetchone()

    return row_to_item(row)


def delete_item(item_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM public.items
                WHERE id = %s
                RETURNING id
                """,
                (item_id,)
            )

            row = cursor.fetchone()

    return row[0] if row else None
