from crud.user_crud import get_database_connection
from psycopg.types.json import Jsonb


def create_security_log(
    email: str,
    event_type: str,
    user_id: int = None,
    ip_address: str = None,
    user_agent: str = None,
    details: dict = None
):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.security_logs
                (user_id, email, event_type, ip_address, user_agent, details)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    user_id,
                    email,
                    event_type,
                    ip_address,
                    user_agent,
                    Jsonb(details or {})
                )
            )


def get_security_logs(limit: int = 50, offset: int = 0):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    email,
                    event_type,
                    ip_address,
                    user_agent,
                    details,
                    created_at
                FROM public.security_logs
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset)
            )

            columns = [description[0] for description in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]