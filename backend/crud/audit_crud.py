from psycopg.types.json import Jsonb

from crud.user_crud import get_database_connection


def create_audit_log(
    actor_user_id: int,
    action: str,
    target_user_id: int | None = None,
    details: dict | None = None,
):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.audit_logs
                (actor_user_id, action, target_user_id, details)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    actor_user_id,
                    action,
                    target_user_id,
                    Jsonb(details or {}),
                ),
            )

            return cursor.fetchone()[0]


def get_audit_logs(limit: int = 50, offset: int = 0):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, actor_user_id, action,
                       target_user_id, details, created_at
                FROM public.audit_logs
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )

            rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "actor_user_id": row[1],
            "action": row[2],
            "target_user_id": row[3],
            "details": row[4],
            "created_at": row[5],
        }
        for row in rows
    ]