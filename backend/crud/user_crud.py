import os
import psycopg


def get_database_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("Database URL not found")

    return psycopg.connect(
        database_url,
        sslmode="require"
    )


def row_to_user(row):
    if row is None:
        return None

    return {
        "id": row[0],
        "email": row[1],
        "password_hash": row[2],
        "role": row[3],
        "is_banned": row[4],
        "failed_login_attempts": row[5],
        "locked_until": row[6],
        "created_at": row[7],
        "updated_at": row[8]
    }


def create_user(email: str, password_hash: str):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.users (email, password_hash)
                VALUES (%s, %s)
                RETURNING id, email, password_hash, role,
                          is_banned, failed_login_attempts,
                          locked_until, created_at, updated_at
                """,
                (email.lower().strip(), password_hash)
            )

            row = cursor.fetchone()

    return row_to_user(row)


def get_user_by_email(email: str):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, password_hash, role,
                       is_banned, failed_login_attempts,
                       locked_until, created_at, updated_at
                FROM public.users
                WHERE LOWER(email) = LOWER(%s)
                """,
                (email.strip(),)
            )

            row = cursor.fetchone()

    return row_to_user(row)


def get_user_by_id(user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, email, password_hash, role,
                       is_banned, failed_login_attempts,
                       locked_until, created_at, updated_at
                FROM public.users
                WHERE id = %s
                """,
                (user_id,)
            )

            row = cursor.fetchone()

    return row_to_user(row)


def reset_failed_login_attempts(user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.users
                SET failed_login_attempts = 0,
                    locked_until = NULL,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (user_id,)
            )


def increment_failed_login_attempts(user_id: int):
    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.users
                SET failed_login_attempts = failed_login_attempts + 1,
                    locked_until = CASE
                        WHEN failed_login_attempts + 1 >= 5
                        THEN NOW() + INTERVAL '15 minutes'
                        ELSE locked_until
                    END,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (user_id,)
            )
    